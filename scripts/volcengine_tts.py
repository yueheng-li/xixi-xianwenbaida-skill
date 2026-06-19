#!/usr/bin/env python3
"""
Volcengine seed-tts-2.0 TTS module for xixi仙问百答 skill suite.
Streaming API + word-level timestamps for dynamic subtitles.
"""
import urllib.request, json, base64, os, ssl, subprocess


def _get_api_key():
    """Read VOLCENGINE_TTS_API_KEY from env or Windows registry (setx fallback)."""
    key = os.environ.get("VOLCENGINE_TTS_API_KEY")
    if key:
        return key
    # Fallback: read from Windows registry (set via `setx` in CMD)
    try:
        out = subprocess.check_output(
            'reg query HKCU\\Environment /v VOLCENGINE_TTS_API_KEY',
            shell=True, text=True, stderr=subprocess.DEVNULL
        )
        for line in out.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 3 and parts[0] == 'VOLCENGINE_TTS_API_KEY':
                return parts[-1]
    except Exception:
        pass
    raise RuntimeError(
        "VOLCENGINE_TTS_API_KEY not found. "
        "Set it via: setx VOLCENGINE_TTS_API_KEY \"your-key\""
    )


KEY = _get_api_key()
RID = "seed-tts-2.0"
URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"

VOICES = {
    "narrator": "zh_female_mengyatou_uranus_bigtts",
    "os": "zh_female_zhixingnv_uranus_bigtts",
}

CHARACTER_VOICES = {
    # === 仙问百答（天庭幼儿园）===
    "闹闹":   "zh_female_mengyatou_uranus_bigtts",
    "旁白":   "zh_female_shaoergushi_uranus_bigtts",
    "孙悟空": "zh_male_sunwukong_uranus_bigtts",
    "太白金星": "zh_male_yuanboxiaoshu_uranus_bigtts",
    "玉帝":   "zh_male_baqiqingshu_uranus_bigtts",
    "猪八戒": "zh_male_zhubajie_uranus_bigtts",
    "嫦娥":   "zh_female_wenroushunv_uranus_bigtts",
    "二郎神": "zh_male_baqiqingshu_uranus_bigtts",
    # === 鸿钧播客 ===
    # 通用场景 — 少年/叛逆（少年梓辛）
    "哪吒": "zh_male_shaonianzixin_uranus_bigtts",
    "杨戬": "zh_male_qingshuangnanda_uranus_bigtts",
    # 通用场景 — 师父/长辈（东方浩然 = 威严沉稳）
    "太乙": "zh_male_dongfanghaoran_uranus_bigtts",
    # 通用场景 — 高冷/学者（高冷沉稳）
    "玉鼎": "zh_male_gaolengchenwen_uranus_bigtts",
    "赤精子": "zh_male_gaolengchenwen_uranus_bigtts",
    "赵公明": "zh_male_gaolengchenwen_uranus_bigtts",
    # 通用场景 — 霸气/统帅（渊博小叔）
    "元始": "zh_male_yuanboxiaoshu_uranus_bigtts",
    "广成子": "zh_male_yuanboxiaoshu_uranus_bigtts",
    # 通用场景 — 开朗/热血（快乐小东）
    "黄龙": "zh_male_kuailexiaodong_uranus_bigtts",
    # 通用场景 — 磁性/算计（磁性解说男声）
    "惧留孙": "zh_male_cixingjieshuonan_uranus_bigtts",
    # 通用场景 — 短小精悍（亮嗓萌仔）
    "土行孙": "zh_male_liangsangmengzai_uranus_bigtts",
    # 通用场景 — 佛系/温和（温柔小哥）
    "弥勒": "zh_male_wenrouxiaoge_uranus_bigtts",
    # 通用场景 — 女修（直率英子 = 干脆利落）
    "云霄": "zh_female_zhishuaiyingzi_uranus_bigtts",
    "石矶": "zh_female_zhishuaiyingzi_uranus_bigtts",
}

def synthesize(text, speaker="narrator", context_hints=None, output_file=None):
    """Generate speech. Returns (audio_bytes, word_list)."""
    # Support both named roles and raw voice IDs (e.g. zh_male_baqiqingshu_uranus_bigtts)
    if speaker.startswith("zh_"):
        voice = speaker
    else:
        voice = VOICES.get(speaker) or CHARACTER_VOICES.get(speaker, VOICES["narrator"])
    hints = context_hints or []
    if speaker == "os":
        hints = ["请用低沉的声音，像在说悄悄话"] + hints
    elif speaker not in VOICES:
        hints = ["请用自然的对话语气，像是在跟人说话"] + hints
    else:
        hints = ["请保持自然温柔的语气"] + hints

    additions = json.dumps({
        "disable_markdown_filter": False,
        "disable_emoji_filter": False,
        "enable_latex_tn": True,
        "context_texts": hints
    })

    payload = json.dumps({
        "req_params": {
            "text": text,
            "speaker": voice,
            "additions": additions,
            "audio_params": {
                "format": "mp3",
                "sample_rate": 24000,
                "enable_subtitle": True
            }
        }
    }).encode('utf-8')

    req = urllib.request.Request(URL, data=payload, method='POST')
    req.add_header("X-Api-Key", KEY)
    req.add_header("X-Api-Resource-Id", RID)
    req.add_header("Content-Type", "application/json")
    req.add_header("Connection", "keep-alive")

    ctx = ssl.create_default_context()
    resp = urllib.request.urlopen(req, timeout=60, context=ctx)
    audio_data = bytearray()
    all_words = []

    for line_bytes in resp:
        line = line_bytes.decode('utf-8').strip()
        if not line:
            continue
        data = json.loads(line)
        code = data.get("code", 0)
        if code == 0 and "data" in data and data["data"]:
            audio_data.extend(base64.b64decode(data["data"]))
        # Words come in separate chunks (data may be null)
        if "sentence" in data and "words" in data["sentence"]:
            all_words.extend(data["sentence"]["words"])
        elif code == 20000000:
            break
        elif code > 0:
            raise RuntimeError(f"TTS error {code}: {data.get('message', str(data))}")

    if not audio_data:
        raise RuntimeError("No audio data received")

    if output_file:
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        with open(output_file, "wb") as f:
            f.write(audio_data)

    return bytes(audio_data), all_words


def synthesize_segments(sections, output_dir, prefix="seg"):
    """Generate audio + word timings for all sections."""
    results = []
    for i, sec in enumerate(sections):
        seg_id = f"{i+1:02d}"
        if sec["type"] == "os":
            speaker = "os"
        elif sec["type"] == "character":
            speaker = sec.get("character", "narrator")
        else:
            speaker = "narrator"
        filename = f"{prefix}-{seg_id}-{sec['type']}.mp3"
        filepath = os.path.join(output_dir, filename)

        print(f"  [{seg_id}] {speaker:8s} | {sec['emotion']:6s} | {len(sec['text'])} chars")
        audio, words = synthesize(sec["text"], speaker=speaker, output_file=filepath)

        # Save word timings for subtitle sync
        words_file = os.path.join(output_dir, f"{prefix}-{seg_id}-{sec['type']}.words.json")
        with open(words_file, 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=2)

        results.append({
            "id": seg_id,
            "file": filepath,
            "words_file": words_file,
            "type": sec["type"],
            "speaker": speaker,
            "size": len(audio),
            "word_count": len(words),
            "timecode": sec["timecode"],
            "section": sec.get("section", ""),
            "text": sec["text"]
        })

    return results