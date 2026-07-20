# Plan: URLs individuales por propiedad (Vercel · Static HTML)

## Por qué importa para SEO
El sitio actual es una SPA de una sola URL (`sillaris.pe/`). Todas las propiedades
viven en JS — Google las ve con dificultad, no puede indexarlas por separado,
y no pueden aparecer en búsquedas como "oficina vucetich arequipa" o
"departamento la negrita precio". Con URLs propias cada propiedad compite
individualmente en Google.

## Arquitectura elegida: Multi-page static (sin framework)
Seguimos en HTML estático puro. Sin Next.js, sin build. Vercel sirve archivos
estáticos de la carpeta `public/`. Cada propiedad tiene su propio `.html`
con el contenido completo ya renderizado en el server (HTML inicial).

```
sillaris.pe/                          → index.html (home SPA actual)
sillaris.pe/propiedades/              → propiedades/index.html
sillaris.pe/propiedades/oficina-vucetich/     → propiedades/oficina-vucetich/index.html
sillaris.pe/propiedades/departamento-umacollo/
sillaris.pe/propiedades/vallejo-35/
sillaris.pe/propiedades/vallejo-65/
sillaris.pe/propiedades/vallejo-85/
sillaris.pe/propiedades/local-comercial-vallejo/
sillaris.pe/propiedades/casa-empresarial-la-negrita/
sillaris.pe/propiedades/casa-av-ugarte/
sillaris.pe/blog/comprar-departamento-arequipa-guia/
sillaris.pe/blog/mejores-zonas-vivir-arequipa/
... (un .html por artículo)
```

## Estructura de carpetas
```
Sillaris/
├── index.html              ← home (SPA actual, sin cambios)
├── vercel.json
├── robots.txt
├── sitemap.xml             ← actualizar con las nuevas URLs
├── llms.txt
├── propiedades/
│   ├── index.html          ← listado de todas las propiedades (SSG)
│   ├── oficina-vucetich/
│   │   └── index.html
│   ├── departamento-umacollo/
│   │   └── index.html
│   └── ... (una carpeta por propiedad)
└── blog/
    ├── index.html
    └── comprar-departamento-arequipa-guia/
        └── index.html
```

Con `"cleanUrls": true` en `vercel.json` (ya configurado), Vercel sirve
`/propiedades/oficina-vucetich/index.html` en la URL
`sillaris.pe/propiedades/oficina-vucetich` (sin .html, sin trailing slash).

## Template de página de propiedad (lo que va en cada index.html)

Cada página de propiedad comparte el shell (nav, footer, estilos) pero tiene:

### `<head>` específico
```html
<title>Oficina en venta Parque Industrial Arequipa · Edificio Vucetich — SILLARIS</title>
<meta name="description" content="Oficina corporativa 52 m² en Edificio Vucetich,
  Parque Industrial Arequipa. Desde USD 79,050. Disponible venta y alquiler. Visita coordinada.">
<link rel="canonical" href="https://sillaris.pe/propiedades/oficina-vucetich/">
```

### JSON-LD específico (Product / Apartment / RealEstateListing)
```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateListing",
  "name": "Oficina Edificio Vucetich",
  "description": "Oficina corporativa 52 m² en Parque Industrial, Arequipa.",
  "url": "https://sillaris.pe/propiedades/oficina-vucetich/",
  "address": { "@type": "PostalAddress", "addressLocality": "Parque Industrial, Arequipa" },
  "offers": {
    "@type": "Offer",
    "price": "79050",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://sillaris.pe/" },
      { "@type": "ListItem", "position": 2, "name": "Propiedades", "item": "https://sillaris.pe/propiedades/" },
      { "@type": "ListItem", "position": 3, "name": "Oficina Edificio Vucetich" }
    ]
  }
}
```

### Contenido HTML estático (no renderizado por JS)
- H1 con keyword principal ("Oficina en venta Parque Industrial Arequipa")
- Descripción, características, precios, FAQs — todos en HTML puro
- Botón de WhatsApp directo
- Breadcrumb visible (nav secundario)
- Link "← Volver a propiedades" y links a propiedades relacionadas

## Cómo generar las páginas (sin build tool)

### Opción A: Script Python generador (recomendado)
Un script `generate.py` lee la data de propiedades (extraída de `sillaris-web.html`)
y produce los archivos `.html` estáticos. Se corre localmente antes de hacer deploy.

```bash
python generate.py   # genera propiedades/ y blog/
# luego git push → Vercel auto-deploya
```

El script reemplaza tokens en un template HTML:
```
{{PROP_TITLE}}, {{PROP_DESC}}, {{PROP_PRICE}}, {{SEO_TITLE}}, {{CANONICAL}} ...
```

### Opción B: Copiar-pegar manual (8 propiedades = factible)
Duplicar un template HTML y editar los datos. Apropiado si las propiedades
cambian poco.

## Actualizar el home SPA
Cuando el usuario hace click en una propiedad desde el home, en lugar de `showSingle(id)`:
```js
// Antes:
onclick="showSingle('vucetich')"

// Después:
onclick="window.location='/propiedades/oficina-vucetich/'"
```
Así el home sigue siendo SPA para UX fluida, y la URL de propiedad es navegable
y compartible directamente.

## Actualizar sitemap.xml
Agregar cada URL de propiedad y artículo de blog al `sitemap.xml` con
`<priority>0.9</priority>` para propiedades y `0.7` para blog.

## Prioridad de implementación
1. **8 páginas de propiedades** — impacto directo en búsquedas de compra/alquiler
2. **Página listado** `/propiedades/` — captura búsquedas genéricas
3. **6 artículos de blog** — captura búsquedas informacionales (mejores zonas, guías)

## Effort estimado
- Template HTML + script generador: ~2h
- 8 páginas generadas y revisadas: ~1h
- Sitemap actualizado: 15min
- Deploy en Vercel: automático con git push
