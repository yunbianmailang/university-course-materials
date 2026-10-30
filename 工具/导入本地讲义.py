"""将已定稿的本地讲义导入可独立构建的公开内容源；不改动原始资料。"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CN = dict(enumerate(['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'], 1))
COURSES = [
    ('复变函数与数理方程', 6, '数学逻辑与证明：从定义、条件和证明思路进入典型应用。'),
    ('信号与系统', 10, '解题引导：联系时域、频域和复频域，明确模型与适用条件。'),
    ('基础物理学2', 7, '物理图像驱动：把实验、光路、模型假设与公式联系起来。'),
]


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8-sig')


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def tables_from(path: Path) -> dict:
    """只读取表格字面量，不运行本地制作脚本。"""
    if not path.exists():
        return {}
    values = {}
    def value(node):
        if isinstance(node, ast.Name):
            return values[node.id]
        if isinstance(node, ast.List):
            return [value(n) for n in node.elts]
        if isinstance(node, ast.Tuple):
            return tuple(value(n) for n in node.elts)
        if isinstance(node, ast.Dict):
            return {value(k): value(v) for k, v in zip(node.keys, node.values)}
        return ast.literal_eval(node)
    for node in ast.parse(read(path)).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    values[target.id] = value(node.value)
    return values.get('TABLES', {})


def table_markdown(rows: list) -> str:
    def cell(value):
        return str(value).replace('|', r'\|').replace('\n', ' ')
    lines = ['| ' + ' | '.join(map(cell, rows[0])) + ' |', '|' + '---|' * len(rows[0])]
    lines += ['| ' + ' | '.join(map(cell, row)) + ' |' for row in rows[1:]]
    return '\n'.join(lines)


def convert(text: str, kind: str, figures: Path, target: Path, no: int, tables: dict) -> str:
    out = []
    copied = set()

    def image(name, caption=''):
        # 与 Word 制作脚本使用同一 PNG，避免使用过期的同名 SVG。
        source = next((figures / (name + ext) for ext in ['.png', '.svg', '.jpg'] if (figures / (name + ext)).is_file()), None)
        if source is None:
            raise FileNotFoundError(f'第{no}讲缺图：{figures / name}')
        rel = Path('插图') / f'第{no}讲' / source.name
        dest = target.parent / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        copied.add(source.name)
        out.append(f'![{caption or name}](<{rel.as_posix()}> ){{ loading=lazy }}'.replace('> )', '>)'))
        if caption:
            out.append('*' + caption + '*')

    def callout(kind, text):
        title, sep, body = text.partition('｜')
        if not sep:
            title, body = {'abstract': ('核心结论', text), 'info': ('思路提示', text), 'warning': ('易错提醒', text)}[kind]
        title = title.replace('"', '”')
        out.append(f'!!! {kind} "{title}"\n\n    ' + body.replace('\n', '\n    '))

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line in ['@break', '@contents']:
            continue
        if line.startswith('@figure '):
            args = line.split(' ', 2)
            image(args[1], args[2] if len(args) > 2 else '')
        elif line.startswith('@fig '):
            name, caption = line[5:].split('|', 1)
            image(name.strip(), caption.strip())
        elif line.startswith('@table '):
            key = line[7:]
            if key not in tables:
                raise ValueError(f'第{no}讲缺表：{key}')
            out.append(table_markdown(tables[key][0]))
        elif line.startswith('@eq '):
            number, formula = line[4:].split('|', 1)
            out.append('$$\n' + formula.strip() + r'\tag{' + number.strip() + '}\n$$')
        elif line.startswith('@nav '):
            out.append('### ' + line[5:])
        elif line.startswith('@source '):
            out.append('> **资料范围**：' + line[8:])
        elif line.startswith('@level '):
            level, _, goal = line[7:].partition('｜')
            out.append('**【' + level + '】** ' + goal)
        elif line.startswith('@layer '):
            out.append('## ' + line[7:])
        elif line.startswith('@lead '):
            out.append('#### ' + line[6:])
        elif re.match(r'^@(A|B|C|core|idea|warn) ', line):
            marker, body = line[1:].split(' ', 1)
            callout({'A': 'abstract', 'B': 'info', 'C': 'warning', 'core': 'abstract', 'idea': 'info', 'warn': 'warning'}[marker], body)
        elif (m := re.match(r'^【([ABC]) ([^】]+)】\s*(.*)', line)):
            callout({'A': 'abstract', 'B': 'info', 'C': 'warning'}[m[1]], m[2] + '｜' + m[3])
        elif line.startswith('@'):
            raise ValueError(f'未处理的源稿标记：{line}')
        elif (m := re.fullmatch(r'\$\$(.*?)\$\$(.*)', line)):
            out.append('$$\n' + m[1] + '\n$$')
            if m[2].strip():
                out.append(m[2].strip())
        elif line.startswith('#'):
            shift = 2 if kind == 'signal' else 1
            out.append('#' * shift + line)
        else:
            out.append(line)
    return '\n'.join(line.rstrip() for line in '\n\n'.join(out).splitlines()) + '\n'


def source_for(study: Path, course: str, no: int):
    folder = study / course / f'第{CN[no]}节课'
    if course == '信号与系统':
        kind = 'signal'
        base = study / course / '.制作' / ('统一重制_20261027/第' + str(no) + '讲' if no <= 9 else '第十节课')
        stem = f'信号与系统_第{no}讲_学习讲义_V3重制版' if no <= 9 else '信号与系统_第10讲_频域响应与理想滤波_学习讲义'
        topic = json.loads(read(base / 'title.json'))['topic'] if no <= 9 else '频域响应与理想滤波'
        text = read(base / '正文.md')
        audio = base / '录音补充.json'
        if audio.exists():
            for anchor, extra in json.loads(read(audio)).items():
                if anchor not in text:
                    raise ValueError(f'录音补充锚点缺失：{no} {anchor}')
                text = text.replace(anchor, anchor + '\n' + extra, 1)
        labels = ['本节课的核心问题', '必要先修知识', '核心知识结构', '重要结论与条件', '课堂听讲重点']
        if no <= 9:
            nav = json.loads(read(base / 'navigation.json'))
        else:
            # 提取制作脚本中既有导航文本；不执行脚本，不另编课程内容。
            tree = ast.parse(read(base / 'build.py'))
            nav, active = [], False
            for node in tree.body:
                if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'p'):
                    continue
                args = node.value.args
                if not args or not isinstance(args[0], ast.Constant) or not isinstance(args[0].value, str):
                    continue
                value = args[0].value
                if value == '第一层 课堂核心速览':
                    active = True; continue
                if active and value == '目录与学习标识':
                    break
                if active:
                    if re.match(r'^[1-5] ', value):
                        nav.append('')
                    else:
                        nav[-1] += ('\n\n' if nav[-1] else '') + value
        assert len(nav) == 5
        figures = base / 'figures'
        tables = tables_from(base / 'tables.py')
        prefix = '## 第一层 课堂核心速览\n\n' + '\n\n'.join('### ' + label + '\n\n' + body for label, body in zip(labels, nav))
        prefix += '\n\n## 第二层 引导式学习正文\n\n'
    elif course == '基础物理学2':
        kind = 'physics'
        base = folder / '_制作/V3'
        pdfs = list(folder.glob(f'基础物理学2_第{no}讲_*_学习讲义.pdf'))
        assert len(pdfs) == 1
        stem = pdfs[0].stem
        topic = stem.split(f'_第{no}讲_', 1)[1].removesuffix('_学习讲义')
        text = '\n\n'.join(read(base / name) for name in ['导航卡.md', '正文.md', '参考与回顾.md'])
        figures, tables, prefix = base / 'figures', {}, ''
    else:
        kind = 'complex'
        base = study / course / '.制作' / (f'前四讲重制/第{CN[no]}讲' if no <= 4 else f'第{CN[no]}节课')
        pdfs = list(folder.glob(f'{course}_第{no}讲_*_学习讲义.pdf'))
        assert len(pdfs) == 1
        stem = pdfs[0].stem
        topic = stem.split(f'_第{no}讲_', 1)[1].removesuffix('_学习讲义')
        text = read(base / '讲义源稿.md')
        figures, tables, prefix = base / '插图', {}, ''
    return folder, stem, topic, kind, text, figures, tables, prefix


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study-root', required=True, type=Path, help='本地原材料工作区；不会上传整个目录')
    parser.add_argument('--date', required=True, help='本次核对日期，YYYY-MM-DD')
    args = parser.parse_args()
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', args.date):
        parser.error('--date 应为 YYYY-MM-DD')
    # 先验证所有输入，缺资料时不改已有网站。
    jobs = [(course, no, source_for(args.study_root, course, no)) for course, count, _ in COURSES for no in range(1, count + 1)]
    manifest = {'schema_version': 1, 'updated': args.date, 'semester': '大二上', 'author': 'yunbianmailang', 'courses': []}
    for course, count, description in COURSES:
        info = {'name': course, 'label': course + ('（光学）' if course == '基础物理学2' else ''), 'description': description, 'lectures': []}
        for _, no, job in (j for j in jobs if j[0] == course):
            folder, stem, topic, kind, text, figures, tables, prefix = job
            # 保留已有网页路径，避免既有收藏失效。
            old = list((ROOT / '网站源' / course).glob(f'第{no}讲_*.md'))
            slug = old[0].stem if len(old) == 1 else f'第{no}讲_{topic}'
            source = Path('内容源') / '大二上' / course / f'第{no:02d}讲.md'
            target = ROOT / source
            body = prefix + convert(text, kind, figures, target, no, tables)
            if re.search(r'自测题|闭卷自测|自测答案', body):
                raise ValueError(f'{course}第{no}讲源稿仍含旧自测模块，请核对')
            write(target, body)
            downloads = {}
            for ext in ['pdf', 'docx']:
                src = folder / (stem + '.' + ext)
                dest = Path('大二上') / course / '笔记' / src.name
                (ROOT / dest).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, ROOT / dest)
                downloads[ext] = {'path': dest.as_posix(), 'sha256': hashlib.sha256(src.read_bytes()).hexdigest()}
            info['lectures'].append({'number': no, 'title': topic, 'slug': slug, 'source': source.as_posix(), 'version': 'V3.0', 'downloads': downloads})
            print(f'{course} 第{no}讲：源稿、插图、PDF、Word 已导入')
        manifest['courses'].append(info)
    write(ROOT / '课程目录.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
