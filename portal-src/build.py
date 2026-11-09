#!/usr/bin/env python3
"""Build the daddymi777.com portal pages from ONE content source.

Source : portal-src/content.json   (all trilingual strings live there)
Outputs: index.html          (zh-Hans — the site root page)
         zh-hant/index.html
         en/index.html

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
<style>
  * { box-sizing: border-box; }
  body { margin: 0; color: #3b3125;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "PingFang TC",
      "Microsoft YaHei", "Noto Sans CJK SC", "Noto Sans CJK TC", system-ui, sans-serif;
    background:
      radial-gradient(900px 480px at 50% -120px, rgba(255, 214, 140, .55), rgba(255, 214, 140, 0) 70%),
      linear-gradient(180deg, #fdf9ef 0%, #faf3e2 55%, #f6eeda 100%);
    min-height: 100vh; }
  a { color: #8a6d1f; }
  .wrap { max-width: 960px; margin: 0 auto; padding: 0 20px 48px; }
  .topbar { display: flex; justify-content: space-between; align-items: baseline;
    gap: 12px; flex-wrap: wrap; padding: 18px 0 4px; }
  .brand { font-weight: 700; font-size: 19px; letter-spacing: .02em; }
  .langswitch { font-size: 14px; }
  .langswitch a, .langswitch .cur { margin-left: 12px; text-decoration: none; }
  .langswitch .cur { font-weight: 700; color: #3b3125; }
  .nav { padding: 6px 0 2px; font-size: 15px; }
  .nav a { margin-right: 16px; text-decoration: none; }
  .heromark { display: block; height: 92px; width: auto; margin: 30px auto 4px; }
  h1 { font-family: Georgia, "Songti SC", "STSong", "Noto Serif CJK SC", serif;
    font-size: clamp(28px, 5.2vw, 44px); line-height: 1.25; text-align: center;
    margin: 14px 0 12px; font-weight: 700; }
  .tagline { text-align: center; color: #6b5b3e; font-size: 17px; line-height: 1.6;
    margin: 0 auto 28px; max-width: 660px; }
  h2 { font-size: 21px; margin: 0 0 10px; }
  .card { background: rgba(255, 255, 255, .78); border: 1px solid #e7dcc3;
    border-radius: 14px; padding: 20px; }
  .listen { display: flex; gap: 18px; align-items: flex-start; }
  .listen img { width: 108px; height: 144px; object-fit: cover; border-radius: 10px; flex: none; }
  .listen .song { font-size: 19px; font-weight: 700; margin: 2px 0 4px; }
  .listen .by { color: #6b5b3e; font-size: 14px; margin: 0 0 6px; }
  .listen audio { width: 100%; margin: 8px 0; }
  .disclosure { font-size: 13px; color: #6b5b3e; line-height: 1.55; margin: 6px 0; }
  .likeprompt { font-size: 15px; margin: 8px 0 0; }
  .songpage { font-size: 14px; }
  .explore { display: block; text-align: center; margin: 20px 0 2px; font-size: 16px;
    text-decoration: none; }
  .band { background: #fffdf6; border: 1px solid #e7dcc3; border-radius: 14px;
    padding: 22px; margin-top: 28px; }
  .band p { line-height: 1.65; margin: 6px 0; }
  .subform { display: flex; gap: 10px; flex-wrap: wrap; margin: 14px 0 4px; }
  .subform label { flex: 0 0 100%; font-size: 14px; color: #6b5b3e; }
  .subform input { flex: 1 1 240px; padding: 11px 14px; font-size: 16px;
    border: 1px solid #d8cba6; border-radius: 10px; background: #fff; color: #3b3125; }
  .subform button { padding: 11px 26px; font-size: 16px; font-weight: 700;
    color: #fff; background: #a8842c; border: 1px solid #a8842c; border-radius: 10px;
    cursor: pointer; }
  .subform button:hover { background: #8a6d1f; }
  .formnote { font-size: 14px; color: #6b5b3e; }
  .footmark { display: block; height: 28px; width: auto; margin: 0 0 6px; }
  .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 14px; }
  .cards .card p { line-height: 1.6; color: #55482f; margin: 6px 0 12px; }
  .cards h3 { margin: 0 0 6px; font-size: 18px; }
  section { margin-top: 34px; }
  .about p { line-height: 1.7; color: #55482f; max-width: 720px; }
  footer { margin-top: 44px; border-top: 1px solid #e7dcc3; padding-top: 18px;
    font-size: 14px; color: #6b5b3e; line-height: 1.9; }
  footer a { text-decoration: none; }
  @media (max-width: 720px) {
    .cards { grid-template-columns: 1fr; }
    .listen { flex-direction: column; }
    .listen img { width: 96px; height: 128px; }
  }
</style>
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
    <h1>%%BRANDLINE%%</h1>
    <p class="tagline">%%TAGLINE%%</p>
  </header>

  <section class="card listen" id="listen" style="margin-top:0">
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

def render(code, page, site, pages):
    prefix = page["prefix"]
    values = {
        "HTML_LANG": page["html_lang"],
        "TITLE": page["title"],
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

if __name__ == "__main__":
    main()
