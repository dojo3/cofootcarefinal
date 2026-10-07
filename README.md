# Colorado Foot Care Nurse

Static website for Kirsten Antony, RN, published through GitHub Pages at https://coloradofootcarenurse.com/.

## Editing and building

The main HTML pages contain the editable page content. `data/articles.json` preserves the complete recovered article text and source links. Do not replace historical articles with summaries or update their publication dates when changing formatting.

After editing page content or the article templates, run:

```sh
python -m pip install lxml
python scripts/build_site.py
python tests/validate_site.py
```

`scripts/build_articles.py` generates the article collection and 41 reading pages. `scripts/build_site.py` then applies shared navigation, footer, canonical URLs, author/business/breadcrumb structured data, share metadata and the sitemap. It also maintains redirects from the old template and duplicate URLs. Commit the generated HTML along with its source changes. GitHub Pages serves these files directly; no JavaScript framework or build service is required by visitors.

Styles are in `css/site-refresh.css`, `css/articles.css` and `css/refinements.css`. Font loading is declared in the shared document head. Increment the asset version in `scripts/build_site.py` when changing CSS or JavaScript.

## Checks

`tests/validate_site.py` checks all 47 indexable pages, complete article text, current prices, author references, canonical URLs, local links, structured data, image dimensions, the sitemap and legacy redirects.

`tests/site_preview.html` is a noindex developer preview for checking the real pages inside 320, 390, 768 and 1280 pixel viewports. It is not linked from the visitor navigation or sitemap. Check navigation, search, price selection and long article pages after publishing.

## Pricing and search metadata

Prices are shown in `services.html`, `index.html` and `service-areas.html`; the city finder is in `js/service-areas.js`. Keep the offers in the services page structured data and `llms.txt` consistent when prices change. Couples discounts are quoted individually; no fixed couples rate is published.

The business provides mobile care. Do not invent a public street address, review rating, certification or medical claim for structured data. Historical article dates are preserved. Search Console verification and a Google Business Profile are managed separately from this repository.
