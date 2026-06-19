# 02-多角色分镜JSON标准化输出规范

## 核心目标

将对话体文案转化为多角色分镜JSON。每个镜头对应一个角色的台词+动作+音效，参数完整、可直接驱动多角色TTS配音、配图生成和HyperFrames渲染。

---

## JSON Schema（儿童科学版 v2）

```json
{
  "$schema": "xixi-storyboard-v2",
  "video_meta": {
    "title": "视频标题（≤15字）",
    "knowledge_point": "知识点（如：屁的臭味来自硫化氢）",
    "volume": "人体篇 | 物理篇 | 化学篇 | 生物篇 | 天文地理篇",
    "chapter_ref": "对应小说章节",
    "characters": ["闹闹", "哪吒"],
    "duration_total": 45.0,
    "style": "儿童科学翻车",
    "aspect_ratio": "9:16",
    "resolution": "1080x1920",
    "fps": 30,
    "bgm": { "type": "轻快儿童 | 搞怪喜剧 | 温馨日常", "volume_ratio": 0.25, "mute_on_crash": true }
  },
  "shots": [
    {
      "id": 1,
      "segment": "开场 | 悟空的蛤蟆理论 | 闹闹的细菌课堂 | ...",
      "speaker": "闹闹 | 哪吒 | 孙悟空 | 嫦娥 | 八戒 | 旁白",
      "text": "当前镜头对应的台词",
      "duration": 3.5,
      "scene": {
        "description": "画面场景的视觉描述",
        "keywords_en": ["heavenly laboratory", "test tubes"],
        "location": "天庭实验室 | 凌霄宝殿 | 广寒宫 | 花果山",
        "mood": "好奇 | 搞笑 | 震惊 | 淡定 | 翻车 | 得意"
      },
      "visual_style": "儿童明亮 | 实验室场景 | 翻车现场 | 温馨日常",
      "character_action": "角色当前动作（驱动配图）",
      "character_expression": "闹闹:淡定 / 哪吒:自信",
      "camera": { "shot_type": "medium | close-up | wide | two-shot", "focus_character": "闹闹" },
      "sfx": "无 | explosion | glass_break | fart | bubbles | gasp | rumble",
      "typography": {
        "subtitle_full": "完整字幕",
        "subtitle_speaker_prefix": "🔬 | 💥 | 🐵 | 🌙 | 🐷 | 📣",
        "subtitle_emphasis": ["关键词"],
        "subtitle_position": "bottom-center"
      },
      "transition": { "in": "cut | flash-white | pop-in", "out": "cut | flash-white | shake" },
      "voice": {
        "character": "闹闹",
        "emotion": "好奇 | 淡定 | 认真 | 激动 | 嘴硬 | 翻车",
        "speed": "slightly-slow | normal | fast",
        "emphasis_words": ["关键词"],
        "pause_after": 0.2
      }
    }
  ]
}
```

---

## 角色标识表

| speaker | 角色 | emoji | 性格锚点 |
|---------|------|-------|----------|
| `闹闹` | 7岁科学课代表 | 🔬 | 淡定认真，"其实呢……" |
| `哪吒` | 12岁自信实验杀手 | 💥 | 嘴硬，翻车后"……好吧" |
| `孙悟空` | 天才型急躁学渣 | 🐵 | "俺老孙试一下！" |
| `嫦娥` | 温柔腹黑 | 🌙 | 微笑吐槽 |
| `八戒` | 懒散偶尔蒙对 | 🐷 | "这个简单……吧？" |
| `太白金星` | 天庭教导主任 | ⭐ | 慢而稳，和稀泥 |
| `玉帝` | 天庭CEO | 👑 | 威严，偶尔被气到破功 |
| `旁白` | 解说/彩蛋引导 | 📣 | 温暖活泼 |

## 音效表

| sfx值 | 触发场景 |
|--------|----------|
| `explosion` | 哪吒做实验炸了 |
| `glass_break` | 试管/烧杯碎了 |
| `fart` | 屎尿屁相关内容 |
| `bubbles` | 液体沸腾/冒泡 |
| `gasp` | 围观神仙惊叹 |
| `rumble` | 实验室被炸得震动 |
| `freeze` | 嫦娥冻住东西 |
| `laughter` | 好笑时刻 |

---

## 时长计算公式（儿童版）

```
儿童口播标准语速：每分钟180-210字（比成人慢15-20%）

闹闹：每分钟190字 → 字数 × 0.32秒
哪吒：每分钟220字 → 字数 × 0.27秒（说话急）
悟空：每分钟240字 → 字数 × 0.25秒（更快）
嫦娥：每分钟200字 → 字数 × 0.30秒
旁白：每分钟200字 → 字数 × 0.30秒

镜头时长 = 字数×角色语速系数 + 停顿 + sfx预留（拟声词+0.5秒）
```

---

## 转场规则（儿童版）

| 转场 | 适用 |
|------|------|
| `cut` | 常规角色对话切换 |
| `flash-white` | 翻车瞬间（白光+震动） |
| `pop-in` | 神仙突然插嘴 |
| `shake` | 实验室震动 |

---

## 完整示例

```json
{
  "$schema": "xixi-storyboard-v2",
  "video_meta": {
    "title": "为什么放屁会臭？",
    "knowledge_point": "屁的臭味来自硫化氢",
    "volume": "人体篇",
    "chapter_ref": "第001章",
    "characters": ["闹闹", "哪吒"],
    "duration_total": 45.0,
    "style": "儿童科学翻车",
    "aspect_ratio": "9:16",
    "resolution": "1080x1920",
    "fps": 30,
    "bgm": { "type": "搞怪喜剧", "volume_ratio": 0.25, "mute_on_crash": true }
  },
  "shots": [
    {
      "id": 1,
      "speaker": "闹闹",
      "text": "哪吒同学，你知道为什么放屁会臭吗？",
      "duration": 4.0,
      "scene": {
        "description": "天庭实验室。闹闹站在小凳子上，手里举着装了透明气体的试管。哪吒坐在对面，脚边的风火轮冒着微弱的黑烟（刚才又炸了）。",
        "keywords_en": ["heavenly lab", "girl on stool", "test tube", "boy with fire wheels"],
        "location": "天庭实验室",
        "mood": "好奇"
      },
      "visual_style": "儿童明亮",
      "character_action": "闹闹歪着头，试管举到哪吒面前",
      "character_expression": "闹闹:好奇 / 哪吒:疑惑",
      "camera": { "shot_type": "two-shot", "focus_character": "闹闹" },
      "sfx": "无",
      "typography": {
        "subtitle_full": "哪吒同学，你知道为什么放屁会臭吗？",
        "subtitle_speaker_prefix": "🔬",
        "subtitle_emphasis": ["为什么", "放屁", "臭"],
        "subtitle_position": "bottom-center"
      },
      "transition": { "in": "cut", "out": "cut" },
      "voice": {
        "character": "闹闹",
        "emotion": "好奇",
        "speed": "slightly-slow",
        "emphasis_words": ["放屁", "臭"],
        "pause_after": 0.3
      }
    },
    {
      "id": 2,
      "speaker": "哪吒",
      "text": "当然是因为吃了不该吃的东西！比如韭菜——",
      "duration": 3.0,
      "scene": {
        "description": "哪吒自信地站起来，双手叉腰。风火轮在身后转得更快了。",
        "keywords_en": ["confident boy", "hands on hips", "fire wheels"],
        "location": "天庭实验室",
        "mood": "得意"
      },
      "visual_style": "儿童明亮",
      "character_action": "哪吒双手叉腰站起来，一脸'这题我会'",
      "character_expression": "哪吒:自信满满 / 闹闹:淡定等待",
      "camera": { "shot_type": "medium", "focus_character": "哪吒" },
      "sfx": "无",
      "typography": {
        "subtitle_full": "当然是因为吃了不该吃的东西！比如韭菜——",
        "subtitle_speaker_prefix": "💥",
        "subtitle_emphasis": ["韭菜"],
        "subtitle_position": "bottom-center"
      },
      "transition": { "in": "cut", "out": "cut" },
      "voice": {
        "character": "哪吒",
        "emotion": "自信",
        "speed": "fast",
        "emphasis_words": ["韭菜"],
        "pause_after": 0.2
      }
    },
    {
      "id": 3,
      "speaker": "闹闹",
      "text": "不对。其实呢，屁的臭味来自一种叫'硫化氢'的东西——就是臭鸡蛋的那个味道。",
      "duration": 6.0,
      "scene": {
        "description": "闹闹淡定地在黑板上画了一个臭鸡蛋。哪吒的表情从自信变成了'什么？你说我的屁是臭鸡蛋？'",
        "keywords_en": ["blackboard", "rotten egg drawing", "boy shocked"],
        "location": "天庭实验室",
        "mood": "搞笑"
      },
      "visual_style": "儿童明亮",
      "character_action": "闹闹在黑板上画了一个臭鸡蛋，表情认真",
      "character_expression": "闹闹:认真 / 哪吒:震惊+不服",
      "camera": { "shot_type": "wide", "focus_character": "闹闹" },
      "sfx": "无",
      "typography": {
        "subtitle_full": "不对。其实呢，屁的臭味来自一种叫'硫化氢'的东西——就是臭鸡蛋的那个味道。",
        "subtitle_speaker_prefix": "🔬",
        "subtitle_emphasis": ["硫化氢", "臭鸡蛋"],
        "subtitle_position": "bottom-center"
      },
      "transition": { "in": "cut", "out": "cut" },
      "voice": {
        "character": "闹闹",
        "emotion": "认真",
        "speed": "slightly-slow",
        "emphasis_words": ["硫化氢", "臭鸡蛋"],
        "pause_after": 0.4
      }
    },
    {
      "id": 4,
      "speaker": "哪吒",
      "text": "我不信！我的屁跟臭鸡蛋有什么关系——我证明给你看！",
      "duration": 4.5,
      "scene": {
        "description": "哪吒跳起来，深吸一口气——肚子开始鼓起来——闹闹默默戴上了护目镜。",
        "keywords_en": ["boy jumping", "belly expanding", "girl putting on goggles"],
        "location": "天庭实验室",
        "mood": "翻车预警"
      },
      "visual_style": "翻车现场",
      "character_action": "哪吒站起来深吸气，肚子鼓起来，闹闹淡定地戴护目镜",
      "character_expression": "哪吒:决心满满 / 闹闹:早就知道接下来要发生什么",
      "camera": { "shot_type": "two-shot", "focus_character": "哪吒" },
      "sfx": "膨胀声",
      "typography": {
        "subtitle_full": "我不信！我的屁跟臭鸡蛋有什么关系——我证明给你看！",
        "subtitle_speaker_prefix": "💥",
        "subtitle_emphasis": ["不信", "证明"],
        "subtitle_position": "bottom-center"
      },
      "transition": { "in": "cut", "out": "flash-white" },
      "voice": {
        "character": "哪吒",
        "emotion": "激动",
        "speed": "fast",
        "emphasis_words": ["不信", "证明"],
        "pause_after": 0.2
      }
    },
    {
      "id": 5,
      "speaker": "旁白",
      "text": "砰——！",
      "duration": 1.5,
      "scene": {
        "description": "画面震动。实验室冒出一团绿色烟雾。闹闹站在烟雾中，护目镜上沾着绿色不明物体。",
        "keywords_en": ["green smoke explosion", "lab shaking", "girl with goggles"],
        "location": "天庭实验室",
        "mood": "翻车"
      },
      "visual_style": "翻车现场",
      "character_action": "绿色烟雾笼罩，闹闹淡定地擦拭护目镜",
      "character_expression": "闹闹:波澜不惊 / 哪吒:尴尬捂脸",
      "camera": { "shot_type": "wide", "focus_character": "无" },
      "sfx": "explosion + fart",
      "typography": {
        "subtitle_full": "砰——！",
        "subtitle_speaker_prefix": "📣",
        "subtitle_emphasis": [],
        "subtitle_position": "bottom-center"
      },
      "transition": { "in": "flash-white", "out": "shake" },
      "voice": {
        "character": "旁白",
        "emotion": "搞笑",
        "speed": "normal",
        "emphasis_words": [],
        "pause_after": 0.5
      }
    },
    {
      "id": 6,
      "speaker": "闹闹",
      "text": "哪吒同学。实验室里——不准放屁。这是第七版安全守则新加的。",
      "duration": 5.0,
      "scene": {
        "description": "闹闹指着墙上被炸得只剩一半的安全守则海报（毛笔新加：第37条·实验室内禁止放屁）。哪吒低着头，风火轮都不转了。",
        "keywords_en": ["safety poster", "new rule", "girl pointing", "boy ashamed"],
        "location": "天庭实验室",
        "mood": "搞笑+温馨"
      },
      "visual_style": "儿童明亮",
      "character_action": "闹闹平静地指向墙上新加的安全守则，哪吒低头认错",
      "character_expression": "闹闹:淡定 / 哪吒:不好意思但还在嘴硬",
      "camera": { "shot_type": "medium", "focus_character": "闹闹" },
      "sfx": "无",
      "typography": {
        "subtitle_full": "哪吒同学。实验室里——不准放屁。这是第七版安全守则新加的。",
        "subtitle_speaker_prefix": "🔬",
        "subtitle_emphasis": ["不准放屁", "第七版"],
        "subtitle_position": "bottom-center"
      },
      "transition": { "in": "cut", "out": "dissolve" },
      "voice": {
        "character": "闹闹",
        "emotion": "淡定",
        "speed": "slightly-slow",
        "emphasis_words": ["不准放屁", "第七版"],
        "pause_after": 0.3
      }
    },
    {
      "id": 7,
      "speaker": "旁白",
      "text": "小朋友们，今天回家做一个实验：把一颗生鸡蛋泡在白醋里，看看三天后会变成什么？评论区告诉闹闹老师！",
      "duration": 6.0,
      "scene": {
        "description": "温馨的家庭厨房。一只手把鸡蛋轻轻放进白醋杯里。右下角Q版闹闹竖起大拇指。",
        "keywords_en": ["kitchen", "egg in vinegar", "experiment", "thumbs up"],
        "location": "家庭厨房",
        "mood": "温馨"
      },
      "visual_style": "温馨日常",
      "character_action": "Q版闹闹在画面右下角竖起大拇指",
      "character_expression": "闹闹:温暖微笑",
      "camera": { "shot_type": "close-up", "focus_character": "无" },
      "sfx": "温馨提示音",
      "typography": {
        "subtitle_full": "🔬家庭小实验：醋泡鸡蛋——鸡蛋壳会消失哦！三天后评论区交作业～",
        "subtitle_speaker_prefix": "📣",
        "subtitle_emphasis": ["醋泡鸡蛋", "壳会消失"],
        "subtitle_position": "bottom-center"
      },
      "transition": { "in": "dissolve", "out": "fade-out" },
      "voice": {
        "character": "旁白",
        "emotion": "温暖",
        "speed": "normal",
        "emphasis_words": ["白醋", "三天后"],
        "pause_after": 0.5
      }
    }
  ]
}
```

---

## 输出规范

- **文件名**：`YYYY-MM-DD_知识点_分镜.json`
- **编码**：UTF-8（无BOM）
- **缩进**：2空格
- **验证**：检查speaker在角色表中、sfx在音效表中
