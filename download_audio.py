#!/usr/bin/env python3
"""Download MP3 from qhmusiccorner/Chinese-HSK / HSK1/fullpinyinwithtones."""
import concurrent.futures
import json
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / 'audio'
API = 'https://api.github.com/repos/qhmusiccorner/Chinese-HSK/git/trees/'
RAW = 'https://raw.githubusercontent.com/qhmusiccorner/Chinese-HSK/main/HSK1/fullpinyinwithtones/'
HEADERS = {'User-Agent': 'PinyinStudio-ChineseHSK/1.0', 'Accept': 'application/vnd.github+json'}


def tree(ref):
    request = urllib.request.Request(API + urllib.parse.quote(ref, safe=''), headers=HEADERS)
    with urllib.request.urlopen(request, timeout=40) as response:
        value = json.load(response)
    if value.get('truncated'):
        raise RuntimeError('GitHub tra ve danh sach thieu (truncated)')
    return value['tree']


def get_audio_files():
    # Lần theo từng cây thay vì git trees recursive của repo rất lớn.
    ref = 'main'
    for part in ('HSK1', 'fullpinyinwithtones'):
        entries = tree(ref)
        subdir = next((entry for entry in entries if entry.get('path') == part and entry.get('type') == 'tree'), None)
        if not subdir:
            raise RuntimeError('Khong tim thay thu muc GitHub: ' + part)
        ref = subdir['sha']
    entries = tree(ref)
    return sorted(entry['path'] for entry in entries if entry.get('type') == 'blob' and entry['path'].endswith('.mp3'))


def download(name):
    out = TARGET / name
    if out.exists() and out.stat().st_size > 100:
        return 'skip'
    req = urllib.request.Request(RAW + urllib.parse.quote(name), headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
        if len(content) < 100 or content[:3] != b'ID3' and content[:2] not in (b'\xff\xfb', b'\xff\xf3', b'\xff\xf2'):
            # Một vài MP3 có phần đầu khác. Chỉ chặn HTML/JSON báo lỗi tải nhầm.
            if content[:30].lstrip().startswith((b'<!DOCTYPE', b'<html', b'{')):
                return 'bad'
        if len(content) < 100:
            return 'bad'
        tmp = out.with_suffix('.mp3.part')
        tmp.write_bytes(content)
        tmp.replace(out)
        return 'ok'
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return 'error: ' + str(exc)


def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    files = get_audio_files()
    print(f'Dang tai {len(files)} tep MP3 tu qhmusiccorner/Chinese-HSK...')
    counts = {'ok': 0, 'skip': 0, 'bad': 0, 'error': 0}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for idx, result in enumerate(executor.map(download, files), 1):
            counts[result if result in counts else 'error'] += 1
            if idx % 100 == 0 or idx == len(files):
                print(f'{idx}/{len(files)}: {counts}')
    print('Hoan tat:', counts)
    if counts['error'] or counts['bad']:
        print('Co file bi loi; chay lai script de tai bu.')


if __name__ == '__main__':
    main()
