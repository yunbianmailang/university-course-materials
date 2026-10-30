"""检查课程清单、源稿标记及构建后的本地链接和锚点。"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import runpy
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.ids.add(attrs['name'])
        for attr in ['href', 'src']:
            if attrs.get(attr):
                self.links.append(attrs[attr])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-dir', type=Path, default=ROOT / 'site')
    args = parser.parse_args()
    builder = runpy.run_path(str(ROOT / '工具/构建站点.py'))
    manifest = builder['load_manifest']()
    errors = []
    total = 0
    for course in manifest['courses']:
        numbers = []
        for lecture in course['lectures']:
            total += 1
            numbers.append(lecture['number'])
            text = (ROOT / lecture['source']).read_text(encoding='utf-8')
            if re.search(r'^@\w+', text, re.M):
                errors.append(f"{lecture['source']}：有未转换标记")
            if '第一层' not in text or '第二层' not in text or '第三层' not in text:
                errors.append(f"{lecture['source']}：三层结构不完整")
        if numbers != list(range(1, len(numbers) + 1)):
            errors.append(f"{course['name']}：讲次重复或不连续")
    site = args.site_dir.resolve()
    pages = {}
    for path in site.rglob('*.html'):
        page = Page()
        page.feed(path.read_text(encoding='utf-8'))
        pages[path.resolve()] = page
    if not pages:
        errors.append('没有构建产物，请先运行 python -m mkdocs build --strict')
    link_count = 0
    for path, page in pages.items():
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            relative = unquote(parsed.path)
            if relative.startswith('/university-course-materials/'):
                dest = site / relative.removeprefix('/university-course-materials/')
            elif relative.startswith('/'):
                dest = site / relative.lstrip('/')
            else:
                dest = path.parent / relative if relative else path
            dest = dest.resolve()
            if not dest.is_relative_to(site):
                errors.append(f'{path.relative_to(site)}：链接越出站点 {link}')
                continue
            if dest.is_dir():
                dest /= 'index.html'
            link_count += 1
            if not dest.is_file():
                errors.append(f'{path.relative_to(site)}：目标缺失 {link}')
            elif parsed.fragment and dest.suffix == '.html' and unquote(parsed.fragment) not in pages.get(dest, Page()).ids:
                errors.append(f'{path.relative_to(site)}：锚点缺失 {link}')
    if errors:
        print('\n'.join(errors[:80]))
        raise SystemExit(f'检查失败：共 {len(errors)} 项问题')
    print(f'检查通过：{total} 讲，{len(pages)} 个网页，{link_count} 条站内链接；下载文件校验一致。')


if __name__ == '__main__':
    main()
