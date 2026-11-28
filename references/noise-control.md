# 颗粒噪点治理 · 决策树（V5）

> 背景：用户对「背景板颗粒」连续打回 3 次。前两次用后期平滑（floodfill、NL-means、大核高斯）都被判不合格，第三次换「抠图重造」才过。下面是能复用的判断与手法。

## 一、先判断颗粒从哪来

| 现象 | 来源 | 该走哪条 |
|---|---|---|
| 放大到 1:1 后背景出现均匀细白点/纸纹 | 生成模型自带水彩纸质感，被放大显形 | **原图级**：抠图重造背景（`hero-plate.md`） |
| 只有某几张区块图有颗粒 | 那几张是同批生成 | 逐张抠图或逐张局部平滑 |
| 全卡到处都有，尤其深色区 | JPEG 压缩 / 缩放重采样 | 导出用 PNG，别用 JPG 中转 |
| 页面灰底上有颗粒 | 图片外圈羽化不足、或页面底色没对齐 | 先对齐底色，再谈降噪 |

**判断方法**：裁 300×300 的 1:1 原尺寸块，看直方图标准差；平坦区 σ>6 基本就是颗粒。

## 二、三条路径，优先级从高到低

### 路径 A · 抠图重造背景（最彻底，推荐给主视觉）

见 `hero-plate.md`。适用于：主视觉、三视图这种「大片背景」的图。
优点：背景是程序生成的，**不可能有颗粒**；缺点：会丢原图的阴影，必须按 `hero-plate.md` §四 补回来。

### 路径 B · 局部背景平滑（省事，适用于只剩小片背景的区块图）

**核心：只磨「平坦背景区」，不动物件边缘。**

```python
flat = gaussian(gray, 5)                  # 局部均值
edge = |gray - flat| > 6                  # 梯度大的地方是边缘
mask = 亮区 & ~膨胀(edge, 14)             # 亮 + 平坦 + 离边缘 14px 以上
out  = mix(img, gaussian(img, 18), mask)  # 只在这些区域用大核
```

三档力度：`σ=10`（轻，留质感）/ `18`（中，推荐）/ `26`（重，会塑料感）。

实例：区块切图统一过一遍，角点 floodfill 判背景（从四角向内扩散，与角点色差 <10 视为背景），再叠上面的平坦区平滑。

### 路径 C · 整图轻度降噪（只在最后兜底）

`NL-means`（`cv2.fastNlMeansDenoisingColored`，h=3）或 PIL 的 `ImageFilter.SMOOTH`。**别单独用**，它会让薄纱、蕾丝一起变柔。

## 三、禁止

| 禁止 | 原因 |
|---|---|
| 对整张原图做大核（≥40px）模糊后当背景 | 人物轮廓外溢成雾，用户一眼看出「糊」 |
| 只降噪不换背景，反复调 σ | 纸纹是原图的，抹不干净，越抹越假 |
| 用 JPG 存中间产物 | 每次重存都加一层块状噪 |
| 拿「加了颗粒更有质感」当理由 | 用户明确把它定义为缺陷 |

## 四、验收口径

1. 1:1 裁图看：**背景平坦区无可见颗粒、物件边缘不糊、薄纱仍透光**。
2. 缩略图看：**背景不发灰、不发雾、没有一圈人形光晕**。
3. 四角与页面底色差 ≤5 阶。
4. 深色区（黑发、黑鞋）没有彩噪（RGB 三通道标准差接近）。

## 五、提示词侧预防（生成时就把背景做干净）

正向加：`clean seamless studio backdrop, smooth gradient background, soft contact shadow on floor, cinematic soft lighting, subtle rim light`
负向加：`noise, film grain, dirty background, jpeg artifacts, grain texture, rough surface, cluttered background, floating in the air, flat solid color background`

注意两句的取舍：
- `smooth gradient background` 要配 `soft contact shadow`，否则模型给纯平底、人悬空；
- 不要写 `pure white background`，白底会把浅色衣服吃掉轮廓。
