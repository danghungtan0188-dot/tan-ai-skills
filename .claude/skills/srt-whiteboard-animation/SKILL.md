---
name: srt-whiteboard-animation
description: 将 SRT 字幕做成暖米黄纸张底的白板手绘动画：读字幕→输出配图策略→确认后生成统一风格线稿→按叙事语义标注分区→预览台调整→渲染 MP4。编排沿用分区遮罩揭示（annotation.json / sequence / startMs / protectedRegions），但每个区域内的落墨换成 stream 的连续笔迹（骨架/网格 ink→color）。当用户提供 SRT 字幕并要求"字幕做成白板手绘/流式笔迹视频""SRT 生成白板动画""按字幕分镜画手绘"时触发。
---

# SRT 白板动画（mask 编排 + stream 画法）

## Tan AI Skills 集成说明

本目录基于上游 MIT 项目，来源与导入 commit 见 [UPSTREAM.md](UPSTREAM.md)。此处的本地集成默认遵循 `tan-ai-skills/CLAUDE.md`：用户明确要求完整制作时，不要在每个非破坏性步骤后重复停下来等确认；先给分镜方案供确认，再连续完成线稿、标注、渲染和质检。只有用户要求分阶段确认、输入缺失/有歧义，或下一步会覆盖文件/产生外部付费时才暂停。用户明确选择逐步协作时，按上游逐步确认流程执行。

若需自行生成白板插画，可选择本地 [ComfyUI 辅助流程](references/comfyui-local-assets.md)。ComfyUI 不是本目录的依赖，也不需要 API；用户可用已有图像生成工具或自备线稿继续流程。

把 SRT 字幕转成白板手绘动画：**编排**沿用分区遮罩揭示（按叙事顺序逐区域揭示、未开始区域完全隐藏、重叠用 `protectedRegions` 保护）；**画法**换成流式笔迹——每个区域在自己的允许掩码内，笔尖沿骨架/网格连续滑行落墨（起笔 ink → 添彩 color），所有区域共享一张持久画布，已画完的区域保留在画布上。所有面向用户的说明、分镜、配置和界面文字必须使用中文。

与逐格跳变或矩形擦除不同：本 skill 的笔迹是**连贯流动**的；与整图 stream 不同：本 skill 按**字幕叙事分区**依次作画，可控制每个元素的出场顺序与时序。

## 默认实现参数

| 项目 | 默认要求 |
|---|---|
| 纸张背景 | 生成图使用暖米黄旧纸色（建议 `#F5EBD7`）；渲染时从原图距四角内缩取样染底，禁止纯白。 |
| 画法 | 每区域 stream 连续笔迹：起笔 `ink`（铺线稿）→ 添彩 `color`（还原原色）；权重 `ink:color = 2:1`。 |
| 笔迹路径 | `--ink-path grid`（网格，默认，稳）或 `skeleton`（骨架追踪，线稿清晰的插画更贴合）。 |
| 上色风格 | `--color-fill contour-wipe`（轮廓扫描，默认）或 `brush`（沿轨迹刷）。 |
| 未绘制区域 | 区域的允许掩码 = 矩形 `region` 扣除「后续区域 + protectedRegions」；未开始区域完全隐藏。 |
| 时长来源 | 每张图的 `sceneDurationMs` 来自该幕字幕的时间跨度（建议 25–35 秒/幕）。 |
| 编辑框 | 预览台默认显示全部编号编辑框；编辑框不属于动画画面内容。 |

## 统一出图视觉规范（强制）

所有场景的源图必须遵循同一套视觉语言；生成前把以下要求完整写入出图提示词，生成后逐条检查：

- **风格与构图：** 极简手绘插图、纯素描草图风格、类似 Notion 的克制涂鸦美学。以概念表达为主，不追求写实；构图简洁、背景干净、大量留白，整体情感平和、清晰，系列内线条/人物/配色一致。
- **颜色与材质：** 米色纸张背景 `#F5EBD7`、深灰色草图线条；仅可用红色、橙色、蓝色 作少量概念性点缀。不得使用其他强调色、高饱和度配色或复杂纹理。
- **人物与对象：** 对象以简洁轮廓、少量线条和留白表达，强调关系/变化/核心概念，而非真实比例、材质与细节。
- **绝对禁止：** 场景源图中的任何文字、词语、字母、数字、字体或标签；写实感、摄影细节、3D 效果、绘画质感；复杂场景、密集背景、繁复装饰和高饱和度画面。
- **绘制手部例外：** 若用户明确说明笔杆上的文字是其标识并要求保留，可保留 `drawing-hand.png` 笔杆上的标识；它不属于场景源图文字，也不需要清除或重绘。未获得用户明确说明时，仍按无文字画面处理。

## Xác nhận và nhịp làm việc

- Mặc định chỉ dừng ở **phân cảnh/kế hoạch hình ảnh** để người dùng duyệt. Sau khi được duyệt, tiếp tục chuẩn bị line art, annotation, preview và render; không hỏi xác nhận lặp lại sau từng thao tác không phá hủy.
- Nếu người dùng nói muốn làm từng bước, hãy chờ duyệt ở các mốc: line art, annotation/preview và bản render cuối.
- Dừng hỏi khi thiếu SRT/hình cần thiết, nội dung có điểm không rõ, cần ghi đè file, hoặc bước tiếp theo sẽ gọi dịch vụ trả phí/cloud.
- Sau khi tạo annotation, mở preview bằng Chrome/Edge nếu có thể. Nếu không thể điều khiển trình duyệt, xuất ảnh preview và báo rõ cách mở `assets/preview.html`; không tuyên bố đã mở hoặc lưu nếu chưa làm thật.

## 工作流程

1. **读字幕、出策略（不生成图片）。** 用 `scripts/parse_srt.py` 把 SRT 解析成字幕条并按 25–35 秒/幕给出建议分镜。据此输出配图策略：每幕的场景编号、核心表达、画面主体、对应字幕区间与 `sceneDurationMs`。每幕只表达一个核心意思。**先让用户确认策略，再继续默认的端到端流程。**
2. **生成线稿。** 按“统一出图视觉规范”逐幕生成 16:9 暖米黄旧纸张底线稿图，背景 `#F5EBD7`，主体之间保留充足留白便于自动拆分；不得生成文字、复杂照片、重叠对象或与规范冲突的元素。若用户选择逐步协作，在此展示线稿并等待确认。
3. **先读字幕再看图，然后标注并打开预览台。** 先阅读该图对应的字幕、再实际查看图片、并获取原图像素宽高；不得只凭字幕臆测画面，也不得只按画面位置机械排序。提炼字幕叙事事件，再把图中可见主体对应到事件，按“场景铺垫 → 关键人物/物体 → 动作冲突或变化 → 反应/结果”的语义顺序安排绘制。创建 `<图片名>.annotation.json` 后，尝试用 Chrome/Edge 打开 `assets/preview.html` 并载入项目目录；若用户选择逐步协作，在此等待确认。
4. **生成区域预览图。** 用 `render_annotation_preview.py` 出编号/方向检查图，核对分区与叙事顺序一致、区域都在画布内、重叠主体用 `protectedRegions` 保护。
5. **在预览台调整并保存。** 若预览台可用，检查并调整区域/顺序/时序/字幕：矩形代理的四边四角可改 `region`，右侧可改名称/方向/开始/结束与字幕，列表可调顺序。保存回原 `.annotation.json`；若无法使用预览台，调整 JSON 后再次生成并检查区域预览图。逐步协作模式在此等待确认最终标注。
6. **命令行渲染成片。** 用 `render_stream_whiteboard.py` 逐幕输出 MP4，抽查开场、重叠模块中段和结尾三个时间点。
7. **多幕合并（仅适用于多幕）。** 用 `merge_scenes.py` 按分镜顺序合并；质检字幕/画面顺序、遮罩泄露、笔迹流畅度、结尾停留和音画同步后交付。逐步协作模式在此等待用户确认最终视频。

## 目录约定

在用户项目中创建：

```text
assets/whiteboard/<项目名>/
  scene-01-<名称>.png
  scene-01-<名称>.annotation.json     # 与 png 同名
  scene-01-<名称>-whiteboard.mp4      # 成片
  scene-01-<名称>-preview.mp4         # 真实片段（预览台生成，低清）
```

图片与配置必须同名：`foo.png` 对应 `foo.annotation.json`。预览台据此自动加载配置。

## 语义排序与像素级标注（必须执行）

1. **阅读依据：** 标注前必须同时具备字幕与已查看的原图。缺任一项先索取，不得生成标注。
2. **顺序依据：** `sequence`、`startMs` 与 `label` 必须反映字幕中的事件先后，而非仅按从左到右、从上到下或视觉显眼程度。
3. **坐标依据：** 每个模块输出原图坐标系的整数像素 `x`、`y`、`width`、`height`；原点左上角，禁止百分比/比例/估算坐标或省略尺寸。`canvas.width`/`canvas.height` 必须等于原图像素尺寸。
4. **模块字段：** 每个元素含 `sequence`、`narrativeRole`、`subtitle`、`region`、`reveal`、`handPath`。`narrativeRole` 用中文说明其在字幕中的叙事作用；`subtitle` 存该区域对应的字幕文本（来自 SRT，供预览台联动与后续用途）；`sequence` 从 1 起连续。
5. **校验：** 生成预览前检查每个区域是否在画布内、是否覆盖对应可见主体、是否与字幕事件相符；重叠主体用 `protectedRegions` 保护后绘制模块。

## 时序模型（stream 画法专用）

- **每幕总时长** `sceneDurationMs` 来自该幕字幕时间跨度（`parse_srt.py` 的 `scenes[].sceneDurationMs`）。
- **区域串行作画：** stream 画法是一支笔在动，同一幕内各区域应**在时间上依次进行**（`startMs` 不重叠）：下一区域从上一区域 `startMs + durationMs`（+ 可选 100–300ms 呼吸）开始。若 `startMs` 重叠，渲染器仍按顺序处理，但视觉上不再是并发。
- **区域内 ink→color：** 每个区域的 `durationMs` 会按 `ink:color = 2:1` 切成起笔段和添彩段。`durationMs` 由预览台的**开始/结束时间**决定（结束−开始），可对齐该区域对应字幕的时长；也可用 150 像素/秒 × 绘制距离作为初始估算。
- **凝视收尾：** 全部区域画完后自动补到 `sceneDurationMs`，并保证结尾至少停留 0.5 秒完整原图。
- `reveal.direction` 在 stream 画法下**不决定真实笔迹**（笔迹由骨架/网格自动生成），仅供预览台的矩形代理演示；保留它是为了预览台可用。

## 遮罩不变量（编排层，必须执行）

- 在时间 `t`，模块仅可显示其 `reveal.startMs ≤ t` 之后、且不超过当前作画进度的像素；未开始模块的任何线条/填充/图像都不得出现。
- 每个区域的**允许掩码** = 矩形 `region` 扣除全部**后续模块的 `region`**，再扣除本模块 `reveal.protectedRegions`。stream 落墨被限制在允许掩码内，因此后续区域不会提前露线。
- `protectedRegions` 采用与 `region` 相同的原图整数像素坐标，用于矩形过大、主体交叠或背景线条可能泄露的情况。
- 渲染器已实现"限制在允许掩码内落墨 → 后续区域与保护区天然不被触碰"的顺序；预览台矩形代理用等价的 `destination-out` 扣除演示同一编排。

## 配置示例

```json
{
  "sceneId": "scene-01",
  "canvas": { "width": 1672, "height": 941 },
  "storyBasis": "该幕字幕的事件摘要",
  "sceneDurationMs": 9000,
  "elements": [
    {
      "id": "rockery",
      "label": "假山场景",
      "sequence": 1,
      "narrativeRole": "故事的场景铺垫",
      "subtitle": "猴子山上，一只小猴子坐在假山顶端，手里拿着香蕉。",
      "type": "structure",
      "region": { "x": 20, "y": 120, "width": 540, "height": 780 },
      "reveal": { "direction": "top_to_bottom", "startMs": 300, "durationMs": 2600, "maskPaddingPx": 22, "protectedRegions": [] },
      "handPath": { "start": [290, 130], "end": [290, 890], "easing": "easeInOut" }
    }
  ]
}
```

> `direction` / `handPath` 仅供预览台矩形代理使用；成片笔迹由 stream 自动生成，无需精调。

## 使用脚本

所有渲染脚本用 skill 内 `.venv` 的解释器运行（依赖隔离）。

1. **准备环境**（首次或缺依赖时）：
   ```bash
   python scripts/prepare_env.py --check   # 探测；成功末行输出 ENV_PY=<路径>，捕获备用
   python scripts/prepare_env.py           # 缺则建 .venv 并装 opencv-python/numpy/av
   ```
2. **解析字幕 + 建议分镜**：
   ```bash
   python scripts/parse_srt.py <字幕.srt> --target-sec 30 --min-sec 25 --max-sec 35
   ```
3. **区域编号预览图**：
   ```bash
   python scripts/render_annotation_preview.py <图片> <标注> <预览图输出>
   ```
4. **预览台（无需服务器）**：直接用 Chrome / Edge 打开 `assets/preview.html`，点"打开文件夹"选目录 → 载入全部图片+同名标注 → 拖拽编辑 → "保存"写回原文件。写回需 File System Access API（Chrome/Edge）；其它浏览器改为下载后手动覆盖。渲染仍走命令行（下面第 5 步）。
5. **渲染单幕成片**：
   ```bash
   <ENV_PY> scripts/render_stream_whiteboard.py <图片> <标注> <输出mp4> assets/drawing-hand.png \
       [--ink-path grid|skeleton] [--color-fill contour-wipe|brush] [--total-ms <毫秒>]
   ```
   `--total-ms` 缺省时用标注里的 `sceneDurationMs`。末行输出 `OUTPUT=<路径>`。
6. **多幕合并**：
   ```bash
   <ENV_PY> scripts/merge_scenes.py --inputs 幕1.mp4 幕2.mp4 幕3.mp4 --output final.mp4
   ```

## 质量检查

渲染前/后确认：

- 首帧为干净的暖米黄旧纸张底，没有提前露出线条。
- 已阅读对应字幕并实际查看原图；`canvas` 与原图像素尺寸一致，所有 `region` 为整数像素坐标且在画布内。
- `sequence`、`startMs` 与字幕事件顺序一致；预览图编号/标签/区域来自同一份标注 JSON。
- 在开场、任意重叠模块中段、所有模块完成后三个时间点检查：未绘制模块均不可见，重叠保护区不漏出，最终帧显示完整原图。
- 笔尖贴近正在推进的笔迹；线稿清晰的插画可用 `--ink-path skeleton` 让笔迹更贴合。
- 所有模块结束后停留至少 0.5 秒完整原图。
- 多幕合并后顺序、时长与字幕分镜一致。

如需修改效果，先在预览台（`assets/preview.html`）调整标注（区域/顺序/时序）并保存，再命令行渲染，不要凭空反复出片。
