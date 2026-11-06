# Portfolio Site - Performance Optimized

**Author:** Pratiksha Bhende - [github.com/pratiksha0604](https://github.com/pratiksha0604)

Task: *Optimize the portfolio site: minify assets, compress images, and add lazy loading.*

## Project structure

```
portfolio-optimized/
├── index.html              <- AFTER: optimized page (use this one)
├── index.original.html     <- BEFORE: unoptimized page (for Lighthouse comparison)
├── css/
│   ├── style.css           <- readable source
│   └── style.min.css       <- minified build
├── js/
│   ├── script.js           <- readable source
│   └── script.min.js       <- minified build
├── images-original/        <- uncompressed originals
├── images/                 <- compressed WebP images used by index.html
├── scripts/                <- minify.py, make_images.py, size_report.py
├── docs/LIGHTHOUSE_REPORT.md
├── package.json
└── .gitignore
```

## Run it
Open `index.html` in a browser, or run a local server:
```bash
npx serve .
```

## The 5 steps (and where they live)

1. **Minify CSS and JS** - with Terser and csso:
   ```bash
   npm install
   npm run build
   ```
   No internet? Use the bundled script: `npm run build:offline` (or `python3 scripts/minify.py`).
   Minified files are already included.
2. **Use the minified files in HTML** - `index.html` loads `css/style.min.css` and `js/script.min.js`.
3. **Compress images** - run originals through an optimizer (Squoosh.app / TinyPNG, or `python3 scripts/make_images.py --compress-only`), save into `images/`, and point the `src` attributes at them.
4. **Lazy loading** - `loading="lazy"` is on the About and Project images. The hero image is intentionally eager because it is above the fold.
5. **Lighthouse audit** - follow `docs/LIGHTHOUSE_REPORT.md`, fill in the before/after scores.

## Use your own images
Put your photos in `images-original/` as `profile.jpg`, `about.jpg`, `project-1.jpg`, `project-2.jpg`, `project-3.jpg`, then:
```bash
python3 scripts/make_images.py --compress-only
npm run report
```

## Push to GitHub
```bash
cd portfolio-optimized
git init
git add .
git commit -m "Optimize portfolio: minify assets, compress images, lazy loading"
git branch -M main
git remote add origin https://github.com/pratiksha0604/portfolio-optimized.git
git push -u origin main
```
(Create the empty `portfolio-optimized` repo on GitHub first, without a README.)
