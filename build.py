#!/usr/bin/env python3
"""Reads lectures.json and writes index.html (static, Hebrew RTL).
Run: python3 build.py"""
import json, html, collections
CH = "https://www.youtube.com/@aiDotEngineer"
css = open('base.css').read() + """
.lec{background:var(--card,#111317);border:1px solid #24282f;border-radius:16px;padding:20px;margin:16px 0}
.lec h3{margin:0 0 4px;font-size:1.15rem;direction:ltr;text-align:right}.meta{color:#9aa0a8;font-size:.85rem;margin:0 0 12px}
.tags span{display:inline-block;border:1px solid #3a3f48;border-radius:999px;padding:2px 10px;margin:0 0 6px 6px;font-size:.78rem;color:#c9ced6}
.lec ul{padding-right:20px}.lec li{margin:6px 0}.aud{border-top:1px solid #24282f;margin-top:12px;padding-top:10px;color:#c9ced6}
.src{display:inline-block;margin-top:10px;color:#F7931A;text-decoration:none;font-weight:600}
.daytitle{margin-top:36px}.note{color:#9aa0a8;font-size:.9rem}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}.toc a{border:1px solid #24282f;border-radius:999px;padding:6px 14px;font-size:.85rem;color:#9aa0a8;text-decoration:none}
"""
L = json.load(open('lectures.json'))
L.sort(key=lambda x: (x['published_est'], x['added']), reverse=True)
HEB = ['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר']
def dlabel(d):
    y, m, dd = d.split('-'); return f"{int(dd)} ב{HEB[int(m)-1]} {y}"
def mins(s): return f"{s//60}:{s%60:02d}"
groups = collections.OrderedDict()
for x in L: groups.setdefault(x['published_est'], []).append(x)
body = []; toc = []
for d, items in groups.items():
    toc.append(f'<a href="#d{d}">{dlabel(d)} ({len(items)})</a>')
    cards = []
    for x in items:
        s = x['summary_he']
        pts = ''.join(f'<li>{html.escape(p)}</li>' for p in s['points'])
        tags = ''.join(f'<span>{html.escape(t)}</span>' for t in s['tags'])
        tr = '' if x['transcript'] == 'available' else '<p class="note">לא נמצא תמלול שמיש להרצאה הזו, ולכן אין סיכום מבוסס תוכן.</p>'
        cards.append(f'''<article class="lec" id="v{x['id']}"><h3>{html.escape(x['title'])}</h3>
<p class="meta">{html.escape(x['speaker'])} · {html.escape(x['org'])} · {mins(x['duration_sec'])} דקות</p>
<p><strong>בקצרה:</strong> {html.escape(s['tldr'])}</p><ul>{pts}</ul>
<p class="aud"><strong>למי זה מתאים:</strong> {html.escape(s['audience'])}</p>{tr}
<div class="tags">{tags}</div><a class="src" href="{x['url']}" rel="noopener" target="_blank">צפייה בהרצאה ביוטיוב ←</a></article>''')
    body.append(f'<section class="section" id="d{d}"><div class="wrap"><h2 class="daytitle">{dlabel(d)} <span class="note">(תאריך משוער)</span></h2>{"".join(cards)}</div></section>')
n = len(L)
page = f'''<!DOCTYPE html>
<html dir="rtl" lang="he"><head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1" name="viewport"/><meta content="#030304" name="theme-color"/><meta content="סיכומים בעברית של ההרצאות בערוץ AI Engineer" name="description"/><title>AI Engineer בעברית | DATA&amp;AI</title><link href="https://fonts.googleapis.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&amp;family=Space+Grotesk:wght@500;700&amp;display=swap" rel="stylesheet"/><style>{css}</style></head><body>
<header class="top"><div class="wrap"><a class="brand" href="https://rkinstinct.github.io/data-ai-hub/">DATA<span style="color:#F7931A">&amp;</span>AI <b>/ AI Engineer</b></a></div></header>
<main id="main"><div class="hero"><div class="wrap"><div class="eyebrow">AI ENGINEER · סיכומי הרצאות</div><h1>AI Engineer בעברית</h1>
<p class="lead">סיכום בעברית של כל הרצאה שעולה לערוץ <a href="{CH}" rel="noopener" target="_blank" style="color:#F7931A">AI Engineer</a> ביוטיוב. כל סיכום נכתב מהתמלול של ההרצאה עצמה, מהחדשות לישנות, וקישור למקור מצורף לכל הרצאה.</p>
<p class="note">{n} הרצאות עד כה. תאריכי הפרסום משוערים (נגזרו מגיל ההעלאה שהוצג ביוטיוב) ועשויים לסטות ביום. הרצאות ארוכות (סדנאות ומעל 25 דקות) עדיין לא סוכמו. חלק מההרצאות הן הצגות של חברות, וזה מצוין בסיכום.</p>
<div class="toc">{''.join(toc)}</div></div></div>
{''.join(body)}</main>
<footer><div class="wrap"><span>סיכומים עצמאיים, לא פרסום רשמי של AI Engineer. התוכן שייך ליוצרים המקוריים.</span></div><p class="rights-line" style="text-align:center;margin:18px auto 0;padding:0 16px;font-size:.92em;opacity:.9;width:100%">© כל הזכויות שמורות לראובן קזורר</p></footer></body></html>'''
open('index.html', 'w').write(page)
print('built', n, 'lectures,', len(page), 'bytes')
