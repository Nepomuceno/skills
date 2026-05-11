# PNG Fallback Generation

Some viewers (older feed readers, slide decks, certain CI artifact previewers) render SVG poorly or not at all. Generate a PNG companion alongside `hero.svg` so the README has a fallback.

## Playwright script

```typescript
import { chromium } from 'playwright';
import { readFileSync } from 'fs';

const svg = readFileSync('hero.svg', 'utf-8');
const html = `<!DOCTYPE html>
<html><head>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>body{margin:0;padding:0;}</style>
</head><body>${svg}</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width: 1200, height: 430 },
  deviceScaleFactor: 2,
});
await page.setContent(html, { waitUntil: 'networkidle' });
await page.waitForTimeout(1000); // let webfont finish loading
await page.screenshot({
  path: 'hero.png',
  clip: { x: 0, y: 0, width: 1200, height: 430 },
});
await browser.close();
```

## Notes

- Match the `viewport` height and `clip.height` to the SVG `viewBox` height (e.g. 860 for multi-row ecosystems).
- `deviceScaleFactor: 2` produces a retina-ready 2400×860 PNG without changing the SVG layout.
- The 1-second `waitForTimeout` is a pragmatic delay for the Google Fonts stylesheet to finish loading; replace with a font-loaded check if your project already has one.
- Run it as a one-off (`bun run gen-hero.ts`) — there is no need to wire it into CI unless the SVG changes frequently.
