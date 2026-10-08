"""Rebuild article pages, shared navigation, search metadata and sitemap.

Run with Python 3 after editing the main HTML pages or data/articles.json.
Dependencies: lxml (pip install lxml).
"""
import datetime
import html as H
import json
import re
import subprocess
import sys
from pathlib import Path
from lxml import html, etree

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://coloradofootcarenurse.com/'
TODAY = '2026-10-07'
VERSION = '20261007-polish'
PRIMARY = ['index.html','services.html','about.html','articles.html','service-areas.html','contact.html']
LABELS = {'index.html':'Home','services.html':'Services & pricing','about.html':'About Kirsten','articles.html':'Articles','service-areas.html':'Service areas','contact.html':'Contact','404.html':'Page not found'}
META = {
 'index.html':('Mobile Foot Care in Denver & Highlands Ranch | Kirsten Antony, RN','Professional medical foot care services provided by Kirsten Antony, RN. Serving Denver, Highlands Ranch and nearby communities. Visits start at $90.'),
 'services.html':('Mobile Foot Care Services & Prices | Kirsten Antony, RN','See in-home foot care prices by city: Highlands Ranch from $90, Denver and Aurora $100, Golden and Arvada $110, Broomfield $115. Couples discounts available.'),
 'about.html':('About Kirsten Antony, RN | Mobile Foot Care Since 2001','Meet Kirsten Antony, a Colorado registered nurse providing mobile foot care since 2001, with experience in long-term care, wound care and holistic wellness.'),
 'articles.html':('Foot Care & Wellness Articles by Kirsten Antony, RN',f'Read {len(json.loads((ROOT / "data/articles.json").read_text()))} complete articles by Kirsten Antony, RN. Explore foot care, mindfulness, healthy aging, nature and the healing arts, with search and topic filters.'),
 'service-areas.html':('Mobile Foot Care Service Areas & Visit Prices | Denver Metro','Find in-home foot care in Highlands Ranch, Denver, Aurora, Parker, Castle Rock, Golden, Arvada, Westminster and Broomfield. Check your city’s visit price.'),
 'contact.html':('Contact Kirsten Antony, RN | Schedule In-Home Foot Care','Call or text (303) 668-8992 to discuss mobile foot care in the Denver metro. Arrange a home visit for yourself, a loved one, a couple or a senior community.'),
 '404.html':('Page Not Found | Colorado Foot Care Nurse','Find services, pricing and articles from Kirsten Antony, RN.')
}
CITIES = ['Highlands Ranch','Littleton','Centennial','Lone Tree','Parker','Castle Rock','Castle Pines','Lakewood','Morrison','Denver','Aurora','Golden','Wheat Ridge','Arvada','Westminster','Broomfield']
SOCIAL = ['https://m.facebook.com/soultosoleholistichealthcare','https://www.instagram.com/soultosoleholistichealth/','https://www.linkedin.com/in/kirstenantony']
def esc(s):return H.escape(str(s),quote=True)
def canon(path):return BASE if path=='index.html' else BASE+path
def prefix(path):return '/' if path=='404.html' else '../' if '/' in path else ''
def header(path):
 p=prefix(path)
 active='articles.html' if path.startswith('articles/') else path
 items=[('index.html','Home'),('services.html','Services & pricing'),('about.html','About'),('articles.html','Articles'),('contact.html','Contact')]
 links=''
 for target,label in items:
  current='aria-current="page" ' if target==active else ''
  links+=f'<a {current}href="{p+target}">{esc(label)}</a>'
 return f'''<header class="site-header"><div class="shell header-inner"><a class="brand" href="{p}index.html" aria-label="Colorado Foot Care Nurse home"><span class="brand-mark" aria-hidden="true">KA</span><span><strong>Kirsten Antony, RN</strong><small>Colorado Foot Care Nurse</small></span></a><button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav"><span></span><span></span><span></span><span class="sr-only">Open menu</span></button><nav id="primary-nav" class="primary-nav" aria-label="Primary navigation">{links}<a class="button button-small" href="tel:+13036688992">Call (303) 668-8992</a></nav></div></header>'''
def footer(path):
 p=prefix(path)
 return f'''<footer class="site-footer"><div class="shell footer-grid"><div><a class="brand footer-brand" href="{p}index.html"><span class="brand-mark" aria-hidden="true">KA</span><span><strong>Kirsten Antony, RN</strong><small>Colorado Foot Care Nurse</small></span></a><p>Gentle foot and nail care, brought to your door. Serving Highlands Ranch and the Denver metro since 2001.</p></div><div><h2>Explore</h2><a href="{p}services.html">Services &amp; pricing</a><a href="{p}service-areas.html">Cities &amp; service areas</a><a href="{p}about.html">Meet Kirsten</a><a href="{p}articles.html">The article collection</a><a href="{p}contact.html">Arrange a visit</a></div><div><h2>Let’s talk</h2><a href="tel:+13036688992">(303) 668-8992</a><a href="mailto:kalacolorado@gmail.com">kalacolorado@gmail.com</a><span>Monday–Friday · 9am–5pm</span></div></div><div class="shell footer-bottom"><span>© <span data-year>2026</span> Kirsten Antony, RN</span><span>Serving private homes, families &amp; senior communities.</span></div></footer>'''
def entities():
 business={'@type':'LocalBusiness','@id':BASE+'#business','name':'Colorado Foot Care Nurse','alternateName':['Kirsten Antony, RN — Mobile Foot Care','Heel Your Feet'],'url':BASE,'image':BASE+'images/headshot.jpg','telephone':'+1-303-668-8992','email':'kalacolorado@gmail.com','description':'Mobile foot and nail care by Kirsten Antony, RN, serving Highlands Ranch and the Denver metro area.','areaServed':[{'@type':'City','name':c+', Colorado'} for c in CITIES],'founder':{'@id':BASE+'#kirsten'},'foundingDate':'2001','sameAs':SOCIAL,'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday'],'opens':'09:00','closes':'17:00'}]}
 person={'@type':'Person','@id':BASE+'#kirsten','name':'Kirsten Antony','honorificSuffix':'RN','jobTitle':'Registered Nurse and Foot Care Nurse','url':BASE+'about.html','image':BASE+'images/headshot.jpg','description':'Colorado registered nurse providing mobile foot care since 2001, with long-term care and wound care experience.','worksFor':{'@id':BASE+'#business'},'sameAs':SOCIAL}
 website={'@type':'WebSite','@id':BASE+'#website','url':BASE,'name':'Colorado Foot Care Nurse','alternateName':'Kirsten Antony, RN','inLanguage':'en-US','publisher':{'@id':BASE+'#business'}}
 return [business,person,website]
def breadcrumb_data(path,title):
 items=[('Home',BASE)]
 if path.startswith('articles/'):items.append(('Articles',BASE+'articles.html'))
 items.append((LABELS.get(path,title),canon(path)))
 return {'@type':'BreadcrumbList','@id':canon(path)+'#breadcrumbs','itemListElement':[{'@type':'ListItem','position':i+1,'name':label,'item':url} for i,(label,url) in enumerate(items)]}
def breadcrumb_html(path,title):
 items=[f'<a href="{prefix(path)}index.html">Home</a>']
 if path.startswith('articles/'):items.append(f'<a href="../articles.html">Articles</a>')
 items.append(f'<span aria-current="page">{esc(LABELS.get(path,title))}</span>')
 return '<nav class="breadcrumbs" aria-label="Breadcrumb">'+ '<span aria-hidden="true">/</span>'.join(items)+'</nav>'
def process(path):
 file=ROOT/path;doc=html.fromstring(file.read_text())
 old_schemas=[]
 for n in doc.xpath('//script[@type="application/ld+json"]'):
  value=json.loads(n.text);old_schemas.extend(value.get('@graph',[value]))
 title,desc=META.get(path,(doc.xpath('//title')[0].text,doc.xpath('//meta[@name="description"]')[0].get('content')))
 url=canon(path);p=prefix(path);article=path.startswith('articles/')
 graph=entities()
 page_type='ProfilePage' if path=='about.html' else 'ContactPage' if path=='contact.html' else 'CollectionPage' if path=='articles.html' else 'WebPage'
 web_page={'@type':page_type,'@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':'en-US','isPartOf':{'@id':BASE+'#website'},'about':{'@id':BASE+'#business'}}
 if path!='index.html':
  graph.append(breadcrumb_data(path,title.split(' | ')[0]));web_page['breadcrumb']={'@id':url+'#breadcrumbs'}
 if path=='about.html':web_page['mainEntity']={'@id':BASE+'#kirsten'}
 elif path=='contact.html':web_page['mainEntity']={'@id':BASE+'#business'}
 elif path=='articles.html':
  collection=next((x for x in old_schemas if x.get('@type')=='CollectionPage'),None)
  if collection:web_page['mainEntity']=collection['mainEntity']
 elif path=='services.html':
  offers=next((x for x in old_schemas if x.get('@type')=='ItemList'),None)
  if offers:
   offers.pop('@context',None);offers['@id']=url+'#services';graph.append(offers);web_page['mainEntity']={'@id':url+'#services'}
 elif article:
  item=next(x for x in old_schemas if x.get('@type')=='Article')
  item.pop('@context',None);item.pop('dateModified',None)
  item.update({'@id':url+'#article','author':{'@id':BASE+'#kirsten'},'publisher':{'@id':BASE+'#business'},'mainEntityOfPage':{'@id':url+'#webpage'},'isPartOf':{'@id':BASE+'articles.html#webpage'},'inLanguage':'en-US'})
  graph.append(item);web_page['mainEntity']={'@id':url+'#article'}
 graph.append(web_page)
 ogtype='article' if article else 'profile' if path=='about.html' else 'website'
 robots='noindex,follow' if path=='404.html' else 'index,follow,max-image-preview:large,max-snippet:-1'
 fonts='https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&amp;family=Manrope:wght@400;500;600;700&amp;display=swap'
 head=f'''<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="{robots}"><meta name="author" content="Kirsten Antony, RN"><link rel="canonical" href="{url}"><meta name="theme-color" content="#173f3a"><meta property="og:type" content="{ogtype}"><meta property="og:locale" content="en_US"><meta property="og:site_name" content="Colorado Foot Care Nurse"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}images/kirsten-antony-social-share.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Kirsten Antony, RN — Colorado Foot Care Nurse"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{BASE}images/kirsten-antony-social-share.jpg"><meta name="twitter:image:alt" content="Kirsten Antony, RN — Colorado Foot Care Nurse"><link rel="icon" href="{p}favicon.ico"><link rel="apple-touch-icon" href="{p}apple-touch-icon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="{fonts}"><link rel="stylesheet" href="{p}css/site-refresh.css?v={VERSION}"><link rel="stylesheet" href="{p}css/articles.css?v={VERSION}"><link rel="stylesheet" href="{p}css/refinements.css?v={VERSION}"><script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')}</script><noscript><style>@media(max-width:960px){{.header-inner{{flex-wrap:wrap}}.menu-toggle{{display:none}}.primary-nav{{display:flex;position:static;flex-wrap:wrap;gap:14px;box-shadow:none;padding:10px 0;width:100%}}.primary-nav>a:not(.button){{border:0}}}}</style></noscript></head>'''
 main=doc.xpath('//main')[0]
 # Shared breadcrumbs are visible content as well as structured data.
 for old in main.xpath('.//nav[@class="breadcrumbs"]'):old.drop_tree()
 if path!='index.html':
  target=main.xpath('.//section[contains(@class,"page-hero")]//div[contains(@class,"shell")]')
  if target:target[0].insert(0,html.fragment_fromstring(breadcrumb_html(path,title.split(' | ')[0])))
 # Ensure author portraits are not interpreted as inline text images by older CSS.
 for image in main.xpath('.//img'):
  image.set('decoding','async')
  if path!='index.html' and 'reading-byline' not in (image.getparent().get('class') or ''):image.set('loading','lazy')
 for link in main.xpath('.//a'):
  if not link.text_content().strip() and not link.get('aria-label') and not link.xpath('.//img'):link.drop_tag()
 body=html.tostring(main,encoding='unicode')
 extras=f'<script src="{p}js/site-refresh.js?v={VERSION}" defer></script>'
 if article or path=='articles.html':extras+=f'<script src="{p}js/articles.js?v={VERSION}" defer></script>'
 if path=='service-areas.html':extras+=f'<script src="js/service-areas.js?v={VERSION}" defer></script>'
 file.write_text(f'<!doctype html>\n<html lang="en">{head}<body><a class="skip-link" href="#main">Skip to content</a>{header(path)}{body}{footer(path)}<a class="mobile-call button" href="tel:+13036688992">Call Kirsten · (303) 668-8992</a>{extras}</body></html>\n')

if __name__=='__main__':
 subprocess.run([sys.executable,str(ROOT/'scripts/build_articles.py')],check=True)
 paths=PRIMARY+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'articles').glob('*.html'))]+['404.html']
 for p in paths:process(p)
 redirects={'blog.html':'articles.html','single.html':'articles.html','styles.html':'index.html','generic.html':'index.html','images/index.html':'index.html','images/about.html':'about.html','images/contact.html':'contact.html','images/services.html':'services.html','images/blog.html':'articles.html','images/single.html':'articles.html','images/styles.html':'index.html','images/generic.html':'index.html'}
 for old,new in redirects.items():
  url=canon(new)
  (ROOT/old).write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(LABELS[new])} | Colorado Foot Care Nurse</title><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url={url}"><link rel="canonical" href="{url}"></head><body><p>This page has moved. <a href="{url}">Visit {esc(LABELS[new])}</a>.</p></body></html>\n')
 ns='http://www.sitemaps.org/schemas/sitemap/0.9';sitemap=etree.Element('urlset',nsmap={None:ns})
 for path in paths:
  if path=='404.html':continue
  u=etree.SubElement(sitemap,'url');etree.SubElement(u,'loc').text=canon(path);etree.SubElement(u,'lastmod').text=TODAY
 (ROOT/'sitemap.xml').write_bytes(etree.tostring(sitemap,xml_declaration=True,encoding='UTF-8',pretty_print=True))
 print(f'Built shared layout, canonical metadata and structured data for {len(paths)} pages; consolidated {len(redirects)} legacy URLs.')
