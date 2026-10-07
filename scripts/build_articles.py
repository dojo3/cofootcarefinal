"""Build the on-site article collection from preserved, sanitized article content."""
import json, html, re, math, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ARTICLES = json.loads((ROOT / 'data/articles.json').read_text())
BASE = 'https://coloradofootcarenurse.com/'
def esc(s): return html.escape(str(s), quote=True)
def date_label(value):
    if len(value) == 10: return datetime.date.fromisoformat(value).strftime('%B %-d, %Y')
    return value
base_page = (ROOT / 'about.html').read_text()
header = re.search(r'<header class="site-header">.*?</header>', base_page, re.S)[0].replace('aria-current="page" href="about.html"', 'href="about.html"').replace('href="articles.html">Articles', 'aria-current="page" href="articles.html">Articles')
footer = re.search(r'<footer class="site-footer">.*?</footer>', base_page, re.S)[0]
end = '<a class="mobile-call button" href="tel:+13036688992">Call Kirsten · (303) 668-8992</a><script src="js/site-refresh.js" defer></script>'
def page(title, desc, path, body, schema, nested=False, extra_script=''):
    h, f, e = header, footer, end
    prefix = '../' if nested else ''
    if nested:
        for name in ['index.html','services.html','about.html','articles.html','contact.html','service-areas.html','js/site-refresh.js']:
            h=h.replace('"'+name+'"','"../'+name+'"');f=f.replace('"'+name+'"','"../'+name+'"');e=e.replace('"'+name+'"','"../'+name+'"')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | Kirsten Antony, RN</title><meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow"><link rel="canonical" href="{BASE+path}">
<meta property="og:type" content="{'article' if nested else 'website'}"><meta property="og:site_name" content="Colorado Foot Care Nurse"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE+path}"><meta property="og:image" content="{BASE}images/kirsten-antony-social-share.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#173f3a"><link rel="icon" href="{prefix}favicon.ico"><link rel="stylesheet" href="{prefix}css/site-refresh.css"><link rel="stylesheet" href="{prefix}css/articles.css">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</','<\\/')}</script></head>
<body><a class="skip-link" href="#main">Skip to content</a>{h}<main id="main">{body}</main>{f}{e}{extra_script}</body></html>'''
cards=[]
for a in ARTICLES:
    url='articles/'+a['slug']+'.html'
    cards.append(f'''<a class="writing-card" href="{url}" data-article data-category="{esc(a['category'])}" data-search="{esc((a['title']+' '+a['category']+' '+a['date'][:4]).lower())}"><span class="writing-meta">{esc(a['category'])} <span aria-hidden="true">·</span> {a['date'][:4]}</span><h2>{esc(a['title'])}</h2><p>{esc(a['excerpt'])}</p><span class="writing-link">Read article <span aria-hidden="true">→</span><small>{a['minutes']} min read</small></span></a>''')
filters=''.join('<button type="button" data-topic="'+esc(c)+'" aria-pressed="'+('true' if c=='All articles' else 'false')+'">'+esc(c)+'</button>' for c in ['All articles','Foot care','Mindfulness','Healing arts','Nature & nutrition','Healthy aging'])
body=f'''<section class="page-hero writing-hero"><div class="shell"><div class="writing-intro"><div><p class="eyebrow">The writing collection · 2015–2025</p><h1>On caring for yourself.<br>And living a little better.</h1><p>Thoughts on foot care, mindful living, nature, and the healing arts. Explore Kirsten’s complete articles, gathered here to read and return to.</p><span class="collection-count">41 articles · Foot care, wellness &amp; a curious mind</span></div><aside class="writing-author"><img src="images/headshot.jpg" width="76" height="76" alt="Kirsten Antony, RN"><strong>Kirsten Antony, RN</strong><p>A Colorado nurse with a lifelong interest in caring for the whole person.</p><a href="about.html">Meet the author →</a></aside></div></div></section>
<section class="section shell writing-collection"><div class="writing-tools" data-filter-tools hidden><label for="article-search">Find something that speaks to you</label><input type="search" id="article-search" placeholder="Search titles, topics, or years…" autocomplete="off"><div class="topic-filters" aria-label="Filter articles by topic">{filters}</div></div><div class="collection-heading"><h2>Browse the collection</h2><p id="article-count" role="status" aria-live="polite">41 articles</p></div><div class="writing-grid">{''.join(cards)}</div><div id="article-empty" class="empty-results" hidden><h2>No articles found</h2><p>Try a different title, topic, or year.</p><button class="button" type="button" data-reset-search>Show all articles</button></div><p class="article-note note">Originally published in Prime Time News and on Kirsten’s website. These articles reflect their original publication dates and are offered for education, reflection, and enjoyment.</p></section>'''
schema={'@context':'https://schema.org','@type':'CollectionPage','name':'Articles by Kirsten Antony, RN','url':BASE+'articles.html','author':{'@id':BASE+'#kirsten'},'mainEntity':{'@type':'ItemList','numberOfItems':len(ARTICLES),'itemListElement':[{'@type':'ListItem','position':i+1,'name':a['title'],'url':BASE+'articles/'+a['slug']+'.html'} for i,a in enumerate(ARTICLES)]}}
(ROOT/'articles.html').write_text(page('Articles for healthier, more mindful living','Read 41 articles by Kirsten Antony, RN, on foot care, mindfulness, nature, healthy aging, and the healing arts.','articles.html',body,schema,extra_script='<script src="js/articles.js" defer></script>'))
for i,a in enumerate(ARTICLES):
    path='articles/'+a['slug']+'.html'
    sources=[]
    if a.get('snapshot'):sources.append('<a href="'+esc(a['snapshot'])+'" rel="noopener noreferrer">Archived publication</a>')
    if a.get('author_copy'):sources.append('<a href="'+esc(a['author_copy'])+'" rel="noopener noreferrer">Original author’s copy</a>')
    original_label='Originally published in Prime Time News' if a['publication']=='Prime Time News' else 'From Kirsten’s Article Blog'
    related=[x for x in ARTICLES if x['category']==a['category'] and x['slug']!=a['slug']][:3]
    related_html=''.join(f'<a href="{x["slug"]}.html"><span>{esc(x["date"][:4])}</span><strong>{esc(x["title"])}</strong><b aria-hidden="true">→</b></a>' for x in related)
    care_link = '<aside class="article-care-link"><p class="eyebrow">Foot care, brought home</p><h2>Could your feet use a little care?</h2><p>Kirsten provides gentle in-home foot and nail care throughout Highlands Ranch and the Denver metro.</p><a class="button button-secondary" href="../services.html">Explore foot care &amp; prices →</a></aside>' if a['category']=='Foot care' else ''
    body=f'''<section class="page-hero reading-hero"><div class="reading-shell"><p class="eyebrow">{esc(a['category'])}</p><h1>{esc(a['title'])}</h1><div class="reading-byline"><img src="../images/headshot.jpg" width="48" height="48" alt=""><div><strong>By <a href="../about.html" rel="author">Kirsten Antony, RN</a></strong><span><time datetime="{a['date']}">{date_label(a['date'])}</time> · {a['minutes']} min read</span></div></div><p class="publication-line">{original_label} · Preserved from the original publication</p></div></section><div class="reading-shell reading-wrap"><div class="reading-actions"><a href="../articles.html">Browse the collection</a><button type="button" data-print-article>Print / save PDF</button></div><article class="article-prose" aria-label="{esc(a['title'])}">{a['body_html']}</article><aside class="reading-note"><p>Written by Kirsten Antony, RN. Preserved here as originally published, with formatting adapted for reading.</p><p>Educational content does not replace individual medical advice, diagnosis, or treatment.</p><p class="source-links">{' · '.join(sources)}</p></aside>{care_link}<section class="related-writing"><p class="eyebrow">Keep reading</p><h2>More to explore</h2><div>{related_html}</div><a class="button button-secondary" href="../articles.html">View all articles</a></section></div>'''
    schema={'@context':'https://schema.org','@type':'Article','headline':a['title'],'description':a['excerpt'],'author':{'@type':'Person','name':'Kirsten Antony','url':BASE+'about.html'},'mainEntityOfPage':BASE+path,'dateModified':'2026-10-07','articleSection':a['category'],'inLanguage':'en','publisher':{'@type':'Organization','name':'Colorado Foot Care Nurse'},'image':BASE+'images/kirsten-antony-social-share.jpg','isBasedOn':a.get('original') or a.get('author_copy')}
    if len(a['date'])==10:schema['datePublished']=a['date']
    (ROOT/path).write_text(page(a['title'],a['excerpt'],path,body,schema,nested=True,extra_script='<script src="../js/articles.js" defer></script>'))
print('Built',len(ARTICLES),'article pages and collection')
