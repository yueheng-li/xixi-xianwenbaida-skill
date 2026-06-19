# 🏫 溪溪仙问百答 — 儿童科学内容量产系统

基于《天庭幼儿园：今天神仙老师教什么》IP 的 AI 短视频+有声书量产技能包。7 岁科学课代表闹闹 + 翻车神仙（哪吒/孙悟空/嫦娥）= 反差萌儿童科普。

## 📦 技能结构

```
xixi仙问百答/
├── SKILL.md                  🎯 主编排器（128行, 全链路调度）
├── xixi-文案创作/SKILL.md    📝 视频/音频文案 + 审核循环
├── xixi-分镜与配图/SKILL.md   🎬 分镜JSON + 配图 + 动画prompt
├── xixi-配音与合成/SKILL.md   🔊 TTS多角色配音 + HyperFrames合成
├── xixi-发布归档/SKILL.md    📦 LLM优化 + Obsidian归档 + 发布包
├── scripts/                  🐍 自包含Python脚本
│   ├── volcengine_tts.py     # 火山引擎TTS引擎
│   └── ximalaya_upload.py    # 喜马拉雅上传
├── _shared/                  📚 共享规则与素材
│   ├── 合规校验标准.md       # 豆包平台拦截规则
│   ├── 角色视觉锚点.md       # 角色外观定义
│   └── 角色定妆照.md         # 定妆照prompt参考
├── references/               📖 8个详细参考文件
├── assets/README.md          # BGM/音频素材准备指南
├── config.example.json       # 配置模板
└── requirements.txt          # Python 依赖
```

## 🚀 快速开始

### 前置条件

| 依赖 | 说明 | 获取 |
|------|------|------|
| **Volcengine TTS API** | 火山引擎 seed-tts-2.0 | [注册并开通](https://www.volcengine.com/product/tts)，获取 API Key |
| **HyperFrames** | 视频渲染引擎 | `npm install -g hyperframes` |
| **ian-xiaohei-illustration** | 配图 AI 模型 | Claude Code Skill |
| **FFmpeg** | 音频拼接 | [下载](https://ffmpeg.org/download.html) |
| **喜马拉雅开放平台** | 音频上传(可选) | [注册开发者](https://open.ximalaya.com) |

### 安装

```bash
# 1. 克隆技能包到 Claude Code skills 目录
git clone https://github.com/YOUR_USERNAME/xixi仙问百答.git ~/.claude/skills/xixi仙问百答

# 2. 复制子技能到同级目录（Claude Code 按目录名发现技能）
cp -r ~/.claude/skills/xixi仙问百答/xixi-* ~/.claude/skills/

# 3. 安装 Python 依赖
pip install -r ~/.claude/skills/xixi仙问百答/requirements.txt

# 4. 设置环境变量
# Windows CMD:
setx VOLCENGINE_TTS_API_KEY "your-api-key"
# macOS/Linux:
echo 'export VOLCENGINE_TTS_API_KEY="your-api-key"' >> ~/.bashrc

# 5. 创建配置文件
cp ~/.claude/skills/xixi仙问百答/config.example.json ~/.claude/skills/xixi仙问百答/config.json
# 编辑 config.json，填入你的 PROJECT_ROOT

# 6. 准备音频素材（见 assets/README.md）
```

### 使用

在 Claude Code 中直接说：

```
帮我做一期仙问百答视频，知识点是"为什么放屁会臭"
```

或逐步调用：

```
用 xixi-文案创作 写一期"彩虹怎么形成的"视频文案
用 xixi-分镜与配图 把这篇文案转成分镜JSON和配图
用 xixi-配音与合成 配音+合成视频
用 xixi-发布归档 优化并发布
```

## 📋 内容产出

| 产出 | 规格 |
|------|------|
| 🎬 抖音短视频 | 30-50秒，1080×1920竖屏，MP4 |
| 🎧 有声书/音频 | 10-15分钟，MP3 192kbps |

## ⚠️ 合规

所有生成内容自动经过[豆包平台合规校验](_shared/合规校验标准.md)，覆盖：
- 封建迷信拦截（神仙=文化传说角色）
- 儿童安全保护（无危险行为/擦边）
- 版权保护（原创Q版造型）
- 禁用词过滤（中英文共40+项）

## 📄 许可

MIT
