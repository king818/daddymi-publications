#!/usr/bin/env python3
"""Object scan gate — Q-A of the signed video-storage architecture (2026-11-23).

Scans every git object newly introduced in a push / pull-request range,
including blobs that were added and later deleted within the range
(`git rev-list --objects base..head` walks every commit in the range, so
intermediate blobs are enumerated even if the final tree no longer has them).

FAIL (job exits 1) on any introduced blob that is:
  * at a path with a media extension (video / audio / HLS), case-insensitive;
  * carrying media magic bytes (a renamed video still fails);
  * larger than 5 MiB.

WARN (GitHub annotation only, job still passes) on:
  * non-text blobs larger than 2 MiB.

Stdlib only, deterministic. Range inputs come from the workflow via env:
  EVENT_NAME, PUSH_BEFORE, PUSH_AFTER, PR_BASE, PR_HEAD, REF_NAME,
  DEFAULT_BRANCH.
"""

import os
import subprocess
import sys

FAIL_SIZE = 5 * 1024 * 1024  # 5 MiB hard limit per blob
WARN_SIZE = 2 * 1024 * 1024  # 2 MiB warning threshold for non-text blobs
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

MEDIA_EXTS = {
    # video
    "mp4", "m4v", "mov", "mkv", "webm", "avi", "mpg", "mpeg", "m2v", "wmv",
    "flv", "f4v", "ts", "m2ts", "mts", "3gp", "3g2", "ogv", "vob", "rm",
    "rmvb", "asf", "divx",
    # audio
    "mp3", "wav", "flac", "aac", "m4a", "ogg", "oga", "opus", "wma", "aif",
    "aiff", "mid", "midi", "amr", "ape",
    # HLS / streaming playlists (segments are .ts above)
    "m3u8", "m3u",
}

ASF_HEADER = bytes([
    0x30, 0x26, 0xB2, 0x75, 0x8E, 0x66, 0xCF, 0x11,
    0xA6, 0xD9, 0x00, 0xAA, 0x00, 0x62, 0xCE, 0x6C,
])
AUDIO_SYNC_SECOND = {0xF1, 0xF9, 0xFB, 0xFA, 0xF3, 0xF2, 0xE3, 0xE2}


def git(*args, inp=None):
    return subprocess.run(["git", *args], input=inp, capture_output=True)


def object_exists(sha):
    return bool(sha) and git("cat-file", "-e", sha).returncode == 0


def resolve_range():
    event = os.environ.get("EVENT_NAME", "")
    if event == "pull_request":
        return os.environ["PR_BASE"], os.environ["PR_HEAD"]
    before = os.environ.get("PUSH_BEFORE", "")
    after = os.environ.get("PUSH_AFTER", "")
    if object_exists(before):
        return before, after
    # New ref or rewritten history: scan what this ref adds over the
    # default branch; for the default branch itself, diff the head
    # commit against its first parent (or the empty tree).
    default = os.environ.get("DEFAULT_BRANCH", "main")
    ref = os.environ.get("REF_NAME", "")
    if ref and ref != default:
        mb = git("merge-base", "origin/" + default, after)
        if mb.returncode == 0:
            return mb.stdout.decode().strip(), after
    parent = git("rev-parse", after + "^")
    if parent.returncode == 0:
        return parent.stdout.decode().strip(), after
    return EMPTY_TREE, after


def introduced_objects(base, head):
    out = git("rev-list", "--objects", base + ".." + head)
    if out.returncode != 0:
        print("::error::git rev-list failed for range "
              + base + ".." + head + ": "
              + out.stderr.decode("utf-8", "replace").strip())
        sys.exit(2)
    objs = {}
    for line in out.stdout.decode("utf-8", "replace").splitlines():
        parts = line.split(" ", 1)
        sha = parts[0]
        path = parts[1] if len(parts) > 1 else ""
        if sha not in objs or (not objs[sha] and path):
            objs[sha] = path
    return objs


def batch_check(shas):
    fmt = "%(objectname) %(objecttype) %(objectsize)"
    p = git("cat-file", "--batch-check=" + fmt,
            inp=("\n".join(shas) + "\n").encode())
    info = {}
    for line in p.stdout.decode().splitlines():
        parts = line.split(" ")
        if len(parts) == 3 and parts[1] in ("blob", "tree", "commit", "tag"):
            info[parts[0]] = (parts[1], int(parts[2]))
    return info


def head_bytes(sha, n):
    p = git("cat-file", "blob", sha)
    return p.stdout[:n]


def media_magic(b):
    if len(b) >= 8 and b[4:8] == b"ftyp":
        return "ISO-BMFF ftyp box (MP4/MOV/3GP/M4A family)"
    if b[:4] == bytes([0x1A, 0x45, 0xDF, 0xA3]):
        return "EBML header (Matroska/WebM)"
    if b[:4] == b"RIFF" and len(b) >= 12 and b[8:12] in (b"AVI ", b"WAVE"):
        return "RIFF container (AVI/WAV)"
    if b[:3] == b"FLV":
        return "FLV header"
    if b[:16] == ASF_HEADER:
        return "ASF header (WMV/WMA)"
    if b[:4] == b".RMF":
        return "RealMedia header"
    if b[:4] == b"OggS":
        return "Ogg container (audio/video)"
    if b[:4] == b"fLaC":
        return "FLAC header"
    if b[:3] == b"ID3":
        return "MP3 ID3 tag"
    if len(b) >= 2 and b[0] == 0xFF and b[1] in AUDIO_SYNC_SECOND:
        return "MPEG-audio / ADTS sync header"
    if len(b) >= 377 and b[0] == 0x47 and b[188] == 0x47 and b[376] == 0x47:
        return "MPEG-TS sync pattern"
    if b[:4] == bytes([0x00, 0x00, 0x01, 0xBA]):
        return "MPEG-PS pack header"
    if b[:4] == b"FORM" and len(b) >= 12 and b[8:12] in (b"AIFF", b"AIFC"):
        return "AIFF header"
    return None


def extension_of(path):
    base = path.rsplit("/", 1)[-1]
    if "." not in base:
        return ""
    return base.rsplit(".", 1)[-1].lower()


def main():
    base, head = resolve_range()
    print("Object scan range: " + base + ".." + head)
    objs = introduced_objects(base, head)
    info = batch_check(list(objs.keys()))
    failures = []
    warnings = []
    n_blobs = 0
    for sha, path in sorted(objs.items(), key=lambda kv: kv[1]):
        entry = info.get(sha)
        if entry is None or entry[0] != "blob":
            continue
        n_blobs += 1
        size = entry[1]
        shown = path if path else "(path unknown)"
        reasons = []
        ext = extension_of(path)
        if ext in MEDIA_EXTS:
            reasons.append("media file extension ." + ext)
        if size > FAIL_SIZE:
            reasons.append("blob size %d bytes exceeds the 5 MiB limit" % size)
        head_small = head_bytes(sha, 512)
        magic = media_magic(head_small)
        if magic:
            reasons.append("media magic bytes: " + magic)
        if reasons:
            failures.append((shown, sha, size, reasons))
        elif size > WARN_SIZE:
            sample = head_bytes(sha, 8192)
            if b"\x00" in sample:
                warnings.append((shown, sha, size))
    print("Scanned %d introduced objects, %d blobs."
          % (len(objs), n_blobs))
    for shown, sha, size in warnings:
        print("::warning::Non-text blob over 2 MiB (allowed, annotated): "
              "%s (%s, %d bytes)" % (shown, sha[:12], size))
    if failures:
        print("")
        print("OBJECT SCAN FAILED — %d offending blob(s):" % len(failures))
        for shown, sha, size, reasons in failures:
            line = "%s (%s, %d bytes): %s" % (
                shown, sha[:12], size, "; ".join(reasons))
            print("  - " + line)
            print("::error::" + line)
        print("")
        print("Git holds no media and no blob over 5 MiB "
              "(video-storage architecture Q-A, 2026-11-23). "
              "Keep masters in the A/B/C archive tier and delivery "
              "packages on OSS/YouTube; commit only references.")
        return 1
    print("Object scan passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
