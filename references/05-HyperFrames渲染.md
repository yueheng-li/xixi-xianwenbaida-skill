# 05-儿童向 HyperFrames 视频渲染规范

> **流程更新**：第五步拆为三个子步骤——5A动态分镜脚本 → 5B多帧配图生成 → 5C视频合成。
> 核心原则：每镜3-4秒，超过则拆多帧；每两镜之间必加转场；每镜加运镜+特效。

## 5A · 动态分镜脚本

将配音时长映射为3-4s/帧的动态分镜表。计算公式：`总帧数 ≈ ceil(配音总时长/3.5)`。

| 字段 | 说明 |
|------|------|
| 帧ID | K1, K2, ... |
| 时间段 | start→end（秒） |
| hold | 帧持续时长（3-4s） |
| 画面动作 | 本帧画面描述（角色锚点不变，仅动作变化） |
| 运镜 | ken-burns zoom from→to |
| 转场 | dissolve时长 / flash-white / fade |
| 特效 | bubble/spark/feather/shake/star/popIn |

## 渲染目标

将多角色配音 + 儿童绘本风配图 + 音效 → 合成为高质儿童科学短视频。

---

## ⚠️ 音频处理（踩坑总结）

**三个铁律**：
1. 音频文件必须放在 HyperFrames 目录内，用相对路径 `src="audio.mp3"`——不能用 `../` 引用外部目录
2. 音频文件名不能含中文字符（HyperFrames 本地文件服务器对中文URL编码有问题，导致 `ERR_ABORTED`）
3. 渲染前用 `ffprobe` 获取每段音频实际时长，按累计时间计算每个镜头的 `data-start`

**操作流程**：
```bash
# 1. 获取实际时长
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 shot_01.mp3

# 2. 拷贝音频（英文文件名）
cp 配音_为什么人会放屁.mp3 HyperFrames/audio.mp3
```

---

## HTML 结构铁律

1. 根元素：`data-composition-id="main"` + `data-duration="总时长秒数"`
2. 每个镜头用 `<div class="clip" data-start="X" data-duration="Y">` 包裹
3. ⚠️ 所有带 `data-start` 的元素**必须**加 `class="clip"`——否则元素会全程可见不消失
4. 图片 `<img class="bg clip" data-animate="ken-burns" data-scale-from="1.0" data-scale-to="1.04">`
5. 字幕用 `<div class="sub clip" data-start="...">`，内含 `<span class="tag">emoji</span>` + `<span class="em">关键词</span>`
6. 音频 `<audio src="audio.mp3" data-start="0" data-duration="总时长" data-volume="1.0" data-master="true">`

## 特效参数速查

| 场景 | 特效 | 属性 |
|------|------|------|
| 常规镜头 | ken-burns | `data-animate="ken-burns" data-scale-from="1.0" data-scale-to="1.03~1.06"` |
| 段落切换 | dissolve | `data-transition-in="dissolve" data-transition-duration-in="0.3~0.5"` |
| 开场 | fade | `data-transition-in="fade" data-transition-duration-in="0.5"` |
| 翻车/雷劈 | flash+shake | `data-transition-in="flash-white" data-transition-duration-in="0.15"` + `data-animate="shake" data-shake-intensity="4~6"` |
| 结尾 | fade-out | 加黑底 clip `<div class="clip" data-start="结束时间" data-duration="0.3" data-transition-out="fade">` |

## 字幕样式

```css
.sub { bottom:140px; left:64px; right:64px; font-size:42px; color:#fff;
  text-shadow:0 3px 12px rgba(0,0,0,.65); }
.sub .tag { font-size:36px; margin-right:6px; }
.sub .em { font-weight:800; color:#FFD700; }  /* 金色高亮关键词 */
```

## 渲染命令

```bash
npx hyperframes preview                    # 预览
npx hyperframes render --output "../05_成片/标题.mp4"  # 渲染
ffprobe -show_entries stream=codec_type 文件.mp4  # 验证有video+audio双轨
```

---

## 渲染参数

```json
{
  "resolution": "1080x1920",
  "aspect_ratio": "9:16",
  "fps": 30,
  "codec": "h264",
  "bitrate": "8M",
  "format": "mp4"
}
```

---

## 儿童版关键技术差异

对比成人版，儿童视频渲染有四个关键差异：

### 1. 角色字幕前缀

每条字幕前加角色emoji标识，小朋友一看就知道谁在说话：

```
🔬闹闹   哪吒同学，你知道为什么放屁会臭吗？
💥哪吒   当然是因为吃了不该吃的东西！
```

### 2. 翻车特效组合

每集至少一个翻车场面，使用固定组合：

```
flash-white（0.2s）→ shake（0.3s）→ 烟雾叠加（0.5s fade in）
→ BGM暂停（0.5s静默）→ 字幕变炸裂大字 → BGM恢复
```

**儿童版翻车标准**：爆炸=Q版蘑菇云 / 碎片=卡通星星 / 烟雾=搞笑绿烟 / 声音=卡通音效（不写实不恐怖）

### 3. 音效层

拟声词必须配对应音效，这是儿童视频的灵魂：

| 拟声词 | 音效 |
|--------|------|
| 砰！ | 卡通爆炸声 |
| 呲—— | 气泡/漏气声 |
| 哗—— | 水流/液体声 |
| 咣当！ | 金属落地声 |
| 噗—— | 放屁声 |

### 4. 家庭实验彩蛋模板

片尾固定模板：温馨厨房场景 + 实验材料特写 + 步骤字幕 + Q版闹闹竖大拇指。

---

## 字幕样式

```css
.subtitle {
  position: absolute;
  bottom: 120px;
  left: 48px;  right: 48px;
  text-align: center;
  font-family: "Noto Sans SC", sans-serif;
  font-size: 38px;
  font-weight: 500;
  line-height: 1.5;
  color: #FFFFFF;
  text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}

.speaker-tag { font-size: 32px; margin-right: 8px; }

.subtitle .emphasis {
  font-weight: 800;
  color: #FFD700;
}

.crash-subtitle {
  font-size: 72px;
  font-weight: 900;
  color: #FF4444;
  animation: shake 0.3s;
}

.egg-subtitle {
  background: rgba(0,0,0,0.5);
  border-radius: 16px;
  padding: 16px 24px;
}
```

---

## Ken Burns 参数（儿童版）

| 情绪 | 缩放 | 方向 |
|------|------|------|
| 好奇/讲解 | 1.0→1.03 | in |
| 自信/得意 | 1.0→1.05 | in |
| 翻车 | shake特效替代KB | — |
| 温馨/彩蛋 | 1.0→1.02 | in（极慢） |

---

## 音效集成

```html
<!-- 配音音轨 -->
<audio src="audio/full_voiceover.mp3" data-start="0" data-volume="1.0" />

<!-- 爆炸音效 -->
<audio src="sfx/explosion_cartoon.mp3"
       data-start="17.5" data-duration="1.0" data-volume="0.6" />

<!-- BGM（翻车时自动静音0.5秒） -->
<audio src="bgm/kids_comedy.mp3" data-start="0"
       data-volume="0.25" data-mute-at="17.5" data-mute-duration="1.0" />
```

---

## 渲染命令

```bash
npx hyperframes preview
npx hyperframes render --output "../05_成片/YYYY-MM-DD_视频标题.mp4"
```

---

## 渲染质量检查

- [ ] 角色字幕emoji标识清晰
- [ ] 翻车特效flash-white+shake流畅
- [ ] 音效与拟声词同步
- [ ] BGM在翻车瞬间暂停
- [ ] 家庭实验彩蛋字幕清晰+Q版闹闹出现
- [ ] 时长30-50秒
