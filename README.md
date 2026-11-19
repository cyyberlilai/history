# Circular Head · History Book

An interactive digital sketchbook of **Circular Head**, on Tasmania's North West Coast — eleven watercolour plates, from the volcanic plug at Stanley to the mills, dairy works and abalone cannery at Smithton.

No build step, no framework, no external requests: a single static page that ships its own JavaScript, CSS, fonts and images.

---

## What it does

- **3D page turn.** The book is a real spread that tilts, lifts and turns as you drag or use the arrow keys — with ambient cast shadows and motion blur on the flipping leaf.
- **Loupe.** Hover to inspect the paper grain and brushwork at close range.
- **Zoom + ink density.** Step the spread from 100% up to 200%, and push the ink slider to deepen or lift the wash.
- **Save a page.** "Keep this page" exports the current spread as an image.
- **Pre-rendered spreads.** Each page is 1920×1080 canvas typography composed over a plate, baked once to WebP so first paint stays cheap.

## Contents

| № | Plate | Place |
|---|-------|-------|
| I | The Nut | Stanley · Bass Strait |
| II | Joseph Lyons | Stanley · Prime Minister |
| III | Lyons Cottage | Stanley · Alexander Terrace |
| IV | Enid Lyons | Born near Smithton · Federal Parliament |
| V | Highfield | Stanley · Highfield |
| VI | Cape Grim | Kennaook / Cape Grim · North West Tip |
| VII | McCain Foods | Smithton · McCain |
| VIII | Ta Ann | Smithton · Ta Ann |
| IX | Saputo Dairy | Smithton · Saputo |
| X | Greenham | Smithton · Greenham |
| XI | Tasmanian Seafoods | Smithton · Abalone cannery |

## Project structure

```
.
├── index.html            # the whole page — markup only, no inline logic
├── start.command         # double-click launcher: serves the site on :8787
├── assets/
│   ├── index-v47.js      # application bundle (plates data, book engine, UI)
│   ├── index-v54.css     # styles, @font-face declarations, layout
│   ├── waratah.webp      # endpaper / decorative artwork
│   └── favicon*.{svg,png}
├── fonts/                # 9 self-hosted woff2 files (no CDN calls)
├── pages/                # 11 pre-rendered spreads, 1920×1080 WebP
├── plates/               # 11 source plate paintings, WebP
├── tools/
│   └── build-pages.py    # bakes pages/*.webp from the live page via Playwright
└── .nojekyll             # tell GitHub Pages to serve files as-is
```

Files under `assets/` carry a version suffix (`index-v47.js`, `index-v54.css`). Only the pair referenced by `index.html` is live; older suffixes are historical snapshots kept for cache-busting rollbacks.

## Run it locally

Either double-click `start.command`, or:

```bash
python3 -m http.server 8787 --bind 127.0.0.1
# then open http://127.0.0.1:8787/
```

A server is required — opening `index.html` as a `file://` URL blocks module scripts and font loads.

## Regenerating the pages

Page copy lives in `assets/index-v47.js`. After editing it, re-bake the spreads:

```bash
pip install playwright && playwright install chromium
python3 -m http.server 8787 --bind 127.0.0.1   # in another terminal
python3 tools/build-pages.py
```

The script loads `http://127.0.0.1:8787/?build=1`, waits for `document.body.dataset.ready === '1'`, collects every 1920×1080 canvas, and writes them to `pages/` at quality 0.82.

## Deploy to GitHub Pages

Everything is relative-path and dependency-free, so a project site works without changes.

```bash
git init
git add .
git commit -m "Circular Head · History Book"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Then: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `(root)` → Save.** The site appears at `https://<your-username>.github.io/<repo-name>/` within a minute.

The `.nojekyll` file at the root stops Jekyll from post-processing the output — leave it in place. To serve from a custom domain, add a `CNAME` file containing the bare domain and point a DNS `CNAME` record at `<your-username>.github.io`.

## Credits

Paintings, writing and layout by **Shanmei Jin** — © [shanmei-jin.win](https://shanmei-jin.win).

Typefaces are all self-hosted and open-licensed (SIL Open Font License): IM Fell English, Cormorant Garamond, Instrument Serif, Newsreader, Caveat, LXGW WenKai (霞鹜文楷), Ma Shan Zheng (马善政).

---

## 中文简介

《Circular Head · History Book》是一本可交互的数字画册，收录塔斯马尼亚西北海岸 Circular Head 地区的十一幅水彩画——从 Stanley 的火山岩颈 "The Nut"，到 Smithton 的锯木厂、乳品厂与鲍鱼罐头厂。

页面支持拖拽翻页（3D 书页）、放大镜查看纸纹、100%–200% 缩放、墨色浓淡调节，以及当前跨页的图片导出。全部为静态文件：无框架、无构建步骤、无外部网络请求，字体与图片全部自托管。

本地预览：双击 `start.command`，或执行 `python3 -m http.server 8787 --bind 127.0.0.1`，然后访问 http://127.0.0.1:8787/ 。

部署：推送到 GitHub 后，在仓库 Settings → Pages 中选择 `main` 分支根目录即可。
