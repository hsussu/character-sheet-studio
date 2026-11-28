# 资料卡版式规格 · 平版（备选，不是默认）

> **默认骨架是 HUD 机能 UI 版**：`references/card-layout-hud.md` + `assets/card-skeleton-hud.html` + `scripts/build_card.py`。
> 这一份是 2026-11-27 霖云卡定稿时逐像素量出的平版（无编号块、无图格描边、纯留白），只在用户明确要「更素 / 不要 UI 感」时切换。
> 模板文件：`assets/card-skeleton-flat.html`。
> 单位一律 CSS px；渲染 `device_scale_factor=1.5`，成品 2160 × 2645（比例 0.817）。

## 1. 画布与栅格

| 项 | 值 |
|---|---|
| 画布宽 | 1440 CSS（输出 2160） |
| 页内边距 | 上 26 / 左右 32 / 下 22 |
| 主栅格 | `grid-template-columns:633px 1fr`，`column-gap:22` |
| 底色 | `body` 与 `.page` 同步设成主图背景采样值（霖云版 `#E9E9EC`） |
| 字体 | `"Noto Sans CJK SC", "Noto Sans SC"`，正文色 `#1A1720` |

**平版与 HUD 版最大差别**：平版图格底是 `#DDDCE4`（比页面底色暗一档，靠色差分区），没有 1px 描边、没有编号块、没有刻度线。

## 2. 左栏

| 元素 | 规格 |
|---|---|
| eyebrow | 9.5px / 字距 4 / `#A79EB4` |
| 主名 | 46px / weight 900 / 字距 4 / line-height 1.05 |
| 英文名 | 13px / 600 / 字距 5 / `#948BA4` |
| 身份标签 | 10px，左侧 1px 竖线 `#DCD6E6`，padding-left 12 |
| 引言 | 12px / line-height 1.9 / `#6E6478`，两行（第二行加 <br>） |
| `.stage` | height 966，`margin-top:4`，`overflow:visible` |
| `.hero` | width 700，`left:-40`，`top:14`，z-index 6，右侧 40px 渐隐 mask |
| 属性表 | 上面 1px 线 `#D6D2DC`；行 `grid-template-columns:66px 1fr`，padding 5.5/0，行线 `#DCD8E2`；值 11.5px，键 9.5px/字距 1.4 |
| chips | flex wrap，gap 7，上边距 14；胶囊 9.5px，边 `#D2CCDE`，底 `#F6F5F9`，radius 100 |
| 世界观块 | 上边距 14 + 1px 线 `#E4E0E9`；行 `grid-template-columns:56px 1fr`，10px / line-height 1.85 |
| 配色块 | 同上线；6 列等宽，gap 8；色块高 26 + 1px 边 `#D4CFDE`；标签 8px |
| 页脚 | 上边距 16，10px / line-height 1.9 / `#948BA4` |

## 3. 右栏（`flex column`，`row-gap:18`）

区块标题：左 padding 78，9.5px / 字距 2.4；中文 11px / 字距 2、英文去掉字重、右侧编号浅紫。

| # | 区块 | 图格高 | 网格 | 说明 |
|---|---|---|---|---|
| 01 | 多角度立绘 | 420 | 单图 + 三标签行 | 正/侧/背等距，脚底共线 |
| 02 | 头部细节 | 339 | `45fr 27.5fr 27.5fr` × 两行 168，gap 3 | 左大格跨两行 + 右 2×2 |
| 03 | 服装细节 | 236 | `repeat(5,1fr)` gap 3 | 平铺实物，无人体 |
| 04 | 配饰与道具 | 236 | `repeat(5,1fr)` gap 3 | 顺序锁死，缺类跳过 |
| 05 | 表情 | 152 | `repeat(6,1fr)` gap 3 | `object-position:50% 44%` |

图格统一：`background:#DDDCE4`，`overflow:hidden`，图 `width/height:100%`，`object-fit:cover`。

区块标签行：8.5px / 字距 1.4 / 居中，`margin-top:5`，列数与图格对齐。

签名区：`margin-top:auto` + 上 1px 线，右对齐两行（11px 字距 5 / 9px 字距 3）。

## 4. 必须手改的两处

1. `body` 与 `.page` 底色 = 主图背景采样值；不同就会在 hero 周围露方块边。
2. 主名、英文名、身份、引言、属性行、chips、世界观、配色、签名——全部换成当前角色内容，不留霖云字样。

## 5. 与 HUD 版的选择

| 情况 | 选哪个 |
|---|---|
| 用户要「以图一为标准」、机能感、编号 + 刻度 | HUD 版（默认） |
| 用户嫌 UI 太吵、要素净杂志感 | 平版 |
| 需要脚本一键渲染、缺项报警 | 只能 HUD 版（`scripts/build_card.py` 认 HUD 模板） |

平版目前只能手改 HTML，不走 `build_card.py`。
