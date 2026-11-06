# Generates site/guide/*, site/sitemap.xml and site/favicon.svg. Run: python3 tools/build_guides.py
import json, os, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
BASE = 'https://stwater20.github.io/car/'
DATE = '2026-11-06'
MAKER = {"@type": "Organization", "name": "sectools.tw", "url": "https://sectools.tw/"}

CSS = """
:root{--ink:#0b0c1c;--ink-2:#14162b;--line:rgba(255,248,242,.14);--paper:#fff8f2;--mute:rgba(255,248,242,.72);--go:#2fe08a;--hot:#ff2e6a;--sky:#3fe0ff;--warn:#ffc23a;
--f-display:'Barlow Condensed','Noto Sans TC','Arial Narrow',sans-serif;--f-body:'Noto Sans TC','PingFang TC','Microsoft JhengHei',sans-serif;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--ink);color:var(--paper);font-family:var(--f-body);font-size:17px;line-height:1.85;-webkit-font-smoothing:antialiased}
a{color:var(--sky)}
.wrap{max-width:780px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
header.top{border-bottom:1px solid var(--line);padding-block:14px}
header.top .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;font-weight:900;font-size:19px;text-decoration:none;color:var(--paper)}
.brand i{font-family:var(--f-display);font-style:normal;font-weight:900;background:var(--sky);color:var(--ink);width:30px;height:30px;display:grid;place-items:center;font-size:20px;border-radius:7px}
nav.links{display:flex;gap:16px;font-size:15px;font-weight:700;flex-wrap:wrap}
nav.links a{color:var(--mute);text-decoration:none}
nav.links a:hover{color:var(--paper)}
.crumbs{font-size:14px;color:var(--mute);margin-top:22px}
.crumbs a{color:var(--mute)}
h1{font-size:clamp(30px,5.4vw,44px);line-height:1.25;margin:10px 0 8px;font-weight:900;text-wrap:balance}
.lede{font-size:18px;color:rgba(255,248,242,.9);margin:0 0 6px}
.meta{font-size:14px;color:var(--mute);margin-bottom:22px}
.meta a{color:var(--mute)}
h2{font-size:clamp(23px,3.6vw,28px);margin:40px 0 10px;font-weight:900;line-height:1.35;text-wrap:balance}
h3{font-size:20px;margin:24px 0 6px;font-weight:900}
ol.steps{counter-reset:s;list-style:none;padding:0;margin:14px 0}
ol.steps li{counter-increment:s;position:relative;padding:10px 0 10px 52px;border-top:1px solid var(--line)}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:10px;width:36px;height:36px;border-radius:50%;background:var(--go);color:var(--ink);font-family:var(--f-display);font-weight:900;font-size:20px;display:grid;place-items:center}
ol.steps b{color:var(--paper)}
ul{padding-left:1.2em}
li{margin:4px 0}
.callout{border-left:4px solid var(--warn);background:rgba(255,194,58,.08);padding:12px 16px;margin:18px 0;font-size:16px}
.cta{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0}
.btn{display:inline-flex;align-items:center;font-weight:900;font-size:18px;text-decoration:none;padding:13px 24px;background:var(--go);color:var(--ink);border-radius:2px;min-height:48px}
.btn.ghost{background:none;border:2px solid var(--line);color:var(--paper)}
.btn:focus-visible{outline:3px solid var(--sky);outline-offset:3px}
figure{margin:20px 0;background:var(--ink-2);padding:14px;border:1px solid var(--line)}
figure svg{width:100%;height:auto;display:block}
figcaption{font-size:14px;color:var(--mute);margin-top:8px}
.table-wrap{overflow-x:auto;border:1px solid var(--line);margin:14px 0}
table{border-collapse:collapse;width:100%;min-width:480px;font-size:16px}
th,td{text-align:left;padding:10px 14px;border-bottom:1px solid var(--line);vertical-align:top}
thead th{background:var(--ink-2);font-size:14px;color:var(--mute)}
td.pts{font-family:var(--f-display);font-weight:900;color:#ff8aa8;white-space:nowrap}
details{border-top:1px solid var(--line);padding:14px 0}
details:last-of-type{border-bottom:1px solid var(--line)}
summary{cursor:pointer;font-weight:800;font-size:18px}
details p{margin:8px 0 0;color:var(--mute)}
.related{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:14px 0}
.related a{display:block;padding:14px;border:1px solid var(--line);text-decoration:none;color:var(--paper);font-weight:800;line-height:1.4}
.related a span{display:block;font-weight:500;font-size:14px;color:var(--mute);margin-top:4px}
.related a:hover{border-color:var(--go)}
footer{margin-top:56px;border-top:1px solid var(--line);padding-block:26px calc(env(safe-area-inset-bottom,0px) + 30px);font-size:15px;color:var(--mute)}
footer .maker a{font-weight:800}
@media (max-width:620px){.related{grid-template-columns:1fr}}
"""

def page(slug, title, h1, desc, lede, body, faqs, related, keywords, crumbs_name):
    url = BASE + 'guide/' + (slug + '/' if slug else '')
    ld = [
      {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc, "inLanguage": "zh-Hant-TW",
       "datePublished": DATE, "dateModified": DATE, "author": MAKER, "publisher": MAKER, "mainEntityOfPage": url,
       "image": BASE + "assets/nightmarket.jpg", "keywords": ", ".join(keywords)},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "停好停滿", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "教學", "item": BASE + "guide/"}] + ([{"@type": "ListItem", "position": 3, "name": crumbs_name, "item": url}] if slug else [])},
    ]
    if faqs:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    faq_html = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faqs)
    rel_html = ''.join(f'<a href="../{s}/">{t}<span>{d}</span></a>' for s, t, d in related)
    crumbs = f'<a href="../../">停好停滿</a> › <a href="../">教學</a> › {crumbs_name}' if slug else '<a href="../">停好停滿</a> › 教學'
    up = '../../' if slug else '../'
    return f"""<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="author" content="sectools.tw">
<meta name="theme-color" content="#0b0c1c">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:locale" content="zh_TW">
<meta property="og:site_name" content="停好停滿 Park Formosa">
<meta property="og:title" content="{html.escape(h1)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/nightmarket.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@800;900&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
{''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)}
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="{up}"><i>P</i>停好停滿</a><nav class="links" aria-label="教學導覽"><a href="{up}guide/reverse-parking/">倒車入庫</a><a href="{up}guide/parallel-parking/">路邊停車</a><a href="{up}guide/driving-test-2026/">場考扣分</a><a href="{up}play/">開始玩</a></nav></div></header>
<main class="wrap">
<div class="crumbs">{crumbs}</div>
<h1>{h1}</h1>
<p class="lede">{lede}</p>
<p class="meta">更新：{DATE}・由 <a href="https://sectools.tw/" target="_blank" rel="noopener author">sectools.tw</a> 製作與維護</p>
{body}
{'<h2>常見問題</h2>' + faq_html if faqs else ''}
{'<h2>延伸閱讀</h2><div class="related">' + rel_html + '</div>' if related else ''}
</main>
<footer><div class="wrap"><p class="maker">停好停滿（Park Formosa）由 <a href="https://sectools.tw/" target="_blank" rel="noopener author">sectools.tw</a> 製作與維護。</p><p>教學內容為一般駕駛技巧整理，不同車型、座椅位置和考場的參考點都不一樣，請以駕訓班教練指導和報考監理站公告為準。遊戲只能幫你熟悉步驟，不能取代實車練習。</p></div></footer>
</body>
</html>
"""

def cta(primary, label, more=()):
    s = f'<div class="cta"><a class="btn" href="../../play/#{primary}">{label} →</a>'
    for h, t in more: s += f'<a class="btn ghost" href="../../play/#{h}">{t}</a>'
    return s + '</div>'

# ---------- diagrams (inline SVG, drawn to the same proportions as the game) ----------
SVG_BAY = """<svg viewBox="0 0 640 420" role="img" aria-labelledby="t1"><title id="t1">倒車入庫路線示意：車子先開過車庫，再方向盤打到底倒進去</title>
<rect width="640" height="420" fill="#14162b"/>
<path d="M0 300 H640 M0 170 H240 M400 170 H640" stroke="#f2b531" stroke-width="6"/>
<path d="M240 170 V20 H400 V170" fill="rgba(47,224,138,.18)" stroke="#f2b531" stroke-width="6"/>
<text x="320" y="62" fill="#2fe08a" font-size="34" font-weight="900" text-anchor="middle" font-family="sans-serif">車庫</text>
<path d="M470 236 C 380 236, 320 210, 320 160 L320 90" fill="none" stroke="#ffc23a" stroke-width="6" stroke-dasharray="14 10"/>
<polygon points="320,76 306,104 334,104" fill="#ffc23a"/>
<rect x="450" y="206" width="170" height="62" rx="14" fill="#3fe0ff"/><text x="535" y="248" font-size="30" font-weight="900" text-anchor="middle" fill="#0b0c1c" font-family="sans-serif">①停這裡</text>
<text x="20" y="250" fill="#fff8f2" font-size="30" font-weight="800" font-family="sans-serif">②打到底倒車</text>
<text x="20" y="130" fill="#fff8f2" font-size="30" font-weight="800" font-family="sans-serif">③正了就回正</text>
<text x="420" y="130" fill="#fff8f2" font-size="30" font-weight="800" font-family="sans-serif">④直退到底</text>
<text x="320" y="370" fill="rgba(255,248,242,.7)" font-size="26" text-anchor="middle" font-family="sans-serif">← 從左邊開過來</text>
</svg>"""
SVG_PAR = """<svg viewBox="0 0 640 400" role="img" aria-labelledby="t2"><title id="t2">路邊停車路線示意：與前方標竿並排後，右打倒車，45 度回正，再左打擺正</title>
<rect width="640" height="400" fill="#14162b"/>
<rect x="0" y="320" width="640" height="80" fill="#5c5852"/><path d="M0 320 H640" stroke="#d8352a" stroke-width="8"/>
<rect x="150" y="236" width="290" height="80" fill="rgba(47,224,138,.18)" stroke="#f2b531" stroke-width="5"/>
<circle cx="150" cy="236" r="9" fill="#ff2e6a"/><circle cx="440" cy="236" r="9" fill="#ff2e6a"/>
<path d="M450 150 C 390 150, 370 180, 330 220 L 300 250 C 270 275, 230 278, 190 278" fill="none" stroke="#ffc23a" stroke-width="6" stroke-dasharray="14 10"/>
<polygon points="176,278 204,264 204,292" fill="#ffc23a"/>
<rect x="450" y="118" width="170" height="62" rx="14" fill="#3fe0ff"/><text x="535" y="160" font-size="30" font-weight="900" text-anchor="middle" fill="#0b0c1c" font-family="sans-serif">①並排停</text>
<text x="20" y="60" fill="#fff8f2" font-size="30" font-weight="800" font-family="sans-serif">②右打到底倒車</text>
<text x="20" y="110" fill="#fff8f2" font-size="30" font-weight="800" font-family="sans-serif">③約 45° 回正</text>
<text x="20" y="160" fill="#fff8f2" font-size="30" font-weight="800" font-family="sans-serif">④左打到底擺正</text>
<text x="320" y="372" fill="rgba(255,255,255,.8)" font-size="26" text-anchor="middle" font-family="sans-serif">人行道・路緣</text>
</svg>"""
SVG_S = """<svg viewBox="0 0 640 360" role="img" aria-labelledby="t3"><title id="t3">S 型曲線示意：前進時車頭貼外側線走，後退時看照後鏡讓後輪在線內</title>
<rect width="640" height="360" fill="#14162b"/>
<path d="M90 330 C 90 150, 300 150, 320 180 S 550 210, 550 50" fill="none" stroke="#f2b531" stroke-width="78"/>
<path d="M90 330 C 90 150, 300 150, 320 180 S 550 210, 550 50" fill="none" stroke="#3a3a42" stroke-width="66"/>
<path d="M90 330 C 90 150, 300 150, 320 180 S 550 210, 550 50" fill="none" stroke="#2fe08a" stroke-width="5" stroke-dasharray="14 10"/>
<text x="20" y="44" fill="#fff8f2" font-size="28" font-weight="800" font-family="sans-serif">左彎：車頭貼右（外）側</text>
<text x="620" y="330" fill="#fff8f2" font-size="28" font-weight="800" font-family="sans-serif" text-anchor="end">右彎：車頭貼左（外）側</text>
</svg>"""

TEST_TABLE = """<div class="table-wrap"><table><thead><tr><th>項目</th><th>常見扣分</th><th>扣分</th></tr></thead><tbody>
<tr><td>起駛</td><td>未繫安全帶</td><td class="pts">−32</td></tr>
<tr><td>起駛</td><td>起駛前未依規定顯示方向燈</td><td class="pts">−32</td></tr>
<tr><td>起駛／環場（2026 新制）</td><td>起步、打方向燈前未轉頭查看照後鏡與死角</td><td class="pts">−32</td></tr>
<tr><td>行人穿越道（2026 新制）</td><td>無號誌路口未減速、未停讓行人</td><td class="pts">−32</td></tr>
<tr><td>行人穿越道</td><td>停車時前懸超越停止線</td><td class="pts">−32</td></tr>
<tr><td>鐵路平交道</td><td>不停車察看、闖越、前輪超越停止線</td><td class="pts">−32</td></tr>
<tr><td>倒車入庫</td><td>車輪壓線、未停入規定範圍</td><td class="pts">−16</td></tr>
<tr><td>平行路邊停車</td><td>車輪壓線、未停入規定範圍</td><td class="pts">−16</td></tr>
<tr><td>上坡起步</td><td>車輪壓線；上坡倒退 15 公分以上（連續扣分）</td><td class="pts">−16</td></tr>
<tr><td>曲線進退</td><td>前進時車輪壓線</td><td class="pts">−32</td></tr>
<tr><td>曲線進退</td><td>普小後退壓線不扣分，但往前修正每次</td><td class="pts">−8</td></tr>
<tr><td>多數項目</td><td>中途熄火（連續扣分）或停車</td><td class="pts">−8</td></tr>
</tbody></table></div>"""

GUIDES = {}
GUIDES['reverse-parking'] = dict(
  title='倒車入庫技巧與口訣：5 步驟圖解，新手不壓線｜停好停滿',
  h1='倒車入庫技巧與口訣：5 個步驟一次停進去',
  desc='倒車入庫怎麼停才不會壓線？從停車點、方向盤打到底的時機、什麼時候回正，到場考壓線扣 16 分的規則，用圖解一次講清楚，還能直接在網頁遊戲裡免費練習。',
  lede='倒車入庫是汽車場考必考、也是日常最常用的停車方式。重點只有三個：停車點要對、方向盤要一次打到底、車身正了就回正。',
  crumb='倒車入庫技巧', kw=['倒車入庫', '倒車入庫技巧', '倒車入庫口訣', '倒車入庫 方向盤', '倒車入庫 壓線', '汽車場考'],
  body=f"""<figure>{SVG_BAY}<figcaption>示意圖，比例已簡化。實際參考點會因車型和座椅位置不同。</figcaption></figure>
<h2>倒車入庫 5 個步驟</h2>
<ol class="steps">
<li><b>先開過車庫再停。</b>車身和車庫口保持大約 50 公分到 1 公尺，往前開到車尾超過車庫一點點再停下。停得太早，倒車時車尾會切到庫角。</li>
<li><b>確認後方、打倒車檔。</b>停穩後轉頭看後方和兩側照後鏡，確定沒有人車再倒。</li>
<li><b>方向盤一次打到底，慢慢倒。</b>車子要往哪邊轉，方向盤就往哪邊打。速度越慢，越有時間看照後鏡修正。</li>
<li><b>車身快要和車庫平行時回正。</b>從照後鏡看兩側車庫線，兩邊和車身的距離差不多時，把方向盤轉回正中間。</li>
<li><b>直直退到底再停。</b>車尾快到庫底就停，不要撞到後方標線或障礙物。</li>
</ol>
<div class="callout">口訣整理：「過庫停、打到底、平行回正、直退到底」。不同駕訓班的參考點不一樣（車庫角、C 柱、照後鏡），請以教練教的為主。</div>
<h2>常見錯誤</h2>
<ul>
<li><b>太早打方向盤：</b>內側後輪會切過庫角，最常見的壓線原因。</li>
<li><b>忘了回正：</b>車身已經正了還繼續打，車尾就會甩到另一邊。</li>
<li><b>倒太快：</b>來不及看照後鏡修正。場考不計時，慢慢倒沒關係。</li>
</ul>
<h2>場考怎麼扣分</h2>
<p>依公路局小型車場考評分標準，倒車入庫<b>車輪壓線或未停入規定範圍扣 16 分</b>，中途熄火每次扣 8 分；入庫後駛出時，起駛前沒打方向燈或沒轉頭查看照後鏡、死角，各扣 32 分（2026 年 3 月 31 日起新制）。完整表格見 <a href="../driving-test-2026/">汽車駕照場考扣分標準</a>。</p>
<h2>在網頁遊戲裡練習</h2>
<p>「停好停滿」的倒車入庫關卡用真實的轉向幾何計算，太早打方向盤一樣會壓線。手機、電腦都能玩，不用下載。</p>
{cta('lv-bay', '練習倒車入庫', [('exam-bay', '場考模擬：倒車入庫'), ('lv-b3', '地下停車場倒車入位')])}""",
  faqs=[('倒車入庫什麼時候打方向盤？', '先往前開到車尾稍微超過車庫口再停，倒車時才把方向盤一次打到底。太早打，內側後輪容易切過庫角壓線。'),
        ('倒車入庫什麼時候回正？', '從兩側照後鏡看車身和左右兩條庫線的距離，差不多相等、車身和車庫平行時就回正，然後直直退到底。'),
        ('倒車入庫壓線扣幾分？', '依公路局小型車場考評分標準，倒車入庫車輪壓線或未停入規定範圍扣 16 分，中途熄火每次扣 8 分。70 分及格。'),
        ('可以在家練習倒車入庫嗎？', '可以用網頁遊戲「停好停滿」熟悉步驟和方向盤的方向感，但真正的參考點還是要在實車上跟教練確認。')],
  related=[('parallel-parking', '路邊停車技巧', '並排、45 度、擺正三步'), ('driving-test-2026', '場考扣分標準', '2026 新制一次看'), ('s-curve', 'S 型曲線進退', '前進與後退的看法'), ('parking-tips', '新手停車技巧', '斜角、迴轉、地下室')])

GUIDES['parallel-parking'] = dict(
  title='路邊停車技巧與口訣：並排、45 度、擺正三步驟圖解｜停好停滿',
  h1='路邊停車技巧與口訣：三個轉向點記住就會',
  desc='路邊停車（平行停車）怎麼停？與前車並排的距離、方向盤右打到底、約 45 度回正、再左打擺正，圖解每一步，加上場考壓線扣分規則和免費網頁練習。',
  lede='路邊停車（平行路邊停車）看起來難，其實只有三個轉向點：並排停好、右打到底倒到約 45 度、回正後左打擺正。',
  crumb='路邊停車技巧', kw=['路邊停車', '路邊停車技巧', '路邊停車口訣', '平行停車', '平行路邊停車', '路邊停車 新手'],
  body=f"""<figure>{SVG_PAR}<figcaption>示意圖：右側路邊停車。在台灣，路邊停車格通常在行車方向的右側。</figcaption></figure>
<h2>路邊停車 4 個步驟</h2>
<ol class="steps">
<li><b>和前方車子（或標竿）並排停好。</b>車身和它平行、間隔大約 50 公分到 1 公尺，車尾和它的車尾大約對齊。</li>
<li><b>方向盤右打到底，慢慢倒車。</b>倒車前先轉頭看後方和右後方，確認沒有機車、行人。</li>
<li><b>車身斜約 45 度時回正。</b>從左側照後鏡看到後方車子的車頭，或車身和路緣大約 45 度時，把方向盤轉回正中間，直直往後倒。</li>
<li><b>車頭快進格子時左打到底擺正。</b>車頭的右前角過了前車車尾，就把方向盤左打到底，車身會慢慢擺正貼近路緣。最後往前或往後微調置中。</li>
</ol>
<div class="callout">口訣整理：「並排、右打、45 度回正、左打擺正」。參考點會因車長和座椅位置不同，空間越小，第 3 步的角度要越大。</div>
<h2>常見錯誤</h2>
<ul>
<li><b>並排距離太遠：</b>倒進去之後車身離路緣太遠，要來回修正很多次。</li>
<li><b>左打太早：</b>車頭右前角還沒過前車車尾就左打，會擦到前車或前方標竿。</li>
<li><b>輪胎撞路緣：</b>擺正時倒太快。慢慢倒，右後輪靠近路緣就停。</li>
</ul>
<h2>場考怎麼扣分</h2>
<p>平行路邊停車<b>車輪壓線或未停入規定範圍扣 16 分</b>，熄火每次扣 8 分。停好駛出時，沒打左方向燈、沒轉頭看照後鏡和死角，各扣 32 分。詳見 <a href="../driving-test-2026/">場考扣分標準</a>。</p>
<h2>在網頁遊戲裡練習</h2>
<p>遊戲裡有駕訓班的路邊停車關卡，也有空間更小、旁邊停滿機車的夜市巷口路邊停車。</p>
{cta('lv-parallel', '練習路邊停車', [('lv-night', '夜市巷口路邊停車'), ('exam-parallel', '場考模擬：路邊停車')])}""",
  faqs=[('路邊停車方向盤怎麼打？', '並排後方向盤右打到底倒車，車身斜約 45 度時回正直倒，車頭快進格子時左打到底擺正。'),
        ('路邊停車要離前車多遠開始倒？', '一般建議車身和前車平行、間隔約 50 公分到 1 公尺，車尾大約對齊前車車尾。實際距離依車型和教練教的參考點調整。'),
        ('路邊停車壓線扣幾分？', '依公路局小型車場考評分標準，平行路邊停車車輪壓線或未停入規定範圍扣 16 分，起駛前未打方向燈扣 32 分。'),
        ('路邊停車要打方向燈嗎？', '靠邊停車和駛出前都應該依規定顯示方向燈。場考駛出時沒打方向燈扣 32 分。')],
  related=[('reverse-parking', '倒車入庫技巧', '5 步驟圖解'), ('driving-test-2026', '場考扣分標準', '2026 新制'), ('parking-tips', '新手停車技巧', '斜角停車、三點迴轉'), ('license-steps', '考駕照流程與費用', '報名、預約、重考')])

GUIDES['s-curve'] = dict(
  title='S 型曲線進退技巧：前進不壓線、後退看照後鏡｜停好停滿',
  h1='曲線進退（S 型）技巧：前進貼外側，後退看後輪',
  desc='汽車場考曲線進退（S 型彎道）怎麼開？前進時車頭貼外側線、後退時看照後鏡讓後輪留在線內，加上前進壓線扣 32 分、後退修正扣 8 分的規則與免費練習。',
  lede='曲線進退要開進一條 S 型彎道再整段倒退出來。前進的關鍵是「車頭貼外側」，後退的關鍵是「看照後鏡顧後輪」。',
  crumb='曲線進退技巧', kw=['曲線進退', 'S型', 'S 型 倒車', '曲線前進', '曲線後退', '汽車場考 S 型'],
  body=f"""<figure>{SVG_S}<figcaption>示意圖。後輪會走在前輪內側（內輪差），所以前進時車頭要貼外側線。</figcaption></figure>
<h2>前進：車頭貼外側線</h2>
<ol class="steps">
<li><b>入彎前放慢，用怠速慢慢走。</b></li>
<li><b>左彎時車頭貼右側線，右彎時車頭貼左側線。</b>後輪會走在前輪內側，車頭走外側，內側後輪才不會切到內線。</li>
<li><b>換彎時方向盤慢慢回正再打另一邊。</b>彎道交接處最容易壓線。</li>
</ol>
<h2>後退：看照後鏡顧後輪</h2>
<ol class="steps">
<li><b>想讓車尾往哪邊，方向盤就往哪邊打。</b></li>
<li><b>輪流看兩側照後鏡，</b>讓後輪和兩側黃線的距離差不多。</li>
<li><b>小幅度修正、慢慢退。</b>普通小型車後退壓線不扣分，但往前修正每次扣 8 分，所以盡量一路退到底。</li>
</ol>
<h2>場考怎麼扣分</h2>
<p>曲線進退<b>前進時車輪壓線扣 32 分</b>；普通小型車<b>後退時壓線不扣分</b>，但往前修正每次扣 8 分，中途熄火或停車扣 8 分（停車最多扣 2 次）。詳見 <a href="../driving-test-2026/">場考扣分標準</a>。</p>
<h2>在網頁遊戲裡練習</h2>
{cta('lv-scurve', '練習曲線前進', [('lv-screv', '練習曲線後退'), ('exam-curve', '場考模擬：曲線進退')])}""",
  faqs=[('S 型前進要怎麼看才不會壓線？', '左彎時車頭貼右側線、右彎時車頭貼左側線。因為後輪會走在前輪內側，車頭走外側，內側後輪才不會壓到內線。'),
        ('曲線後退壓線會扣分嗎？', '依公路局評分標準，普通小型車後退時壓線不扣分，但往前修正每次扣 8 分，中途熄火或停車也扣 8 分。'),
        ('曲線前進壓線扣幾分？', '前進時車輪壓線扣 32 分，等於一次扣掉將近三分之一。')],
  related=[('reverse-parking', '倒車入庫技巧', '過庫停、打到底'), ('parallel-parking', '路邊停車技巧', '三個轉向點'), ('driving-test-2026', '場考扣分標準', '完整項目表'), ('license-steps', '考駕照流程與費用', '報名到拿照')])

GUIDES['driving-test-2026'] = dict(
  title='汽車駕照場考扣分標準與 2026 新制：停讓行人、轉頭看死角｜停好停滿',
  h1='汽車駕照場考扣分標準（2026 新制整理）',
  desc='小型車場考 100 分起扣、70 分及格。整理起駛、行人穿越道、平交道、倒車入庫、路邊停車、上坡起步、曲線進退的扣分項目，以及 2026 年 3 月 31 日起新增的停讓行人與轉頭確認死角規定。',
  lede='汽車駕照（小型車）場考滿分 100、70 分及格。一次扣 32 分的動作只要漏三次就一定不及格，所以最重要的是把「繫安全帶、轉頭看、打方向燈、停讓」練成習慣。',
  crumb='場考扣分標準', kw=['汽車場考', '汽車駕照 扣分', '場考扣分標準', '2026 考照新制', '停讓行人 扣32分', '考駕照'],
  body=f"""<h2>2026 年 3 月 31 日起的新制</h2>
<ul>
<li><b>無號誌路口停讓行人：</b>經過行人穿越道要減速，有行人要停讓，沒做到扣 32 分。</li>
<li><b>起步、環場與打方向燈前轉頭確認：</b>要轉頭查看照後鏡和視野死角，沒做到扣 32 分。</li>
<li>適用以考試日期為準：3 月 31 日（含）以後考試用新評分表。</li>
</ul>
<h2>常見扣分項目</h2>
{TEST_TABLE}
<div class="callout">以上整理自公路局小型車場考評分標準與 2026 新制報導，項目名稱、順序和細節各監理站可能不同，請以報考監理站公告的最新評分表為準。</div>
<h2>最容易被當的 5 件事</h2>
<ol class="steps">
<li><b>上車忘了繫安全帶。</b>一起步就扣 32 分。</li>
<li><b>起步、打方向燈前沒轉頭。</b>2026 新制，只看照後鏡不夠，要轉頭看死角。</li>
<li><b>行人穿越道沒停讓。</b>看到斑馬線就先放慢。</li>
<li><b>平交道沒有完全停下來左右看。</b>停、看、聽。</li>
<li><b>曲線前進壓線。</b>前進壓線扣 32 分，後退壓線不扣分。</li>
</ol>
<h2>用模擬考練流程</h2>
<p>「停好停滿」的考照模擬照著這份扣分標準做了 8 站：起駛、行人穿越道、號誌路口、平交道、上坡起步、路邊停車、倒車入庫、曲線進退。考完會列出每一個扣分原因，手機也能玩。</p>
{cta('exam', '開始場考模擬考', [('exam-rail', '只練平交道'), ('exam-cross', '只練停讓行人')])}""",
  faqs=[('汽車場考幾分及格？', '小型車場考滿分 100 分，70 分及格。'),
        ('2026 汽車考照新制改了什麼？', '2026 年 3 月 31 日起，小型車場考新增無號誌路口停讓行人，以及起步、環場、打方向燈前要轉頭確認死角，沒做到都是扣 32 分。'),
        ('場考哪些動作一次扣 32 分？', '例如未繫安全帶、起駛前未打方向燈、未轉頭確認死角、未停讓行人、平交道不停車察看、曲線前進壓線等。'),
        ('倒車入庫和路邊停車壓線扣幾分？', '兩者都是車輪壓線或未停入規定範圍扣 16 分。')],
  related=[('reverse-parking', '倒車入庫技巧', '5 步驟圖解'), ('parallel-parking', '路邊停車技巧', '並排、45 度、擺正'), ('s-curve', 'S 型曲線進退', '前進與後退'), ('license-steps', '考駕照流程與費用', '報名、預約、重考')])

GUIDES['license-steps'] = dict(
  title='考汽車駕照流程與費用：報名、預約、筆試、場考、路考｜停好停滿',
  h1='考汽車駕照流程懶人包：從報名到拿到駕照',
  desc='第一次考汽車駕照要怎麼準備？整理網路預約報名、駕訓班或自學、筆試、場考、路考的順序、自行報考的費用，以及 2026 年起未到考會暫停預約的規定。',
  lede='考汽車駕照大致分成：上網預約、筆試、場地駕駛考驗（場考）、道路駕駛考驗（路考）。下面是新手最常問的流程與注意事項。',
  crumb='考駕照流程', kw=['考汽車駕照', '考駕照流程', '汽車駕照 費用', '汽車駕照 報名', '駕訓班', '自學考駕照'],
  body=f"""<h2>考照流程</h2>
<ol class="steps">
<li><b>決定上駕訓班或自學。</b>駕訓班結業可以在駕訓班考場考；自學要先申請學習駕駛證，由有駕照的人陪同在規定時間地點練習，再到監理站考。</li>
<li><b>體檢與上網預約。</b>目前考照採網路預約，到監理服務網選考試日期與監理站。</li>
<li><b>筆試。</b>交通規則與標誌的選擇、是非題，及格才能考路考。</li>
<li><b>場地駕駛考驗（場考）。</b>起駛、行人穿越道、平交道、倒車入庫、路邊停車、上坡起步、曲線進退等，100 分起扣、70 分及格。</li>
<li><b>道路駕駛考驗（路考）。</b>在實際道路上依指示行駛。</li>
<li><b>通過後領照。</b></li>
</ol>
<h2>費用</h2>
<p>不透過駕訓班、直接到監理站報考汽車駕照，網路上整理的首次全項費用約 450 元、一年內重考每次約 225 元；駕訓班學費另計。費用可能調整，請以監理服務網公告為準。</p>
<h2>預約要注意</h2>
<ul>
<li>2026 年起，預約後沒取消也沒到考，會被暫停預約：第 1 次 15 天、第 2 次 30 天、第 3 次 60 天。不能去就記得線上取消。</li>
<li>熱門監理站名額常常很滿，最好提早預約。</li>
</ul>
<div class="callout">以上整理自公開報導與監理單位資訊，規定可能變動。報名條件、費用、考試項目請以交通部公路局監理服務網和報考監理站的最新公告為準。</div>
<h2>考前用模擬考熟悉流程</h2>
{cta('exam', '免費場考模擬', [('lv-bay', '練倒車入庫'), ('lv-parallel', '練路邊停車')])}""",
  faqs=[('考汽車駕照要多少錢？', '自行到監理站報考，網路整理的首次全項費用約 450 元、一年內重考每次約 225 元，駕訓班學費另計。實際以監理服務網公告為準。'),
        ('考駕照可以現場報名嗎？', '目前採網路預約，請到監理服務網預約考試日期與監理站。'),
        ('預約考試沒去會怎樣？', '2026 年起，未取消又未到考會被暫停預約，第 1 次 15 天、第 2 次 30 天、第 3 次 60 天。'),
        ('場考跟路考差在哪？', '場考是在考場內考倒車入庫、路邊停車等項目；路考是在實際道路上依指示行駛。場考 70 分及格才能接著考路考。')],
  related=[('driving-test-2026', '場考扣分標準', '2026 新制'), ('reverse-parking', '倒車入庫技巧', '5 步驟圖解'), ('parallel-parking', '路邊停車技巧', '三個轉向點'), ('s-curve', 'S 型曲線進退', '不壓線的看法')])

GUIDES['parking-tips'] = dict(
  title='新手停車技巧：斜角停車、三點迴轉、地下停車場倒車入位｜停好停滿',
  h1='新手停車技巧：生活中最常遇到的 5 種停車',
  desc='拿到駕照後最常遇到的停車情境：賣場停車格、斜角停車、加油站、三點迴轉、地下停車場柱子旁倒車入位、透天厝車庫，整理新手技巧並附免費停車遊戲練習關卡。',
  lede='考完駕照才是開始。停車場的柱子、旁邊的休旅車、巷口的機車，才是新手最常擦撞的地方。',
  crumb='新手停車技巧', kw=['新手停車', '停車技巧', '斜角停車', '三點迴轉', '地下停車場 停車', '停車遊戲'],
  body=f"""<h2>1. 賣場停車格（車頭朝內）</h2>
<p>車頭朝內最簡單：開到車位正前方再轉進去。太早轉，後輪會切到旁邊的車（內輪差）。</p>
{cta('lv-mall', '練習賣場停車')}
<h2>2. 斜角停車</h2>
<p>斜角車位只要轉約 60 度，比直角車位好進。車頭對準車位再轉，注意右後方。</p>
{cta('lv-angle', '練習斜角停車')}
<h2>3. 加油站</h2>
<p>進加油島前就要對正，進去之後兩側空間很小，幾乎沒有修正空間。</p>
{cta('lv-gas', '練習加油站')}
<h2>4. 三點迴轉</h2>
<ol class="steps">
<li><b>方向盤左打到底往前，</b>前輪快碰到對面路緣就停。</li>
<li><b>方向盤右打到底倒車，</b>車尾快碰到另一側就停。</li>
<li><b>再左打到底往前，</b>就轉過來了。巷子窄的話可能要來回多次。</li>
</ol>
{cta('lv-uturn', '練習三點迴轉')}
<h2>5. 地下停車場倒車入位</h2>
<p>柱子通常在車位的前角，太早打方向盤一定擦到。倒車雷達變紅就停，往前修正再退。大車（休旅車）在窄車位會更難。</p>
{cta('lv-b3', '練習地下停車場', [('lv-house', '透天厝車庫（最難）')])}
<h2>為什麼用停車遊戲練習？</h2>
<p>「停好停滿」是免費、免下載的網頁停車遊戲，用真實轉向幾何計算車子的行進路線，能幫你建立「方向盤打多少、車尾會跑去哪」的感覺；卡關時可以叫出提示路線，也有練習模式擦撞不會失敗。</p>""",
  faqs=[('新手停車最常擦撞在哪？', '多半是轉進車位時太早打方向盤，後輪走在前輪內側（內輪差）切到旁邊的車或柱子。'),
        ('三點迴轉怎麼做？', '左打到底往前到快碰路緣，右打到底倒車，再左打到底往前。巷子窄可能要來回多次。'),
        ('有免費的停車遊戲可以練習嗎？', '「停好停滿」是免費網頁停車遊戲，有 12 個停車關卡和汽車場考模擬，手機、電腦都能玩。')],
  related=[('reverse-parking', '倒車入庫技巧', '5 步驟圖解'), ('parallel-parking', '路邊停車技巧', '並排、45 度、擺正'), ('driving-test-2026', '場考扣分標準', '2026 新制'), ('license-steps', '考駕照流程與費用', '報名、預約、重考')])

for slug, g in GUIDES.items():
    os.makedirs(f'{ROOT}/guide/{slug}', exist_ok=True)
    with open(f'{ROOT}/guide/{slug}/index.html', 'w') as f:
        f.write(page(slug, g['title'], g['h1'], g['desc'], g['lede'], g['body'], g['faqs'], g['related'], g['kw'], g['crumb']))

# guide hub
cards = ''.join(f'<a href="../guide/{s}/">{g["h1"]}<span>{g["desc"][:60]}…</span></a>'.replace('../guide/', './') for s, g in GUIDES.items())
hub = page('', '停車技巧與考駕照教學：倒車入庫、路邊停車、場考扣分｜停好停滿', '停車技巧與考駕照教學',
  '新手停車與汽車駕照考試教學整理：倒車入庫技巧、路邊停車口訣、S 型曲線進退、2026 場考扣分新制、考駕照流程費用，每篇都能直接在免費網頁遊戲裡練習。',
  '從考駕照到日常停車，最常被搜尋的問題都整理在這裡。每篇都附免費練習關卡。',
  f'<div class="related">{cards}</div><div class="cta"><a class="btn" href="../play/">開始玩停好停滿 →</a><a class="btn ghost" href="../play/#exam">場考模擬考</a></div>',
  [], [], ['停車技巧', '倒車入庫', '路邊停車', '考駕照', '汽車場考'], '教學')
hub = hub.replace('href="../../', 'href="../')  # hub sits one level up
os.makedirs(f'{ROOT}/guide', exist_ok=True)
open(f'{ROOT}/guide/index.html', 'w').write(hub)

# sitemap
urls = [('', '1.0', 'weekly'), ('play/', '0.9', 'weekly'), ('guide/', '0.8', 'weekly')] + [(f'guide/{s}/', '0.8', 'monthly') for s in GUIDES] + [('drive/', '0.4', 'monthly')]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{u}</loc><lastmod>{DATE}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n' for u, p, c in urls) + '</urlset>\n'
open(f'{ROOT}/sitemap.xml', 'w').write(sm)
open(f'{ROOT}/favicon.svg', 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#3fe0ff"/><text x="32" y="47" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="44" text-anchor="middle" fill="#0b0c1c">P</text></svg>')
print('ok', len(GUIDES))
