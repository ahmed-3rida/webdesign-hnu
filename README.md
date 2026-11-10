# Web Design Pixel Quest

موقع مذاكرة لمادة **Web Design** (Multimedia Software)، بستايل pixel art ومعاه Light و Dark mode:
شرح المحاضرات الخمسة بالعربي والمصطلحات إنجليزي، كويز تدريبي على كل محاضرة، واختبار شامل بيتولد مختلف كل مرة.

Made by [Ahmed Salman](https://dev.uniskills.pro/).

## Features

- 5 lessons with exam tips, comparison tables and small interactive demos (12-column grid, 8px spacing).
- A practice quiz per lecture (answer and explanation after every question, options shuffled each attempt).
- A final exam generated from a bank of about 250 questions: 30 questions, 6 per lecture, random order and shuffled options.
  Every exam has a 6-character code, so two people can take the same exam.
- Light and dark modes (Auto follows the device) with 6 color palettes per mode: Arcade, Matcha, Ocean, Sunset, Sakura, Mono.
  An Arabic font picker offers Cairo (default), Tajawal, Readex Pro, Noto Kufi Arabic and IBM Plex Sans Arabic.
  Choices are saved on the device. Palettes live in `tools/palettes.py`; edit there and run `python3 tools/palettes.py`.

## Structure

| Path | What it is |
|------|------------|
| `src/index.html` | The whole app in one file (lessons, question bank, exam generator, character, styles). Edit this. |
| `tools/build.js` | Builds the SEO-ready static site from `src/index.html`. |
| `site/` | Built output, ready to deploy (12 pages, sitemap, robots, OG image, icons). |

## Build

```bash
npm install
npx playwright install chromium
npm run build:site -- https://webdesign-hnu.vercel.app
```

The domain argument is used for canonical URLs, Open Graph tags and the sitemap.

## Deploy

The built files in `site/` are committed, so hosts only need to serve that folder.

- **Vercel:** works as-is through `vercel.json` (no install, no build, output `site`).
- **Netlify / Cloudflare Pages:** set the publish directory to `site` and leave the build command empty.

Run `npm run build:site` locally and commit `site/` whenever `src/index.html` changes.
