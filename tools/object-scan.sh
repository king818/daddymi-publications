#!/usr/bin/env bash
# object-scan.sh — server-side object-scan gate (GitHub Actions check "object-scan").
# Implements Q-A of the signed video-storage architecture (2026-11-23):
# scans every git object NEWLY INTRODUCED in BASE..HEAD (not just the final
# tree — a blob added and deleted inside the range is still scanned), and
# FAILS when a new blob is:
#   * a media payload by extension (video / audio / HLS, case-insensitive),
#   * a media or archive payload by magic bytes (incl. renamed files),
#   * an archive payload by extension,
#   * larger than 5 MiB (hard cap, any type).
# WARNS (annotation only) on non-text blobs larger than 2 MiB.
# Special case: ".ts" fails only when the content is MPEG-TS (sync bytes) or
# binary — plain-text TypeScript sources are not HLS segments.
# Usage: object-scan.sh <base-sha> <head-sha>
set -uo pipefail

BASE="${1:-}"
HEAD="${2:-}"
HARD_LIMIT=$((5 * 1024 * 1024))
WARN_LIMIT=$((2 * 1024 * 1024))
ZERO="0000000000000000000000000000000000000000"

if [ -z "$BASE" ] || [ -z "$HEAD" ] || [ "$HEAD" = "$ZERO" ]; then
  echo "object-scan: nothing to scan (empty range)."
  exit 0
fi

# New branch push (before == 0): fall back to the merge-base with the default branch.
if [ "$BASE" = "$ZERO" ]; then
  BASE="$(git merge-base "$HEAD" origin/HEAD 2>/dev/null || true)"
  if [ -z "$BASE" ] || [ "$BASE" = "$HEAD" ]; then
    echo "object-scan: no new objects relative to the default branch."
    exit 0
  fi
fi

if ! git rev-parse --verify --quiet "$BASE^{commit}" >/dev/null || ! git rev-parse --verify --quiet "$HEAD^{commit}" >/dev/null; then
  echo "object-scan: base or head commit not present locally; failing closed."
  exit 1
fi

VIDEO_EXTS=" mp4 m4v mov mkv webm avi wmv flv f4v mpg mpeg m2ts mts 3gp 3g2 ogv vob asf rm rmvb divx m3u8 weba "
AUDIO_EXTS=" mp3 wav flac aac m4a ogg oga opus wma aif aiff mid midi amr au "
ARCHIVE_EXTS=" zip 7z rar tar gz tgz bz2 xz zst lz4 cab iso dmg "

fail_count=0
warn_count=0
scanned=0

report_fail() { # path size reason
  echo "::error file=$1::object-scan FAIL: $3 (blob $2 bytes, path: $1)"
  echo "FAIL  path=$1 size=$2 reason=$3"
  fail_count=$((fail_count + 1))
}
report_warn() { # path size
  echo "::warning file=$1::object-scan WARN: non-text blob over 2 MiB ($2 bytes, path: $1)"
  echo "WARN  path=$1 size=$2 reason=non-text blob over 2 MiB"
  warn_count=$((warn_count + 1))
}

# Collect new objects with their paths (rev-list --objects prints each object
# once, with a representative path), then batch-check type+size.
obj_list="$(git rev-list --objects "$BASE..$HEAD" 2>/dev/null || true)"
if [ -z "$obj_list" ]; then
  echo "object-scan: range $BASE..$HEAD introduces no objects."
  exit 0
fi

declare -A PATH_OF SIZE_OF
while read -r sha path; do
  [ -n "$sha" ] && PATH_OF["$sha"]="${path:-<no-path>}"
done <<< "$obj_list"

while read -r sha type size; do
  [ "$type" = "blob" ] || continue
  SIZE_OF["$sha"]="$size"
done < <(printf '%s\n' "${!PATH_OF[@]}" | git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize)' 2>/dev/null || true)

for sha in "${!SIZE_OF[@]}"; do
  size="${SIZE_OF[$sha]}"
  path="${PATH_OF[$sha]:-<no-path>}"
  scanned=$((scanned + 1))

  # Hard size cap applies to every blob, whatever its type.
  if [ "$size" -gt "$HARD_LIMIT" ]; then
    report_fail "$path" "$size" "blob over 5 MiB hard cap"
    continue
  fi

  # Extension (case-insensitive), taken from the blob's path.
  base_name="${path##*/}"
  ext=""
  case "$base_name" in
    *.*) ext="$(printf '%s' "${base_name##*.}" | tr '[:upper:]' '[:lower:]')" ;;
  esac

  # First bytes (hex tokens) for magic-byte and binary checks.
  hexbytes="$(git cat-file blob "$sha" 2>/dev/null | head -c 564 | od -An -v -tx1 | tr -s ' ' '\n' | grep -v '^$' || true)"
  b=()
  while read -r tok; do b+=("$tok"); done <<< "$hexbytes"
  byte() { printf '%s' "${b[$1]:-}"; }
  magic=""
  if [ "$(byte 4)$(byte 5)$(byte 6)$(byte 7)" = "66747970" ]; then magic="ftyp media container (MP4/MOV/3GP/M4A)"; fi
  if [ -z "$magic" ] && { [ "$(byte 4)$(byte 5)$(byte 6)$(byte 7)" = "6d6f6f76" ] || [ "$(byte 4)$(byte 5)$(byte 6)$(byte 7)" = "6d646174" ]; }; then magic="QuickTime moov/mdat"; fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)$(byte 3)" = "1a45dfa3" ]; then magic="EBML (MKV/WebM)"; fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)$(byte 3)" = "52494646" ]; then
    case "$(byte 8)$(byte 9)$(byte 10)$(byte 11)" in
      41564920) magic="RIFF AVI video" ;;
      57415645) magic="RIFF WAVE audio" ;;
    esac
  fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)" = "464c56" ]; then magic="FLV video"; fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)$(byte 3)" = "000001ba" ]; then magic="MPEG program stream"; fi
  if [ -z "$magic" ] && [ "$(byte 0)" = "47" ]; then
    if [ "$size" -ge 376 ] && [ "$(byte 188)" = "47" ] && [ "$(byte 376)" = "47" ]; then magic="MPEG-TS (HLS segment)"; fi
    if [ -z "$magic" ] && [ "$size" -ge 188 ] && [ $((size % 188)) -eq 0 ] && [ "$(byte 188)" = "47" ]; then magic="MPEG-TS (HLS segment)"; fi
    if [ -z "$magic" ] && [ "$size" -eq 188 ]; then magic="MPEG-TS (HLS segment)"; fi
  fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)$(byte 3)$(byte 4)$(byte 5)$(byte 6)$(byte 7)" = "3026b2758e66cf11" ]; then magic="ASF/WMV"; fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)$(byte 3)" = "4f676753" ]; then magic="Ogg container (audio/video)"; fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)$(byte 3)" = "2e524d46" ]; then magic="RealMedia"; fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)" = "494433" ]; then magic="MP3 (ID3)"; fi
  if [ -z "$magic" ] && [ "$(byte 0)" = "ff" ]; then
    case "$(byte 1)" in
      fb|f3|f2) magic="MP3 frame sync" ;;
      f1|f9) magic="AAC (ADTS)" ;;
    esac
  fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)$(byte 3)" = "664c6143" ]; then magic="FLAC audio"; fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)$(byte 3)" = "504b0304" ]; then magic="ZIP archive"; fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)$(byte 3)$(byte 4)$(byte 5)" = "377abcaf271c" ]; then magic="7z archive"; fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)$(byte 2)$(byte 3)" = "52617221" ]; then magic="RAR archive"; fi
  if [ -z "$magic" ] && [ "$(byte 0)$(byte 1)" = "1f8b" ]; then magic="gzip archive"; fi

  # Binary? (NUL byte within the first 8 KiB — git's own text heuristic.)
  # Count-based check: testing the pipeline's exit status directly is unsafe
  # under pipefail (head closing the pipe SIGPIPEs cat-file).
  is_binary=0
  nul_count="$(git cat-file blob "$sha" 2>/dev/null | head -c 8192 | od -An -v -tx1 | tr -s ' ' '\n' | grep -c -x '00' || true)"
  if [ "${nul_count:-0}" -gt 0 ] 2>/dev/null; then
    is_binary=1
  fi

  # Extension verdicts.
  if [ -n "$ext" ]; then
    if printf '%s' "$VIDEO_EXTS" | grep -q " $ext "; then
      if [ "$ext" = "ts" ] && [ -z "$magic" ] && [ "$is_binary" -eq 0 ]; then
        : # plain-text .ts (TypeScript) — not an HLS segment
      else
        report_fail "$path" "$size" "media extension .$ext"
        continue
      fi
    elif printf '%s' "$AUDIO_EXTS" | grep -q " $ext "; then
      report_fail "$path" "$size" "audio extension .$ext"
      continue
    elif printf '%s' "$ARCHIVE_EXTS" | grep -q " $ext "; then
      report_fail "$path" "$size" "archive extension .$ext"
      continue
    fi
  fi

  # Magic-byte verdict (catches renamed media/archives).
  if [ -n "$magic" ]; then
    report_fail "$path" "$size" "magic bytes: $magic"
    continue
  fi

  # Warning: non-text blob over 2 MiB.
  if [ "$size" -gt "$WARN_LIMIT" ] && [ "$is_binary" -eq 1 ]; then
    report_warn "$path" "$size"
  fi
done

echo "object-scan: scanned $scanned new blob(s) in $BASE..$HEAD — $fail_count failure(s), $warn_count warning(s)."
if [ "$fail_count" -gt 0 ]; then
  exit 1
fi
exit 0
