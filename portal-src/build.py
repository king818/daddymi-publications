#!/usr/bin/env python3
"""Build the daddymi777.com portal pages from ONE content source.

Source : portal-src/content.json   (all trilingual strings live there)
Outputs: index.html          (zh-Hans — the site root page)
         zh-hant/index.html
         en/index.html
         portal.css          (the single visual layer, from
                              portal-src/portal.css — restyle there;
                              the page structure never changes)

The three versions are rendered from a single template + the single
content file, so they cannot drift apart. Re-run after editing
content.json:  python3 portal-src/build.py

ROOT SWITCH DONE 2026-11-09: the portal IS the root now; the old
publications index lives at /publications/ (owned by generate.py).
Link layout: per-page relative prefixes from content.json ("" for the
root page, "../" for the two language pages) resolve every asset and
section link from each page's own depth, on both the custom domain
and the github.io mirror.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TEMPLATE = """<!DOCTYPE html>
<html lang="%%HTML_LANG%%">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<meta name="description" content="%%TAGLINE%%">
<link rel="canonical" href="%%CANONICAL%%">
<link rel="alternate" hreflang="zh-Hans" href="https://daddymi777.com/">
<link rel="alternate" hreflang="zh-Hant" href="https://daddymi777.com/zh-hant/">
<link rel="alternate" hreflang="en" href="https://daddymi777.com/en/">
<link rel="alternate" hreflang="x-default" href="https://daddymi777.com/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="米老爸 Daddy Mi">
<meta property="og:title" content="%%TITLE%%">
<meta property="og:description" content="%%TAGLINE%%">
<meta property="og:url" content="%%CANONICAL%%">
<meta property="og:image" content="%%OG_IMAGE%%">
<meta property="og:image:width" content="%%OG_IMAGE_W%%">
<meta property="og:image:height" content="%%OG_IMAGE_H%%">
<meta property="og:locale" content="%%OG_LOCALE%%">
%%OG_LOCALE_ALTS%%
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%%TITLE%%">
<meta name="twitter:description" content="%%TAGLINE%%">
<meta name="twitter:image" content="%%OG_IMAGE%%">
<link rel="icon" type="image/png" sizes="32x32" href="%%PREFIX%%brand/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="%%PREFIX%%brand/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="%%PREFIX%%brand/apple-touch-icon.png">
<script>
/* Legacy-anchor rescue (joint recommendation §4): the old root index
   rendered series blocks without stable fragment ids, so any shared
   link carrying an unknown #fragment meant "the index". Send those to
   /publications/ with the fragment preserved. The portal's own
   section anchors (#listen, #subscribe, #works, #about) stay. */
(function () {
  var own = { '#listen': 1, '#subscribe': 1, '#works': 1, '#about': 1, '': 1 };
  var h = window.location.hash || '';
  if (!own[h]) { window.location.replace('%%PUBS_RESCUE%%' + h); }
})();
</script>
<link rel="stylesheet" href="%%PREFIX%%portal.css">
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <div class="brand">米老爸 Daddy Mi</div>
    <div class="langswitch">%%LANG_SWITCH%%</div>
  </div>
  <nav class="nav">
    <a href="%%GW_LINK%%">%%NAV_GW%%</a>
    <a href="%%MIXI_LINK%%">%%NAV_MIXI%%</a>
    <a href="%%PUBS_LINK%%">%%NAV_VIDEOS%%</a>
  </nav>

  <header>
    <img class="heromark" src="%%PREFIX%%brand/mark-transparent.png" alt="米老爸 Daddy Mi">
    %%BRANDLINE_BLOCK%%
    <p class="tagline">%%TAGLINE%%</p>
    <img class="heroimg" src="%%HERO_IMG%%" alt="%%HERO_IMG_ALT%%">
  </header>

  <section class="card listen" id="listen" style="margin-top:0">
    %%INSCR_STRIP%%
    <img src="%%COVER%%" alt="%%LISTEN_IMG_ALT%%">
    <div style="flex:1; min-width:0">
      <h2>%%LISTEN_H%%</h2>
      <p class="song">%%SONG_TITLE%%</p>
      <p class="by">%%SONG_BY%%</p>
      <audio controls preload="none" src="%%AUDIO%%"></audio>
      <p class="disclosure">%%AI_DISCLOSURE%%</p>
      <p class="songpage"><a href="%%DIANDENG_LINK%%">%%SONG_PAGE_LINK%%</a></p>
      <p class="likeprompt"><a href="#subscribe">%%LIKE_PROMPT%% ↓</a></p>
    </div>
  </section>

  <a class="explore" href="#works">%%EXPLORE_LINK%% ↓</a>

  <section class="band" id="subscribe">
    <h2>%%SUBSCRIBE_H%%</h2>
    <p>%%SUBSCRIBE_COPY%%</p>
    <!-- ============================================================
      EMAIL FORM — Buttondown embed-subscribe (joint recommendation
      §6): a pure-HTML form POST to a single host, no JavaScript.
      WIRED LIVE 2026-11-09 to the real Buttondown account
      (username "daddymi", newsletter "Daddy Mi"): the action is
      https://buttondown.com/api/emails/embed-subscribe/daddymi
      (portal-src/content.json -> site.buttondown_username; re-run
      portal-src/build.py after any change). Buttondown requires
      double opt-in by default, so a subscriber is only added after
      clicking the confirmation email. Mainland three-test
      (submission / confirmation delivery to QQ + 163 / unsubscribe
      reachability, joint rec. §6) is tracked in BUILD-LOG.
      ============================================================ -->
    <form class="subform" action="https://buttondown.com/api/emails/embed-subscribe/%%BUTTONDOWN_USERNAME%%" method="post">
      <label for="bd-email">%%EMAIL_LABEL%%</label>
      <input id="bd-email" type="email" name="email" required placeholder="%%EMAIL_PLACEHOLDER%%" autocomplete="email">
      <button type="submit">%%SUBSCRIBE_BUTTON%%</button>
    </form>
    <p class="formnote">%%FORM_PENDING%% <a href="mailto:%%SUPPORT_EMAIL%%">%%SUPPORT_EMAIL%%</a></p>
  </section>

  <section id="works">
    <h2>%%WORKS_H%%</h2>
    <div class="cards">
      <div class="card">
        <h3>%%CARD1_T%%</h3>
        <p>%%CARD1_D%%</p>
        <a href="%%GW_LINK%%">%%CARD1_LINK%%</a>
      </div>
      <div class="card">
        <h3>%%CARD2_T%%</h3>
        <p>%%CARD2_D%%</p>
        <a href="%%MIXI_LINK%%">%%CARD2_LINK%%</a>
      </div>
      <div class="card">
        <h3>%%CARD3_T%%</h3>
        <p>%%CARD3_D%%</p>
        <a href="%%PUBS_LINK%%">%%CARD3_LINK%%</a>
      </div>
    </div>
  </section>

  <section class="about" id="about">
    <h2>%%ABOUT_H%%</h2>
    <p>%%ABOUT_P%%</p>
    <p class="faith">%%ABOUT_FAITH%%</p>
  </section>

  <footer>
    <img class="footmark" src="%%PREFIX%%brand/mark-transparent.png" alt="">
    <div>%%FOOTER_SUPPORT%%：<a href="mailto:%%SUPPORT_EMAIL%%">%%SUPPORT_EMAIL%%</a></div>
    <div><a href="%%YT_CHANNEL%%" target="_blank" rel="noopener">%%YT_CHANNEL_LABEL%%</a></div>
    <div><a href="%%YT_MV%%" target="_blank" rel="noopener">%%YT_MV_LABEL%%</a></div>
    <div>%%FOOTER_PRIVACY%%</div>
    <div>© 2026 米老爸 Daddy Mi</div>
  </footer>
</div>
</body>
</html>
"""

ORDER = ["zh-hans", "zh-hant", "en"]

# Stylesheet C "Ink & Light" + Track A calligraphy (boss ruling
# 2026-11-09): on the Chinese views the hero brand line is the
# QC-passed calligraphy artwork (brand/calligraphy/brand-line{1,2}.png,
# indigo #1E2A38). Semantics/fallback (team review must-fix): the
# images carry alt="" and the real sentence lives in an sr-only span;
# a hidden serif text layer (.callig-text, Noto Serif 600 indigo)
# appears instead if an image fails to load (onerror -> .callig-failed).
# The English view keeps its brand line as elegant serif text. The
# song card carries the vertical inscription strip on the Chinese
# views only: role="img" + per-language aria-label on the container,
# alt="" on each glyph image.
BRANDLINE_ALT = {
    "zh-hans": ("以智慧启发人生", "以科技传递温暖"),
    "zh-hant": ("以智慧啟發人生", "以科技傳遞溫暖"),
}
INSCR_LABEL = {"zh-hans": "点灯的人", "zh-hant": "點燈的人"}
_ONERROR = "onerror=\"this.closest('.brand-art').classList.add('callig-failed')\""

def _brandline_block(page, prefix):
    code = page["html_lang"].lower()
    if code in BRANDLINE_ALT:
        alt1, alt2 = BRANDLINE_ALT[code]
        return ('<h1 class="brand-art">'
                '<span class="callig-text" aria-hidden="true"><span class="ct-line">%s</span><span class="ct-line">%s</span></span>'
                '<img class="callig-line1" src="%sbrand/calligraphy/brand-line1.png" alt="" %s>'
                '<img class="callig-line2" src="%sbrand/calligraphy/brand-line2.png" alt="" %s>'
                '<span class="sr-only">%s</span></h1>'
                % (alt1, alt2, prefix, _ONERROR, prefix, _ONERROR, page["brandline"]))
    return '<h1 class="brand-en">%s</h1>' % page["brandline"]

def _inscr_strip(page, prefix):
    code = page["html_lang"].lower()
    if code in INSCR_LABEL:
        imgs = "".join('<img src="%sbrand/calligraphy/inscr-%d.png" alt="">' % (prefix, i) for i in range(4))
        return '<div class="inscr-strip" role="img" aria-label="%s">%s</div>' % (INSCR_LABEL[code], imgs)
    return ""

def render(code, page, site, pages):
    prefix = page["prefix"]
    values = {
        "HTML_LANG": page["html_lang"],
        "TITLE": page["title"],
        "BRANDLINE_BLOCK": _brandline_block(page, prefix),
        "INSCR_STRIP": _inscr_strip(page, prefix),
        "TAGLINE": page["tagline"],
        "CANONICAL": page["canonical"],
        "OG_IMAGE": site["og_image"],
        "OG_IMAGE_W": str(site["og_image_w"]),
        "OG_IMAGE_H": str(site["og_image_h"]),
        "OG_LOCALE": page["og_locale"],
        "BRANDLINE": page["brandline"],
        "LISTEN_H": page["listen_h"],
        "SONG_TITLE": site["song_title"],
        "SONG_BY": page["song_by"],
        "AI_DISCLOSURE": page["ai_disclosure"],
        "SONG_PAGE_LINK": page["song_page_link"],
        "LIKE_PROMPT": page["like_prompt"],
        "EXPLORE_LINK": page["explore_link"],
        "SUBSCRIBE_H": page["subscribe_h"],
        "SUBSCRIBE_COPY": page["subscribe_copy"],
        "FORM_PENDING": page["form_pending"],
        "PREFIX": prefix,
        "PUBS_RESCUE": prefix + "publications/",
        "BUTTONDOWN_USERNAME": site["buttondown_username"],
        "EMAIL_LABEL": page["email_label"],
        "EMAIL_PLACEHOLDER": page["email_placeholder"],
        "SUBSCRIBE_BUTTON": page["subscribe_button"],
        "SUPPORT_EMAIL": site["support_email"],
        "WORKS_H": page["works_h"],
        "CARD1_T": page["card1_t"], "CARD1_D": page["card1_d"], "CARD1_LINK": page["card1_link"],
        "CARD2_T": page["card2_t"], "CARD2_D": page["card2_d"], "CARD2_LINK": page["card2_link"],
        "CARD3_T": page["card3_t"], "CARD3_D": page["card3_d"], "CARD3_LINK": page["card3_link"],
        "ABOUT_H": page["about_h"], "ABOUT_P": page["about_p"],
        "ABOUT_FAITH": page["about_faith"],
        "HERO_IMG": prefix + site["hero_image"],
        "HERO_IMG_ALT": page["hero_img_alt"],
        "FOOTER_SUPPORT": page["footer_support"],
        "FOOTER_PRIVACY": page["footer_privacy"],
        "YT_CHANNEL": site["youtube_channel"],
        "YT_MV": site["youtube_mv_playlist"],
        "YT_CHANNEL_LABEL": page["yt_channel"],
        "YT_MV_LABEL": page["yt_mv"],
        "NAV_GW": page["nav_gw"], "NAV_MIXI": page["nav_mixi"], "NAV_VIDEOS": page["nav_videos"],
        "LISTEN_IMG_ALT": page["listen_img_alt"],
        "COVER": prefix + site["cover_path"],
        "AUDIO": prefix + site["audio_path"],
        "GW_LINK": prefix + "gospel-wisdom/?lang=" + code,
        "MIXI_LINK": prefix + "gospel-wisdom/mixi/?lang=" + code,
        "DIANDENG_LINK": prefix + "gospel-wisdom/dian-deng/?lang=" + code,
        "PUBS_LINK": prefix + "publications/",
    }
    alts = [pages[c]["og_locale"] for c in ORDER if c != code]
    values["OG_LOCALE_ALTS"] = "\n".join(
        '<meta property="og:locale:alternate" content="%s">' % a for a in alts)
    # language switcher: current language as text, others as links (paths from content.json)
    parts = []
    for c in ORDER:
        label = page["switch_labels"][c]
        href = page["lang_switch"][c]
        if href is None:
            parts.append('<span class="cur" aria-current="true">%s</span>' % label)
        else:
            parts.append('<a href="%s">%s</a>' % (href, label))
    values["LANG_SWITCH"] = "".join(parts)
    html = TEMPLATE
    for k, v in values.items():
        html = html.replace("%%" + k + "%%", v)
    assert "%%" not in html, [t for t in html.split("%%")[1::2]]
    return html

def main():
    data = json.load(open(os.path.join(HERE, "content.json")))
    site, pages = data["site"], data["pages"]
    for code in ORDER:
        page = pages[code]
        html = render(code, page, site, pages)
        out = os.path.join(ROOT, page["out"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote %-28s %6d bytes" % (page["out"], len(html.encode("utf-8"))))
    # single visual layer: portal-src/portal.css -> site-root portal.css
    css = open(os.path.join(HERE, "portal.css"), encoding="utf-8").read()
    with open(os.path.join(ROOT, "portal.css"), "w", encoding="utf-8") as f:
        f.write(css)
    print("wrote %-28s %6d bytes" % ("portal.css", len(css.encode("utf-8"))))

if __name__ == "__main__":
    main()
