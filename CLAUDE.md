# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`sillaris-web.html` is a **single, self-contained static website** for SILLARIS Desarrollo Urbano — a real-estate agency in Arequipa, Peru. There is no build system, package manager, framework, or dependency: HTML, CSS (`<style>`), and JavaScript (`<script>`) all live in the one file. Spanish (`lang="es"`, locale `es_PE`) is the site language; keep all user-facing copy in Spanish.

## Running / previewing

Open `sillaris-web.html` directly in a browser, or serve it for a clean origin:

```bash
python -m http.server 8000   # then open http://localhost:8000/sillaris-web.html
```

There are no tests, no lint, and no build step. "Deploy" = publish this single HTML file.

## Architecture

It is a **client-side SPA built without a framework**. Key consequences any change must respect:

- **Pseudo-pages, one URL.** Sections with class `.page` (`#page-home`, `#page-props`, `#page-proyecto`, `#page-blog`, `#page-contacto`, `#page-single`) are toggled via `showPage(name)`, which swaps the `.active` class. Navigation uses `onclick="showPage(...)"` with `href="#"` — there is no router and no per-page URL. Deep links / history are not wired up.
- **Content is data-driven and rendered by JS.** The arrays `props` (property listings) and `blogs` (articles) near the top of the `<script>` are the source of truth. Render functions build HTML from them: `renderHome`, `renderProps`, `renderBlog`, `renderVallejo`, `renderCard`, `renderBlogCard`, and `showSingle(id)` for the property detail view. To add/edit a property or article, edit the data object — do not hand-write card markup.
- **Each property object** carries display fields plus `desc`, `benefits[]`, `faqs[]` (Q/A pairs rendered into the detail page), and a `seoKw` string. `prices[]` is the price-breakdown table; `feats[]` are the chips.
- **No real images.** Property/blog visuals are CSS `linear-gradient` backgrounds with an emoji `icon`, stored in the data (`color`, `icon`). There are no `<img>` assets.
- **Conversion is WhatsApp-first.** Forms do not POST anywhere. `submitLeadForm()` and `submitContact()` assemble a message and open `wa.me/${PHONE}`. `PHONE` (`51913177975`) is defined once at the top of the script — change it there. `waMsg()` / `contactWhatsApp()` build the prefilled messages.
- **Styling is a CSS custom-property design system.** The `:root` block (cream/stone/accent palette, shadows, radius, `--transition`) drives the whole look; reuse these variables instead of hard-coded colors. Typography is system fonts only (Georgia serif headings, Segoe UI body) — no web fonts to load.
- Scroll-reveal animations use a single `IntersectionObserver`; FAQ accordions use `toggleFaq(i, prefix)`; toasts use `showToast()`.

## SEO notes

`<head>` already contains title, meta description, keywords, canonical, Open Graph, and a `RealEstateAgent` JSON-LD block. Because the site is a JS-rendered SPA on one URL, be aware that property/blog/detail content is **not in the initial HTML** and pseudo-pages share a single canonical URL — relevant when reasoning about indexation, structured data, sitemaps, or per-listing rich results.
