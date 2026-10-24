# -*- coding: utf-8 -*-
"""把三门课的《讲义源稿.md》转换为 MkDocs 网页版。

三门课的 Markdown 方言不同，本脚本按课程分派转换规则：
- 复变函数与数理方程:【A/B/C 标题】强调模块、【必须掌握】等优先级徽章、@figure 裸标记
- 信号与系统:「前缀｜」模块（易错提醒/录音补充/资料内容…）、@figure 名称+图注、@table 数据表
- 基础物理学2:【PPT重点】等来源徽章、@fig 名称|图注、@source 资料范围

输入只读；产物写入 仓库/网站源/<课程>/ 与 仓库/网站源/文件/。
每次运行先清空各课程的生成目录再重建，保证无残留。
新增一讲：在对应课程的 LECTURES 里加一行，运行本脚本，再在 mkdocs.yml 的 nav 里登记。
用法: python 工具/转换网页版.py
"""
import ast
import re
import shutil
import sys
from pathlib import Path

STUDY = Path(r"D:\Development\Codex\学习")
REPO = Path(r"D:\Development\Codex\大学课程学习资料")
SITE = REPO / "网站源"
FILES_DIR = SITE / "文件"

ADMONITION_TYPE = {"A": "abstract", "B": "info", "C": "warning"}

# 徽章样式：class → 标签文本集合
PILL_CLASS = {
    "pill-must": {"必须掌握"},
    "pill-rec": {"建议理解", "本课约定"},
    "pill-ext": {"拓展阅读", "了解即可"},
    "pill-ppt": {"PPT重点", "PPT图示", "课堂数值例", "课堂思考"},
    "pill-src": {"资料内容", "资料例题", "资料内容与校核", "教材补充"},
    "pill-und": {"理解补充"},
}


def pill_for(tag: str):
    """按标签文本（忽略后缀）返回徽章 class，未登记返回 None。"""
    base = tag.split()[0] if tag.split() else tag
    for cls, names in PILL_CLASS.items():
        if tag in names or base in names:
            return cls
    return None


def badge_replace(text: str, warn_missing: set):
    """把【标签】替换为 <span class="pill ...">标签</span>。"""
    def repl(m):
        tag = m.group(1)
        cls = pill_for(tag)
        if cls is None:
            warn_missing.add(tag)
            return m.group(0)
        return f'<span class="pill {cls}">{tag}</span>'
    return re.sub(r"【([^【】]{2,14})】", repl, text)


def isolate_display_math(out: list) -> list:
    """独行 $$...$$ 公式前后补空行，避免与段落文字同段导致定界符配对错乱。"""
    res = []
    n = len(out)
    for idx, ln in enumerate(out):
        s = ln.strip()
        if re.fullmatch(r"\$\$.+\$\$", s):
            if res and res[-1].strip() and not res[-1].strip().startswith("!!!"):
                res.append("")
            res.append(ln)
            nxt = out[idx + 1].strip() if idx + 1 < n else ""
            if nxt and not nxt.startswith("!!!"):
                res.append("")
        else:
            res.append(ln)
    return res


def embed_figure(name: str, caption: str, figdir: Path, rel_dir: str, lecture_tag: str, copied: set) -> list:
    """生成图片（+可选图注）嵌入行，前后补空行。"""
    src = None
    for ext in (".svg", ".png"):
        p = figdir / f"{name}{ext}"
        if p.exists():
            src = p
            break
    if src is None:
        raise FileNotFoundError(f"{lecture_tag} 缺少插图 {name}（在 {figdir}）")
    copied.add(src.name)
    lines = ["", f"![{lecture_tag} 插图 {name}]({rel_dir}/{lecture_tag}/{src.name}){{ loading=lazy }}"]
    if caption:
        lines.append(f"*{caption}*")
    lines.append("")
    return lines


def structural(line: str) -> bool:
    s = line.strip()
    return (not s) or s.startswith("#") or s.startswith("@") or s.startswith("!!!") or bool(re.match(r"^【[ABC] ", s))


def render_table(data, warn: list, name: str) -> list:
    """把 [header, row...] 的表格数据渲染为 Markdown 表格。"""
    if not data or not isinstance(data, list):
        warn.append(f"表格 {name} 数据缺失")
        return ["", f"*表格 {name} 数据缺失*", ""]
    esc = lambda c: str(c).replace("|", "\\|").replace("\n", " ")
    header = [esc(c) for c in data[0]]
    lines = ["", "| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for row in data[1:]:
        cells = [esc(c) for c in row] + [""] * (len(header) - len(row))
        lines.append("| " + " | ".join(cells[: len(header)]) + " |")
    lines.append("")
    return lines


def extract_tables(py_paths) -> dict:
    """用 ast 从 build 脚本里安全提取 list 常量形式的表格定义（不执行脚本）。"""
    tables = {}
    for p in py_paths:
        if not p.exists():
            continue
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and isinstance(node.value, (ast.List, ast.Tuple)):
                        try:
                            tables.setdefault(t.id, ast.literal_eval(node.value))
                        except Exception:
                            pass
    return tables


def conv_fubian(raw: list, figdir: Path, lecture_tag: str, copied: set, warnings: list) -> list:
    out, i = [], 0
    while i < len(raw):
        s = raw[i].strip()
        m = re.match(r"^@figure\s+(\S+)\s*$", s)
        if m:
            out.extend(embed_figure(m.group(1), "", figdir, "插图", lecture_tag, copied))
            i += 1
            continue
        m = re.match(r"^【([ABC]) ([^】]+)】\s*(.*)$", s)
        if m:
            kind, title, first = m.groups()
            body = [first] if first else []
            i += 1
            while i < len(raw) and not structural(raw[i]):
                body.append(raw[i].strip())
                i += 1
            out.append(f'!!! {ADMONITION_TYPE[kind]} "{title}"')
            for pl in body:
                out.extend("    " + x for x in badge_replace(pl, set()).splitlines())
            out.append("")
            continue
        ln = raw[i]
        if re.match(r"^#{1,5} ", ln):
            ln = "#" + ln
        out.append(badge_replace(ln, set()))
        i += 1
    return out


# 信号的「前缀｜」模块
SIGNAL_CALLOUT = {  # 前缀 → (admonition 类型, 标题)
    "易错提醒": "warning",
    "资料校核": "warning",
    "录音补充": "info",
    "补充讲解": "info",
    "补充推导": "info",
    "补充例题": "info",
    "补充提醒": "info",
    "题设补足": "info",
}
SIGNAL_PILL = {"资料内容": "pill-src", "资料例题": "pill-src", "资料内容与校核": "pill-src", "本课约定": "pill-rec"}


def conv_signal(raw: list, figdir: Path, lecture_tag: str, copied: set, warnings: list, tables: dict) -> list:
    out, i = [], 0
    while i < len(raw):
        s = raw[i].strip()
        m = re.match(r"^@figure\s+(\S+)\s*(.*)$", s)
        if m:
            caption = re.sub(r"\s{2,}", " ", m.group(2)).strip()
            out.extend(embed_figure(m.group(1), caption, figdir, "插图", lecture_tag, copied))
            i += 1
            continue
        m = re.match(r"^@table\s+(\S+)\s*$", s)
        if m:
            out.extend(render_table(tables.get(m.group(1)), warnings, m.group(1)))
            i += 1
            continue
        m = re.match(r"^([^｜\n]{2,8})｜\s*(.*)$", s)
        if m:
            tag, first = m.group(1), m.group(2)
            if tag in SIGNAL_CALLOUT:
                body = [first] if first else []
                i += 1
                while i < len(raw) and not structural(raw[i]):
                    body.append(raw[i].strip())
                    i += 1
                out.append(f'!!! {SIGNAL_CALLOUT[tag]} "{tag}"')
                for pl in body:
                    out.append("    " + pl)
                out.append("")
                continue
            if tag in SIGNAL_PILL:
                rest = f'<span class="pill {SIGNAL_PILL[tag]}">{tag}</span> ' + first
                out.append(rest)
                i += 1
                continue
        ln = raw[i]
        if re.match(r"^#{1,5} ", ln):
            ln = "#" + ln
        out.append(ln)
        i += 1
    return out


# 基物2 的【】标签
PHYS_TAG = re.compile(
    r"【(PPT重点[^】]*|理解补充[^】]*|教材补充[^】]*|必须掌握|建议理解|了解即可|PPT图示|课堂数值例|课堂思考)】"
)


def conv_physics(raw: list, figdir: Path, lecture_tag: str, copied: set, warnings: list) -> list:
    out, i = [], 0
    while i < len(raw):
        s = raw[i].strip()
        m = re.match(r"^@fig\s+([^|｜]+)\|(.*)$", s)
        if m:
            out.extend(embed_figure(m.group(1).strip(), m.group(2).strip(), figdir, "插图", lecture_tag, copied))
            i += 1
            continue
        m = re.match(r"^@source\s+(.*)$", s)
        if m:
            out.extend(["", f"> **资料范围**：{m.group(1).strip()}", ""])
            i += 1
            continue

        def phys_pill(mm):
            return f'<span class="pill {pill_for(mm.group(1)) or "pill-ppt"}">{mm.group(1)}</span>'

        ln = PHYS_TAG.sub(phys_pill, raw[i])
        if re.match(r"^#{1,5} ", ln):
            ln = "#" + ln
        out.append(ln)
        i += 1
    return out


def topic_from_h1(first_h1: str, fallback: str) -> str:
    t = re.sub(r"^[\d\s.\-、]+", "", first_h1).strip()
    return t or fallback


def main() -> int:
    ok = True
    # 每次全量重建：清掉各课程的生成物（讲次页面与插图），保留手写的课程说明.md
    for d in ("复变函数与数理方程", "信号与系统", "基础物理学2"):
        d = SITE / d
        if d.exists():
            for f in d.glob("第*讲_*.md"):
                f.unlink()
            shutil.rmtree(d / "插图", ignore_errors=True)
    shutil.rmtree(FILES_DIR, ignore_errors=True)
    FILES_DIR.mkdir(parents=True, exist_ok=True)

    # ---------- 课程定义 ----------
    FUB = STUDY / "复变函数与数理方程"
    SIG = STUDY / "信号与系统"
    PHY = STUDY / "基础物理学2"

    fubian_lectures = []
    for cn, no in (("一", 1), ("二", 2), ("三", 3), ("四", 4), ("五", 5)):
        src_dir = FUB / ".制作" / (f"前四讲重制/第{cn}讲" if no <= 4 else "第五节课")
        folder = FUB / f"第{cn}节课"
        pdf = next(folder.glob(f"复变函数与数理方程_第{no}讲_*_学习讲义.pdf"))
        topic = re.match(rf"复变函数与数理方程_第{no}讲_(.+)_学习讲义", pdf.name).group(1)
        fubian_lectures.append(
            dict(no=no, topic=topic, md=[src_dir / "讲义源稿.md"], figdir=src_dir / "插图",
                 files=[pdf.name, pdf.name[:-4] + ".docx"], filedir=folder))

    signal_lectures = []
    sig_meta = [
        # (正文md, 图目录子文件夹, 配套文件, 页面主题——按各讲正文实际内容概括)
        (1, ["正文.md"], None, ["第一节课 信号与系统自学笔记.docx"], "学习路线与基本语言"),
        (2, ["正文.md"], None, ["第二节课 信号与系统自学笔记.docx"], "微分方程经典法与响应分解"),
        (3, ["正文.md"], None, ["第三节课 信号与系统自学笔记.docx"], "傅里叶级数与频谱"),
        (4, ["正文.md"], None, ["第四节课 信号与系统自学笔记.docx"], "傅里叶变换与典型信号频谱"),
        (5, ["正文.md", "后半.md"], "figures", ["第五节课 信号与系统自学笔记 修订稿.docx"], "典型变换对与抽样定理"),
        (6, ["正文.md", "后半.md"], "figures", ["第六节课 信号与系统自学笔记.docx"], "拉普拉斯变换的性质"),
        (7, ["正文.md"], "figures", ["第七节课 信号与系统自学笔记.docx"], "拉普拉斯逆变换与 s 域模型"),
        (8, ["正文.md"], "figures", ["信号与系统_第8讲_频率响应与稳定性_学习讲义.docx",
                                     "信号与系统_第8讲_频率响应与稳定性_学习讲义.pdf"], "频率响应与稳定性"),
    ]
    for cn, no in (("一", 1), ("二", 2), ("三", 3), ("四", 4), ("五", 5), ("六", 6), ("七", 7), ("八", 8)):
        _, mds, figsub, files, topic = sig_meta[no - 1]
        mk = SIG / ".制作" / f"第{cn}节课"
        folder = SIG / f"第{cn}节课"
        figdir = mk / figsub if figsub else mk
        signal_lectures.append(dict(no=no, topic=topic, md=[mk / m for m in mds], figdir=figdir,
                                    files=files, filedir=folder))

    physics_lectures = []
    for cn, no in (("一", 1), ("二", 2), ("三", 3), ("四", 4), ("五", 5), ("六", 6), ("七", 7)):
        folder = PHY / f"第{cn}节课"
        pdf = next(folder.glob(f"基础物理学2_第{no}讲_*_学习讲义.pdf"))
        topic = re.match(rf"基础物理学2_第{no}讲_(.+)_学习讲义", pdf.name).group(1)
        files = [pdf.name, pdf.name[:-4] + ".docx"]
        zsd = list(folder.glob(f"基础物理学2_第{no}讲_*_知识点总结.pdf"))
        if zsd:
            files += [zsd[0].name, zsd[0].name[:-4] + ".docx"]
        physics_lectures.append(dict(no=no, topic=topic, md=[folder / "_制作" / "正文.md"],
                                     figdir=folder / "_制作" / "figures", files=files, filedir=folder))

    jobs = [
        ("复变函数与数理方程", "fubian", fubian_lectures),
        ("信号与系统", "signal", signal_lectures),
        ("基础物理学2", "physics", physics_lectures),
    ]

    for course_name, kind, lectures in jobs:
        course_dir = SITE / course_name
        course_dir.mkdir(parents=True, exist_ok=True)
        for lec in lectures:
            lecture_tag = f"第{lec['no']}讲"
            figdir = lec["figdir"]
            copied = set()
            raw = []
            for p in lec["md"]:
                raw.extend(p.read_text(encoding="utf-8").splitlines())
                raw.append("")
            first_h1 = next((ln.lstrip("# ").strip() for ln in raw if re.match(r"^#\s", ln)), "")

            # 主题：优先用文件名里的主题，信号1-7讲回退到 md 首个一级标题
            topic = lec["topic"] or topic_from_h1(first_h1, f"信号与系统自学笔记")

            warnings = []
            tables = extract_tables([figdir.parent / "tables.py", figdir.parent / "build.py"]) if kind == "signal" else {}
            if kind == "fubian":
                body = conv_fubian(raw, figdir, lecture_tag, copied, warnings)
            elif kind == "signal":
                body = conv_signal(raw, figdir, lecture_tag, copied, warnings, tables)
            else:
                body = conv_physics(raw, figdir, lecture_tag, copied, warnings)

            # 复制插图
            dst_fig = course_dir / "插图" / lecture_tag
            dst_fig.mkdir(parents=True, exist_ok=True)
            n_fig = 0
            for f in sorted(figdir.glob("*")):
                if f.is_file() and f.suffix.lower() in (".png", ".svg", ".jpg"):
                    shutil.copy2(f, dst_fig / f.name)
                    n_fig += 1

            # 复制讲义文件
            links = []
            for name in lec["files"]:
                src = lec["filedir"] / name
                if not src.exists():
                    warnings.append(f"缺失文件 {name}")
                    continue
                shutil.copy2(src, FILES_DIR / name)
                label = "PDF 在线阅读" if name.endswith(".pdf") else "Word 下载"
                if "知识点总结" in name:
                    label = "知识点总结 PDF" if name.endswith(".pdf") else "知识点总结 Word"
                links.append(f"    - [{label}（{name}）](../文件/{name})")
            header = "!!! tip \"本讲配套文件\"\n" + "\n".join(links) if links else ""

            page_body = "\n".join(isolate_display_math(body)).replace("\n\n\n\n", "\n\n")
            page = course_dir / f"{lecture_tag}_{topic}.md"
            page.write_text(f"# {lecture_tag} {topic}\n\n{header}\n\n{page_body}\n", encoding="utf-8")

            # 插图引用校验：源里引用的都复制了吗
            missing = [n for n in copied if not (dst_fig / n).exists()]
            status = "OK" if not (warnings or missing) else "有警告"
            print(f"[{course_name}] {lecture_tag} {topic}: 插图{n_fig} 引用{len(copied)} 表格{len(tables)} {status}")
            for w in warnings + [f"缺图 {m}" for m in missing]:
                print(f"    ! {w}")
                ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
