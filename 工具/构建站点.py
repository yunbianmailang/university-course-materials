"""从仓库内的内容源和课程目录生成网站；不依赖个人电脑路径。"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from 生成索引 import generate
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '网站源'
REPO_URL = 'https://github.com/yunbianmailang/university-course-materials'


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def checked_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError(f'无效的仓库文件路径：{relative}')
    return path


def load_manifest():
    manifest = json.loads((ROOT / '课程目录.json').read_text(encoding='utf-8'))
    seen = set()
    for course in manifest['courses']:
        for lecture in course['lectures']:
            key = (course['name'], lecture['slug'])
            if key in seen:
                raise ValueError(f'重复讲次：{key}')
            seen.add(key)
            checked_path(lecture['source'])
            for download in lecture['downloads'].values():
                path = checked_path(download['path'])
                if hashlib.sha256(path.read_bytes()).hexdigest() != download['sha256']:
                    raise ValueError(f'下载文件已变更，请更新课程目录：{path.name}')
    return manifest


def build():
    manifest = load_manifest()
    cards = []
    nav = ["  - 首页: index.md", "  - 知识点索引: 知识点索引.md", "  - 学习与复习: 学习与复习.md"]
    source_dirs = []
    # 所有删除都限于此仓库的网站生成目录，原始讲义与手写页面不受影响。
    for course in manifest['courses']:
        name = course['name']
        dst = (SITE / name).resolve()
        if not dst.is_relative_to(SITE.resolve()):
            raise ValueError(f'无效课程目录：{name}')
        dst.mkdir(parents=True, exist_ok=True)
        for path in dst.glob('第*讲_*.md'):
            path.unlink()
        figures = dst / '插图'
        if figures.exists():
            shutil.rmtree(figures)
        nav += [f"  - {course['label']}:", f'      - 课程说明: {name}/课程说明.md']
        rows, repo_rows, lecture_links = [], [], []
        for lecture in course['lectures']:
            source = checked_path(lecture['source'])
            if source.parent not in source_dirs:
                source_dirs.append(source.parent)
                if (source.parent / '插图').exists():
                    shutil.copytree(source.parent / '插图', figures, dirs_exist_ok=True)
            downloads = []
            for ext, label in [('pdf', 'PDF 阅读'), ('docx', 'Word 下载')]:
                item = lecture['downloads'][ext]
                # 配套文件由构建时复制，不再在 main 中维护第二份二进制文件。
                downloads.append(f"[{label}](<../文件/{Path(item['path']).name}>)")
            edit = f"{REPO_URL}/edit/main/{quote(lecture['source'], safe='/')}"
            issue = REPO_URL + '/issues/new?template=note-error.yml&title=' + quote(f"[纠错] {name} 第{lecture['number']}讲 ")
            header = f"---\nedit_url: {edit}\n---\n\n# 第{lecture['number']}讲 {lecture['title']}\n\n"
            header += f"**{lecture['version']} · 核对日期 {manifest['updated']}**\n\n"
            header += ' · '.join(downloads) + f' · [报告本讲问题]({issue})\n\n'
            header += '网页与下载版依据同一份定稿整理；网页省略印刷页码，按章节导航阅读。来源和原图说明保留在正文。\n\n'
            body = source.read_text(encoding='utf-8')
            error_no = 0
            def mark_error(match):
                nonlocal error_no
                error_no += 1
                return f'<a id="error-{error_no}"></a>\n\n' + match[0]
            body = re.sub(r'^!!! warning[^\n]*', mark_error, body, flags=re.M)
            write(dst / (lecture['slug'] + '.md'), header + body)
            target = lecture['slug'] + '.md'
            rows.append(f"| 第{lecture['number']}讲 | [{lecture['title']}](<{target}>) | " + ' · '.join(downloads) + ' |')
            repo_rows.append(f"| 第{lecture['number']}讲 | {lecture['title']} | [PDF](<笔记/{Path(lecture['downloads']['pdf']['path']).name}>) · [Word](<笔记/{Path(lecture['downloads']['docx']['path']).name}>) |")
            nav.append(f"      - 第{lecture['number']}讲 {lecture['title']}: {name}/{target}")
            lecture_links.append(f"[第{lecture['number']}讲](<{name}/{target}>)")
        intro = f"# {course['label']}\n\n{course['description']}\n\n已整理 **{len(course['lectures'])} 讲**，均有网页、PDF 和 Word。核对日期：{manifest['updated']}。\n\n"
        table_header = '| 讲次 | 主题 | 配套讲义 |\n|---|---|---|\n'
        write(dst / '课程说明.md', intro + table_header + '\n'.join(rows) + '\n\n[知识点索引](../知识点索引.md) · [学习与复习](../学习与复习.md) · [来源与许可](../项目说明/来源与许可.md)\n')
        write(ROOT / '大二上' / name / 'README.md', intro + table_header + '\n'.join(repo_rows) + '\n\n[在线阅读](https://yunbianmailang.github.io/university-course-materials/) · [贡献说明](../../CONTRIBUTING.md)\n')
        cards.append(f'<div class="course-card" markdown>\n\n### [{course["label"]}](<{name}/课程说明.md>)\n\n**{len(course["lectures"])} 讲 · 网页 / PDF / Word**\n\n{course["description"]}\n\n' + ' · '.join(lecture_links) + '\n\n</div>')
    files_dir = (SITE / '文件').resolve()
    assert files_dir.parent == SITE.resolve()
    if files_dir.exists():
        shutil.rmtree(files_dir)
    files_dir.mkdir()
    names = set()
    for course in manifest['courses']:
        for lecture in course['lectures']:
            for item in lecture['downloads'].values():
                path = checked_path(item['path'])
                if path.name in names:
                    raise ValueError(f'配套文件重名：{path.name}')
                names.add(path.name)
                shutil.copy2(path, files_dir / path.name)
    total = sum(len(c['lectures']) for c in manifest['courses'])
    home = f'''---
hide:
  - toc
---

# 大学课程学习资料

把课堂里没来得及理解的问题，整理成可以反复阅读、查找和修订的学习讲义。

**大二上 · {len(manifest['courses'])} 门课程 · {total} 讲 · 更新于 {manifest['updated']}**

[按知识点查找](知识点索引.md) · [制定阅读路线](学习与复习.md) · [参与纠错](项目说明/参与贡献.md)

## 从一门课开始

''' + '\n\n'.join(cards) + '''

## 怎样使用

- **课前或快速回顾**：先看每讲的课堂核心速览。
- **理解概念与推导**：按问题进入引导式正文，需要时再看详细参考。
- **平板阅读与批注**：打开 PDF；修改内容或公式时下载 Word。
- **发现疑点**：使用每讲顶部的“报告本讲问题”，注明章节、公式与建议。

学习标识是阅读建议；考试范围以教师通知为准。资料来源和引用边界见[来源与许可](项目说明/来源与许可.md)。
'''
    write(SITE / 'index.md', home)
    nav += ['  - 项目说明:', '      - 参与贡献: 项目说明/参与贡献.md', '      - 笔记规范: 项目说明/笔记规范.md', '      - 来源与许可: 项目说明/来源与许可.md', '      - 更新记录: 项目说明/更新记录.md']
    config = ROOT / 'mkdocs.yml'
    text = config.read_text(encoding='utf-8').split('\nnav:', 1)[0]
    write(config, text.rstrip() + '\n\nnav:\n' + '\n'.join(nav) + '\n')
    generate(ROOT, manifest)
    print(f'已生成 {total} 讲、{len(names)} 份配套文件和全部课程目录。')


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    build()
