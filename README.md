# Sitekeeper test site

Synthetic static site used for live end-to-end checks of Sitekeeper's
`static_git` adapter (text edits, photo replacement, booking widget).
All content is fictional. Served by GitHub Pages at https://ertad-family.github.io/.

Layout: `site/content/<lang>/<slug>.html` (header lines, `---`, body),
`site/content/<lang>/_site.html` header/footer texts, `site/media/` images.
`python3 site/build.py` builds into `out/`; the Pages workflow deploys on push to main.
