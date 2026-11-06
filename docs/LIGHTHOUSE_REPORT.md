# Step 5 - Lighthouse Audit & Documented Improvements

**Project:** Portfolio site optimization  
**Author:** Pratiksha Bhende  

## 1. What was optimized

| Step | Action | Result |
|------|--------|--------|
| 1 | Generated minified CSS/JS (Terser + csso, or `scripts/minify.py` offline) | `css/style.min.css`, `js/script.min.js` |
| 2 | Replaced originals with minified files in HTML | `index.html` links `style.min.css` and `script.min.js` (with `defer`) |
| 3 | Compressed and resized images (JPEG -> WebP, quality 78), updated `src` | `images/*.webp` |
| 4 | Added `loading="lazy"` to below-the-fold images | About + 3 project images |
| 5 | Ran Lighthouse before/after | See section 3 |

## 2. Measured file-size savings (from `npm run report`)

```
File                        Before       After    Saved
style.min.css               5.1 KB      3.6 KB    29.0%
script.min.js               1.5 KB      1.0 KB    38.1%
profile.webp              644.0 KB      6.5 KB    99.0%
about.webp                709.0 KB      9.0 KB    98.7%
project-1.webp            893.6 KB      7.1 KB    99.2%
project-2.webp            898.7 KB      7.6 KB    99.2%
project-3.webp            895.7 KB      7.2 KB    99.2%
TOTAL                    4047.6 KB     42.0 KB    99.0%
```

> The bundled sample images are generated gradients, so their savings look extreme.
> With real photos expect roughly 60-90% savings. Re-run `npm run report` after swapping in your own images.

## 3. Lighthouse scores - fill in after running the audit

Run on `index.original.html` (BEFORE) and `index.html` (AFTER), Mobile mode, in an Incognito window.

| Metric | Before | After |
|--------|--------|-------|
| Performance score | ___ | ___ |
| First Contentful Paint (FCP) | ___ s | ___ s |
| Largest Contentful Paint (LCP) | ___ s | ___ s |
| Total Blocking Time (TBT) | ___ ms | ___ ms |
| Cumulative Layout Shift (CLS) | ___ | ___ |
| Total page weight | ___ KB | ___ KB |
| Accessibility / Best Practices / SEO | ___ | ___ |

### How to run Lighthouse
1. Start a local server: `npx serve .` (or VS Code Live Server).
2. Open `http://localhost:3000/index.original.html` in Chrome -> DevTools (F12) -> **Lighthouse** tab.
3. Choose **Mobile**, tick **Performance**, click **Analyze page load**. Note the scores above.
4. Repeat for `http://localhost:3000/index.html`.
5. Optionally export each report (Lighthouse menu -> Save as HTML).

## 4. Why each change helps

- **Minification** removes comments and whitespace, so fewer bytes to download and parse.
- **WebP + resizing** images were the largest part of the page; serving them at display size cuts transfer dramatically.
- **`loading="lazy"`** defers off-screen images until the user scrolls near them, which lowers initial load.
- **Hero image is NOT lazy** and uses `fetchpriority="high"` + `<link rel="preload">`, because lazy-loading the LCP image makes LCP worse.
- **`width`/`height` attributes** reserve space, preventing layout shift (CLS).
- **`defer` on the script** keeps JavaScript from blocking first paint.
