#!/usr/bin/env python3
"""
喜马拉雅开放平台 — 批量上传音频
API: https://open.ximalaya.com/doc/detailApi

使用前：
1. 访问 open.ximalaya.com 注册开发者账号
2. 创建应用 → 获取 App Key / App Secret
3. 填写下面的配置
"""

import argparse, hashlib, json, os, time, urllib.request
from pathlib import Path

# ═══════════════════════════════════════
# 配置区（从喜马拉雅开放平台获取）
# ═══════════════════════════════════════
APP_KEY = os.environ.get('XIMALAYA_APP_KEY', '')
APP_SECRET = os.environ.get('XIMALAYA_APP_SECRET', '')
ACCESS_TOKEN = os.environ.get('XIMALAYA_ACCESS_TOKEN', '')  # OAuth2.0 授权后获取
ALBUM_ID = os.environ.get('XIMALAYA_ALBUM_ID', '')  # 专辑 ID

BASE_URL = 'https://api.ximalaya.com'

# ═══════════════════════════════════════
# 签名与请求
# ═══════════════════════════════════════

def _sign(params, secret):
    """喜马拉雅签名：按 key 排序 + secret → MD5"""
    raw = ''.join(f'{k}={params[k]}' for k in sorted(params))
    raw += secret
    return hashlib.md5(raw.encode()).hexdigest()

def _request(method, path, params=None, files=None):
    """发送 API 请求（自动签名）。"""
    url = BASE_URL + path

    common = {
        'app_key': APP_KEY,
        'client_os_type': '4',
        'nonce': str(int(time.time() * 1000)),
        'timestamp': str(int(time.time() * 1000)),
    }

    if ACCESS_TOKEN and ACCESS_TOKEN != '未授权':
        common['access_token'] = ACCESS_TOKEN

    if params:
        common.update(params)

    sig = _sign(common, APP_SECRET)
    common['sig'] = sig

    # Build query string
    qs = '&'.join(f'{k}={v}' for k, v in common.items())
    full_url = f'{url}?{qs}'

    if files:
        # Multipart upload
        import http.client
        from urllib.parse import urlparse
        parsed = urlparse(full_url)
        boundary = '----FormBoundary' + hashlib.md5(str(time.time()).encode()).hexdigest()
        body = bytearray()
        for key, val in files.items():
            if isinstance(val, tuple):
                filename, data, content_type = val
                body += f'--{boundary}\r\n'.encode()
                body += f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode()
                body += f'Content-Type: {content_type}\r\n\r\n'.encode()
                body += data
                body += b'\r\n'
        body += f'--{boundary}--\r\n'.encode()

        req = urllib.request.Request(full_url, data=bytes(body))
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    else:
        req = urllib.request.Request(full_url, method=method)

    try:
        resp = urllib.request.urlopen(req, timeout=60)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'body': e.read().decode()}

# ═══════════════════════════════════════
# 上传 API（根据开放平台文档调整）
# ═══════════════════════════════════════

def create_track(title, description, mp3_path, album_id=None, tags=None):
    """创建/上传一条声音。

    对应 API: POST /tracks （需确认实际端点）

    常见参数: title, album_id, file (multipart), description, tags
    """
    album_id = album_id or ALBUM_ID
    if not album_id:
        raise ValueError('未设置 ALBUM_ID')

    mp3_path = Path(mp3_path)
    with open(mp3_path, 'rb') as f:
        mp3_data = f.read()

    files = {
        'file': (mp3_path.name, mp3_data, 'audio/mpeg'),
    }

    params = {
        'title': title,
        'album_id': album_id,
        'description': description or '',
    }
    if tags:
        params['tags'] = tags

    return _request('POST', '/tracks', params=params, files=files)


def batch_upload(release_dir, album_id=None):
    """批量上传发布包目录下的所有 MP3。

    自动从 发布信息.md 读取标题和描述。
    """
    release = Path(release_dir)
    mp3_files = sorted(release.glob('podcast_final.mp3'))

    if not mp3_files:
        print(f'No podcast_final.mp3 found in {release_dir}')
        return

    info_md = release / '发布信息.md'
    title = '未命名'
    description = ''
    if info_md.exists():
        content = info_md.read_text(encoding='utf-8')
        # Extract first H1 as title
        for line in content.split('\n'):
            if line.startswith('# ') and '发布信息' not in line:
                title = line[2:].strip()
                break
        # Extract description block
        in_desc = False
        desc_lines = []
        for line in content.split('\n'):
            if line.startswith('```') and not in_desc:
                in_desc = True
                continue
            if line.startswith('```') and in_desc:
                break
            if in_desc:
                desc_lines.append(line)
        if not desc_lines:
            # Fallback: use first non-heading paragraph
            for line in content.split('\n'):
                if line and not line.startswith('#') and not line.startswith('|') and len(line) > 20:
                    description = line.strip()
                    break
        else:
            description = '\n'.join(desc_lines).strip()

    print(f'Uploading: {title}')
    print(f'File: {mp3_files[0]} ({os.path.getsize(mp3_files[0]) / 1024:.0f} KB)')

    result = create_track(
        title=title,
        description=description,
        mp3_path=str(mp3_files[0]),
        album_id=album_id,
        tags='鸿钧播客,道教,神话'
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


# ═══════════════════════════════════════
# CLI
# ═══════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='喜马拉雅批量上传')
    parser.add_argument('release_dir', help='发布包目录路径')
    parser.add_argument('--album-id', default=ALBUM_ID, help='喜马拉雅专辑 ID')
    parser.add_argument('--check-config', action='store_true', help='检查配置是否完整')
    args = parser.parse_args()

    if args.check_config:
        issues = []
        if not APP_KEY: issues.append('XIMALAYA_APP_KEY 未设置')
        if not APP_SECRET: issues.append('XIMALAYA_APP_SECRET 未设置')
        if not ACCESS_TOKEN: issues.append('XIMALAYA_ACCESS_TOKEN 未设置（需OAuth授权）')
        if not ALBUM_ID and not args.album_id:
            issues.append('XIMALAYA_ALBUM_ID 未设置')
        if issues:
            print('❌ 配置不完整：')
            for i in issues: print(f'  - {i}')
            print('\n获取方式：')
            print('  1. 访问 https://open.ximalaya.com 注册开发者')
            print('  2. 创建应用 → 获取 App Key / App Secret')
            print('  3. OAuth2.0 授权 → 获取 Access Token')
            print('  4. 在喜马拉雅创建专辑 → 获取 Album ID')
        else:
            print('✅ 配置完整，可以上传')
        return

    result = batch_upload(args.release_dir, args.album_id)
    if result and result.get('error'):
        print(f'\n❌ 上传失败: {result}')
        print('提示：检查 APP_KEY / APP_SECRET / ACCESS_TOKEN 是否正确')


if __name__ == '__main__':
    main()
