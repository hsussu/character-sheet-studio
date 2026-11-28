#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资料卡构建器（HUD 骨架 · V5）

用法：
    python3 build_card.py config.json            # 输出 PNG
    python3 build_card.py config.json --html     # 只生成 HTML，不渲染

config.json 最小结构：
{
  "out": "/abs/path/角色名-资料卡-01.png",
  "assets_dir": "/abs/path/切图目录",
  "accent": "#3F7F63",
  "page_bg": "#EDEDEE",
  "star": "#A9CBB5",
  "images": {"HERO":"hero_src_v3.png","TURN":"turn.png", ... },
  "text":   {"EYEBROW":"CHARACTER DESIGN　人物设定","NAME":"沈清栀","NO":"NO.001", ... },
  "rows":   [["姓　名","<b>沈清栀</b><span class='dim'>　女 · 19 岁</span>"], ...],
  "chips":  ["第七灯塔","守灯人", ...],
  "world":  [["阵　营","圣堂 · 第七灯塔（编号 7-04）"], ...],
  "palette":[["#F3F4F1","雪白棉府"], ...],
  "labels": {"turn":[...],"head":[...],"cost":[...],"acc":[...],"expr":[...]}
}

渲染：Playwright chromium，1440 CSS 宽 + device_scale_factor=1.5 → 2160 宽。
"""
import json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
SKELETON = os.path.join(HERE, "..", "assets", "card-skeleton-hud.html")
CHROMIUM = "/usr/local/bin/chromium"

LABEL_COLS = {"turn": 3, "head": 5, "cost": 5, "acc": 5, "expr": 6}


def escape(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_html(cfg):
    html = open(SKELETON, encoding="utf-8").read()

    # 1) 颜色全局替换
    html = html.replace("#3F7F63", cfg.get("accent", "#3F7F63"))
    html = html.replace("#EDEDEE", cfg.get("page_bg", "#EDEDEE"))
    html = html.replace("#A9CBB5", cfg.get("star", "#A9CBB5"))
    html = html.replace("#9FC0AC", cfg.get("star", "#A9CBB5"))

    # 2) 图片
    for key, fn in cfg.get("images", {}).items():
        html = html.replace("{{%s}}" % key, escape(fn))

    # 3) 结构化区块
    rows_html = "\n        ".join(
        '<div class="row"><div class="k">%s</div><div class="v">%s</div></div>' % (escape(k), v)
        for k, v in cfg.get("rows", []))
    html = html.replace("{{DATA_ROWS}}", rows_html)

    chips_html = "".join('<span class="chip">%s</span>' % escape(c) for c in cfg.get("chips", []))
    html = html.replace("{{CHIPS}}", chips_html)

    world_html = "\n      ".join(
        '<div class="wrow"><span>%s</span>%s</div>' % (escape(k), v)
        for k, v in cfg.get("world", []))
    html = html.replace("{{WORLD_ROWS}}", world_html)

    pal_html = "\n        ".join(
        '<div class="sw"><i style="background:%s"></i><span>%s</span></div>' % (c, escape(n))
        for c, n in cfg.get("palette", []))
    html = html.replace("{{PALETTE}}", pal_html)

    # 4) 标签行
    for grp in LABEL_COLS:
        labels = cfg.get("labels", {}).get(grp, [])
        span = "".join("<span>%s</span>" % escape(x) for x in labels)
        html = html.replace("{{%s_LABELS}}" % grp.upper(), span)

    # 5) 纯文本占位符
    for key, val in cfg.get("text", {}).items():
        html = html.replace("{{%s}}" % key, escape(val))

    # 6) 缺项检查：必填占位符没给值就报出来（缺图会渲染成空白格）
    left = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", html)))
    if left:
        print("!! 以下占位符没有配置值（会渲染成空白）：", ", ".join(left))
    html = re.sub(r"\{\{[A-Z0-9_]+\}\}", "", html)
    return html


def render(html_path, out_png):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROMIUM, args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1.5)
        pg.goto("file://" + os.path.abspath(html_path))
        pg.wait_for_timeout(500)
        h = pg.evaluate("document.body.scrollHeight")
        pg.set_viewport_size({"width": 1440, "height": int(h)})
        pg.screenshot(path=out_png, full_page=True)
        b.close()
    return out_png


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    html = build_html(cfg)
    out_png = cfg.get("out", "card.png")
    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    html_path = os.path.splitext(out_png)[0] + ".html"
    open(html_path, "w", encoding="utf-8").write(html)
    print("HTML:", html_path)
    if "--html" not in sys.argv:
        render(html_path, out_png)
        print("PNG :", out_png)
