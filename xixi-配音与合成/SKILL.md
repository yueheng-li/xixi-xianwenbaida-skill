---
name: xixi-配音与合成
description: >-
  儿童科普视频TTS多角色配音+HyperFrames视频合成。触发:"配音"/"合成"/"渲染"/"TTS"或由xixi仙问百答调度。
  输出多角色配音MP3+成品MP4(双模式:动画合成/图片KenBurns)。
argument-hint: [分镜JSON路径]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# 溪溪·配音与合成

## 第三步：TTS 多角色配音

**引擎**：Volcengine seed-tts-2.0
**API Key**：环境变量 `VOLCENGINE_TTS_API_KEY`（自动fallback到Windows注册表）
**核心脚本**：`../scripts/volcengine_tts.py`

### 音色表

| 角色 | 音色ID | 特征 | 语速 |
|------|--------|------|------|
| 旁白 | `zh_female_shaoergushi_uranus_bigtts` | 少儿故事 2.0，温暖亲切 | 1.00 |
| 闹闹 | `zh_female_mengyatou_uranus_bigtts` | 萌丫头 2.0，淡定童声 | 0.90 |
| 哪吒 | `zh_male_shaonianzixin_uranus_bigtts` | 少年梓辛 2.0，自信嘴硬 | 1.10 |
| 孙悟空 | `zh_male_sunwukong_uranus_bigtts` | 猴哥 2.0，急躁聪明 | 1.20 |
| 嫦娥 | `zh_female_wenroushunv_uranus_bigtts` | 温柔淑女 2.0 | 0.95 |
| 八戒 | `zh_male_zhubajie_uranus_bigtts` | 猪八戒 2.0，憨厚慵懒 | 0.85 |
| 太白金星 | `zh_male_yuanboxiaoshu_uranus_bigtts` | 渊博小叔 2.0，老年智者 | 0.85 |
| 玉帝 | `zh_male_baqiqingshu_uranus_bigtts` | 霸气青叔 2.0，威严 | 0.95 |

### 情绪控制（context_texts）

| 角色 | 情绪 | context_texts |
|------|------|---------------|
| 闹闹 | 淡定 | "请用平静淡然的语气，一本正经说离谱的话" |
| 哪吒 | 自信 | "请用自信满满的语气，尾音上扬" |
| 哪吒翻车 | 嘴硬 | "请用突然心虚的语气，声音变小，像做错事被抓包" |
| 悟空 | 急躁 | "请用急不可耐的语气，语速偏快" |
| 嫦娥 | 温柔 | "请用温柔轻声的语气，像在哄人，语速缓慢" |
| 旁白 | 活泼 | "请用活泼轻快的语气，语速稍快，尾音上扬" |

### 操作流程

```
读取分镜JSON → 按speaker分组 → 逐段调用 volcengine_tts.synthesize()
→ 生成 segments/*.mp3 → 请求间300ms限速
→ FFmpeg concat拼接: ffmpeg -y -i "concat:shot_01.mp3|shot_02.mp3|..." -c copy output.mp3
```

**停顿规范**：旁白400ms / 角色切换250ms / 对话150ms

**输出**：
- `配音_xxx.mp3`（44.1kHz / 24kHz原始）
- `segments/` 目录（逐段TTS，可复用）
- `manifest.json`（段落+时长+角色清单）

> 完整参数见 `../references/03-火山引擎TTS配音.md`

---

## 第五步C：视频合成（双模式）

### 模式判断

```
检查素材：
  ├─ 有动画MP4段(anim_segments/*.mp4) → 🎞️ 动画合成模式
  └─ 只有静态图片(images/*.png) → 🖼️ 图片合成模式
```

### 🎞️ 模式A：动画合成

**素材**：`anim_segments/seg_NN.mp4`（每段8-10s）+ `audio.mp3` + `bgm.mp3` + `ending.mp3`

HTML 中用 `<video>` 替代 `<img>`：
```html
<video class="bg clip" data-start="0" data-duration="9.0"
       src="anim_segments/seg_01.mp4" muted playsinline data-animate="none"></video>
```

- `<video>` 必须 `muted`（配音走独立音频轨）
- 动画段 `data-animate="none"`（动画已有运动）
- segment间 dissolve 0.3s

### 🖼️ 模式B：图片Ken Burns合成

每帧图片 + zoom/pan + 配音 + 字幕。
```html
<img class="bg clip" data-animate="ken-burns" data-scale-from="1.0" data-scale-to="1.05" src="images/k01.png">
```

### 音画同步铁律

> 音频讲什么，画面显示什么。逐段核对：说话角色在画面中 ✓ / 台词动作在发生 ✓ / 情绪一致 ✓ / 段边界对齐 ✓

### 渲染规范

- 输出：MP4，1080×1920竖屏，30fps
- 转场：dissolve 0.25-0.5s，翻车 flash-white 0.15s，开场 fade-in，结尾 fade-out
- 字幕：底部居中，角色emoji前缀，金色高亮关键词
- 3音频轨：`audio.mp3`(配音) + `bgm.mp3`(BGM, vol=0.18) + `ending.mp3`(片尾~2.4s)

### 渲染命令

```bash
cd HyperFrames/
npx hyperframes render --output "../05_成片/{标题}.mp4"
```

---

## Step 0：素材准备

| 素材 | 路径 | 用途 |
|------|------|------|
| 角色视觉锚点 | `../_shared/角色视觉锚点.md` | 配图引用 |
| 纯净BGM | `{{PROJECT_ROOT}}/抖音/背景音乐_纯BGM.mp3` | 拷贝为 `bgm.mp3`，vol=0.15-0.20 |
| 结尾音频 | `{{PROJECT_ROOT}}/HyperFrames/ending.mp3` | ~2.4s "感谢收看" |

## 渲染后必检

- [ ] 音画内容逐段一致
- [ ] 无卡顿/模糊
- [ ] 字幕与画面对齐
- [ ] BGM不压人声
- [ ] 时长合规（30-50s / 10-15min）

## 参考

- `../references/03-火山引擎TTS配音.md`
- `../references/05-HyperFrames渲染.md`
- `../scripts/volcengine_tts.py`
