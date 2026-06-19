---
name: xixi-分镜与配图
description: >-
  儿童科普视频分镜JSON+场景配图+动画Prompt生成。触发:"分镜"/"配图"/"动画prompt"或由xixi仙问百答调度。
  输出静态分镜JSON、动画分镜JSON、配图prompt、动画prompt。
argument-hint: [文案.md路径]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Skill
---

# 溪溪·分镜与配图

> **合规铁律**：所有 prompt 生成前必须通过 [`../_shared/合规校验标准.md`](../_shared/合规校验标准.md) 逐项检查。
> **角色锚点**：配图/动画prompt必须从 `../_shared/角色视觉锚点.md` 逐字复制角色描述，不自行发挥。

## 核心流程

```
文案 → 静态分镜JSON(逐句) + 动画分镜JSON(8-10s/段)
     → 场景配图(每shot 1张) + 动画Prompt(每段完整+一行版)
     → 动态分镜脚本(多帧拆分) → 多帧配图
```

---

## 第二步：静态分镜JSON

**输入**：`01_文案.md`
**输出**：`02_分镜.json`

**JSON Schema 核心字段**：
```json
{
  "video_meta": {"title": "", "duration_total": 45, "style": "儿童科学翻车",
    "category": "人体篇|物理篇|化学篇|生物篇|天文地理篇", "characters": []},
  "shots": [{
    "id": 1, "speaker": "闹闹", "text": "台词",
    "duration": 3.5,
    "scene": {"description": "", "keywords_en": [], "mood": ""},
    "visual_style": "儿童明亮|实验室场景|天庭背景",
    "transition": "cut",
    "character_action": "角色动作描述",
    "sfx": "音效"
  }]
}
```

**规则**：
- 每句台词 = 1个shot，时长=字数×0.3-0.35秒
- speaker 驱动后续多角色TTS
- character_action 驱动配图
- sfx 标注音效

> 完整 Schema 见 `../references/02-分镜JSON输出.md`

## 第二步B：动画分镜JSON

**输入**：`02_分镜.json`
**输出**：`02b_动画分镜.json`（3-6个segment，每段8-10秒）

**合并规则**：同一场景+同组角色+连续叙事 → 合并为1个segment；场景切换 → 新segment。

**JSON Schema 核心字段**：
```json
{
  "animation_meta": {"title": "", "duration_total": 45, "segment_count": 5,
    "style": "儿童科学翻车动画"},
  "segments": [{
    "id": 1, "start_time": 0, "duration": 9.0,
    "shots_merged": [1,2,3],
    "scene": {"description": "", "background": "", "lighting": "",
      "camera_movement": "镜头推/拉/摇/移/跟"},
    "character_actions": [{"character": "", "action": ""}],
    "keyframe_sequence": ["0s: 起始", "4.5s: 中间", "9s: 落幅"],
    "mood": "",
    "transition_from_prev": "fade-in", "transition_to_next": "dissolve 0.3s"
  }]
}
```

---

## 第四步：场景配图

**输入**：`02_分镜.json`
**输出**：每shot 1张PNG（1080×1920竖屏）+ `03_配图prompts.md`

**画风**：ian-xiaohei-illustration | 儿童绘本风 | 色彩明亮饱和 | Q版可爱 | 翻车夸张搞笑

**操作**：
```
提取每shot的scene+character_action → 读取 `../_shared/角色视觉锚点.md` → 生成配图prompt
→ 合规自检(八大类+禁用词表) → 调用模型 → 审核 → 导出images/
```

## 第四步B：动画Prompt

**输入**：`02b_动画分镜.json`
**输出**：`04b_动画prompts.md`（每段完整prompt块 + 一行版prompt）

**Prompt结构**：
```
## 动画段 {ID}
画面描述(200-400字,起幅→过程→落幅)
+ 运镜描述(匀速平滑,儿童友好)
+ 角色动作序列(秒级精度)
+ 场景与光影
+ 角色视觉锚点(从 `../_shared/角色视觉锚点.md` 逐字复制)
+ 动画Prompt一行版(150-300字,精炼完整)
```

**图生视频prompt规则**：只写动作+运镜，不写角色外观（参考图已定义）。用通用代称 `a figure`。

---

## 第五步A：动态分镜脚本

**原则**：每帧3-4秒，超过4秒的镜头拆为多帧（K1/K2/K3）。帧间 dissolve 0.3-0.4s。

**格式**：`镜头ID | 时间段 | 帧 | hold | 画面动作 | 镜头运动 | 转场 | 特效`

## 第五步B：多帧配图

为动态分镜每帧生成1张配图prompt → 合规自检 → 调用模型。
多帧prompt必须从 `../_shared/角色视觉锚点.md` 逐字复制，仅帧间动作/镜头变化。

---

## Step 0A：定妆照（全系列只跑一次）

首次使用前一次性生成 8 角色 + 6 场景定妆照 → 存入 `_shared/定妆照/`。
后续所有章节复用，不得重新生成。生成前 prompt 必须通过合规校验。

---

## 参考

- `../references/02-分镜JSON输出.md`
- `../references/04-场景配图.md`
- `../_shared/合规校验标准.md`
- `../_shared/角色视觉锚点.md`
