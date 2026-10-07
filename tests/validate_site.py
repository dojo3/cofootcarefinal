"""Content-preservation, pricing, crawlability and link checks for the static site."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote
from lxml import html, etree

ROOT=Path(__file__).resolve().parents[1]
BASE='https://coloradofootcarenurse.com/'
articles=json.loads((ROOT/'data/articles.json').read_text())
assert len(articles)==42
audit=json.loads((ROOT/'data/clipping-audit.json').read_text())
assert len(audit['photos'])==29
assert all(any(a['slug']+'.html'==Path(p['path']).name for a in articles) for p in audit['photos'])
paths=['index.html','about.html','services.html','contact.html','service-areas.html','articles.html']+['articles/'+a['slug']+'.html' for a in articles]
titles=set();descriptions=set();canonical=set()
for path in paths:
 doc=html.parse(str(ROOT/path))
 assert len(doc.xpath('//h1'))==1,path
 title=doc.xpath('//title/text()')[0];assert title not in titles,(path,'duplicate title');titles.add(title)
 desc=doc.xpath('//meta[@name="description"]/@content')[0];assert desc not in descriptions,(path,'duplicate description');descriptions.add(desc)
 url=doc.xpath('//link[@rel="canonical"]/@href')[0]
 assert url==BASE+('' if path=='index.html' else path),path
 assert url not in canonical;canonical.add(url)
 assert 'noindex' not in doc.xpath('//meta[@name="robots"]/@content')[0]
 graph=json.loads(doc.xpath('//script[@type="application/ld+json"]/text()')[0])['@graph']
 assert any(n.get('@id')==BASE+'#kirsten' and n.get('url')==BASE+'about.html' for n in graph)
 assert any(n.get('@id')==BASE+'#business' and len(n['areaServed'])==16 for n in graph)
 if path!='index.html':
  crumbs=next(n for n in graph if n['@type']=='BreadcrumbList')
  assert crumbs['itemListElement'][-1]['item']==url
  assert doc.xpath('//nav[@aria-label="Breadcrumb"]')
 for link in doc.xpath('//@href | //@src'):
  parsed=urlparse(link)
  if parsed.scheme or parsed.netloc or not parsed.path:continue
  target=ROOT/parsed.path.lstrip('/') if parsed.path.startswith('/') else ROOT/Path(path).parent/unquote(parsed.path)
  assert target.exists(),(path,link)
  if parsed.fragment and target.suffix=='.html':
   linked=html.parse(str(target));assert linked.xpath('//*[@id=$name]',name=parsed.fragment),(path,link,'missing fragment')
 for image in doc.xpath('//img'):
  assert image.get('alt') is not None,(path,'missing image alternative')
  assert image.get('width') and image.get('height'),(path,'missing image dimensions')
 for a in doc.xpath('//a'):
  assert a.text_content().strip() or a.get('aria-label') or a.xpath('.//img[@alt]'),(path,'empty link')

def norm(s):return re.sub(r'\s+','',s)
for a in articles:
 doc=html.parse(str(ROOT/'articles'/(a['slug']+'.html')))
 body=doc.xpath('//article[@class="article-prose"]')[0]
 preserved=html.fragment_fromstring(a['body_html'],create_parent='div')
 assert norm(body.text_content())==norm(preserved.text_content()),(a['slug'],'changed article text')
 assert not body.xpath('.//script | .//iframe'),a['slug']
 graph=json.loads(doc.xpath('//script[@type="application/ld+json"]/text()')[0])['@graph']
 item=next(x for x in graph if x['@type']=='Article')
 assert item['author']['@id']==BASE+'#kirsten'
 assert 'dateModified' not in item,'Do not imply historical health advice was clinically updated.'

prices=html.parse(str(ROOT/'services.html'))
actual=[(' '.join(n.xpath('.//dt')[0].text_content().split()),' '.join(n.xpath('.//dd')[0].text_content().split())) for n in prices.xpath('//dl[@class="area-prices"]/div')]
assert [re.search(r'\$\d+',v)[0] for _,v in actual]==['$90','$100','$110','$115'],actual
assert 'starting at' in actual[0][1]
text=prices.xpath('//main')[0].text_content()
assert 'Fingernail trimming and filing' in text and '$20' in text
assert 'Discounts are available for couples' in text
assert not re.search(r'\$10\b|trip fee|travel charge',text,re.I)
legacy=['blog.html','single.html','styles.html','generic.html']+[str(p.relative_to(ROOT)) for p in (ROOT/'images').glob('*.html')]
for path in legacy:
 doc=html.parse(str(ROOT/path));assert doc.xpath('//meta[@name="robots" and contains(@content,"noindex")]'),path
 assert doc.xpath('//meta[@http-equiv="refresh"]'),path
sitemap=etree.parse(str(ROOT/'sitemap.xml'))
assert set(sitemap.xpath('//*[local-name()="loc"]/text()'))==canonical
assert 'Sitemap: '+BASE+'sitemap.xml' in (ROOT/'robots.txt').read_text()
print(f'PASS: {len(paths)} indexable pages; {len(articles)} complete articles; exact prices; valid metadata, sitemap, links and image dimensions; {len(legacy)} legacy redirects.')
