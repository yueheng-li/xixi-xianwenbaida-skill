# 03-多角色 seed-tts-2.0 配音规范

## API 技术参数

### 端点与认证

```
URL: https://openspeech.bytedance.com/api/v3/tts/unidirectional

Headers:
  X-Api-Key: ${VOLCENGINE_TTS_API_KEY}
  X-Api-Resource-Id: seed-tts-2.0
  Content-Type: application/json
```

### 请求体格式

```json
{
  "req_params": {
    "text": "要合成的文本",
    "speaker": "音色ID",
    "additions": "{\"context_texts\":[\"情绪提示\"],\"disable_markdown_filter\":false,\"disable_emoji_filter\":false}",
    "audio_params": {
      "format": "mp3",
      "sample_rate": 24000,
      "enable_subtitle": true
    }
  }
}
```

### 响应格式（流式逐行JSON）

每行独立JSON对象，含 `base64` 音频块。`code: 20000000` 为流结束信号。

### 核心引擎

**TTS引擎**：`../scripts/volcengine_tts.py`
- `synthesize(text, speaker, context_hints, output_file)` → `(audio_bytes, word_list)`

**音频管线**：`../scripts/ximalaya_upload.py`
- 脚本解析 → 角色映射 → 逐段TTS → FFmpeg拼接 → BGM混音

---

## 仙问百答角色音色分配

> **铁律**：每个角色必须使用独立音色ID，不允许多人共用一个角色。

### 核心角色

| 角色 | 音色ID | 音色名称 | 音色描述 | speed | pitch |
|------|--------|----------|----------|-------|-------|
| **旁白** | `zh_female_shaoergushi_uranus_bigtts` | 少儿故事 2.0 | 温暖亲切女声，儿童故事讲述感 | 1.00 | 1.00 |
| **闹闹** | `zh_female_mengyatou_uranus_bigtts` | 萌丫头/Cutey 2.0 | 可爱小女生，7岁，淡定认真 | 0.90 | 1.05 |
| **哪吒** | `zh_male_shaonianzixin_uranus_bigtts` | 少年梓辛/Brayan 2.0 | 12岁少年音，自信嘴硬，翻车后骤降 | 1.10 | 1.00 |
| **孙悟空** | `zh_male_sunwukong_uranus_bigtts` | 猴哥 2.0 | 专属猴哥音色，急躁聪明 | 1.20 | 1.05 |
| **嫦娥** | `zh_female_wenroushunv_uranus_bigtts` | 温柔淑女 2.0 | 温柔端庄，偶尔腹黑 | 0.95 | 0.95 |
| **八戒** | `zh_male_zhubajie_uranus_bigtts` | 猪八戒 2.0 | 专属八戒音色，憨厚慵懒 | 0.85 | 1.00 |

### 配角

| 角色 | 音色ID | 音色名称 | 音色描述 | speed |
|------|--------|----------|----------|-------|
| **太白金星** | `zh_male_yuanboxiaoshu_uranus_bigtts` | 渊博小叔 2.0 | 老年智者，天庭教导主任 | 0.85 |
| **玉帝** | `zh_male_baqiqingshu_uranus_bigtts` | 霸气青叔 2.0 | 威严庄重，偶尔破功 | 0.95 |
| **二郎神** | `zh_male_gaolengchenwen_uranus_bigtts` | 高冷沉稳 2.0 | 高冷男神，偶尔憋不住笑 | 0.95 |

---

## 情绪控制

通过 `additions.context_texts` 数组传递情绪提示：

### 闹闹的情绪谱

| 场景 | context_texts |
|------|---------------|
| 讲解 | `"请用平静淡然的语气，一本正经说离谱的话"` |
| 提问 | `"请用好奇的语气，尾音微微上扬"` |
| 夸奖 | `"请用温柔轻声的语气，像在哄人，语速缓慢"` |
| 面对翻车 | `"请用平静淡然的语气，带无奈感"` |

### 哪吒的情绪谱

| 场景 | context_texts |
|------|---------------|
| "我觉得不对！" | `"请用自信满满的语气，尾音上扬"` |
| "看我的！" | `"请用热情洋溢的语气，语速偏快"` |
| 翻车后"……好吧" | `"请用突然心虚的语气，声音变小，像做错事被抓包，语速骤降"` |

### 悟空的情绪谱

| 场景 | context_texts |
|------|---------------|
| "俺老孙试一下！" | `"请用急不可耐的语气，语速偏快，等不及要试"` |
| 翻车后 | `"请用突然惊讶的语气，不可置信感"` |

### 嫦娥的情绪谱

| 场景 | context_texts |
|------|---------------|
| 正常说话 | `"请用温柔轻声的语气，像在哄人"` |
| 腹黑吐槽 | `"请用温柔但憋着笑的语气，像在说反话"` |

### 旁白的情绪谱（女声）

| 场景 | context_texts |
|------|---------------|
| 正常旁白 | `"请用温暖亲切的语气，像少儿节目主持人，语速适中"` |
| 翻车解说 | `"请用憋着笑说话的语气，像看到小孩子做傻事忍俊不禁"` |
| 彩蛋引导 | `"请用活泼轻快的语气，像是在分享一个好玩的小秘密"` |

---

## 配音流程

### 🎬 视频配音流程（Python脚本自动化）

```
1. 读分镜JSON → 提取每镜 speaker + text
2. 角色名映射音色ID + 情绪提示（查 VOICE_MAP 和 EMOTION_HINTS 字典）
3. 循环调用 synthesize(text, speaker=音色ID, context_hints=[情绪提示], output_file=路径)
4. 生成 segments/001-旁白.mp3, 002-哪吒.mp3, ...
5. 请求间 300ms 限速
6. 保存 manifest.json（所有段落+时长+角色清单）
7. FFmpeg concat 协议无损拼接：
   ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy output_full.mp3
8. 用 ffprobe 获取每段实际时长，用于 HyperFrames 时间同步
```

**脚本模板**：见实际产出 `audio/generate_audio.py`——读分镜JSON → 查 VOICE_MAP → 逐段 synthesise → FFmpeg concat。

### 🎧 音频配音流程

```
1. 解析文案脚本 → 提取角色标注（【角色·情绪】格式）
2. 角色名映射为音色ID（查音色表）
3. 逐段调用 synthesize()，输出到 segments/ 目录
4. 请求间 300ms 限速
5. 段间插入静音：旁白分段400ms / 角色切换250ms / 对话轮换150ms
6. FFmpeg concat 拼接 + 可选 BGM 混音
7. 输出最终MP3（192kbps, 44100Hz, mono）+ manifest.json
```

---

## 配音质量检查

- [ ] 每个角色音色与性格匹配（不看画面只听声音能分辨是谁）
- [ ] 闹闹语速最慢（她是"定海神针"）
- [ ] 哪吒翻车后的降调降速效果明显
- [ ] 悟空说话有"猴急感"
- [ ] 角色切换时音量一致
- [ ] 整体听感像"一群人在录音棚里录的"
- [ ] 无截断/爆音/杂音
