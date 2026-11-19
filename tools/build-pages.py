#!/usr/bin/env python3
"""Bake the 11 composed book pages to ./pages/*.webp.

Run from the project root with the preview server on :8787:
    python3 tools/build-pages.py

The site renders each page by drawing the plate + canvas typography into a
1920x1080 canvas, then encoding it to WebP in the browser. Doing that at
runtime is the slowest part of the first load, so we do it once here and ship
the finished pages instead. Re-run this after changing any page copy.
"""
import base64, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "pages")
URL = "http://127.0.0.1:8787/?build=1"
QUALITY = 0.82

HOOK = """
window.__canvases = [];
const _create = document.createElement.bind(document);
document.createElement = function (tag, ...rest) {
  const el = _create(tag, ...rest);
  if (String(tag).toLowerCase() === 'canvas') window.__canvases.push(el);
  return el;
};
"""

def main():
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--use-gl=angle", "--use-angle=swiftshader"])
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.add_init_script(HOOK)
        pg.goto(URL, wait_until="domcontentloaded")
        pg.wait_for_function("document.body.dataset.ready === '1'", timeout=120000)
        ids = pg.evaluate("()=>[...document.querySelectorAll('.plate')].map(e=>e.dataset.id||'')")
        n = pg.evaluate("()=>window.__canvases.filter(c=>c.width===1920&&c.height===1080).length")
        print(f"captured {n} canvases")
        data = pg.evaluate(
            """(q)=>window.__canvases.filter(c=>c.width===1920&&c.height===1080).map(c=>c.toDataURL('image/webp', q))""", QUALITY)
        b.close()

    order = ["nut","lyons","cottage","enid","highfield","capegrim","mccain","taann","saputo","greenham","seafoods"]
    for i, durl in enumerate(data):
        raw = base64.b64decode(durl.split(",", 1)[1])
        name = f"{i+1:02d}-{order[i]}.webp"
        with open(os.path.join(OUT, name), "wb") as f:
            f.write(raw)
        print(f"  {name:<22} {len(raw)/1024:7.0f} KB")

if __name__ == "__main__":
    main()
