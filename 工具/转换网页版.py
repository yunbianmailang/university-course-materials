# -*- coding: utf-8 -*-
"""把复变函数与数理方程各讲《讲义源稿.md》转换为 MkDocs 网页版。

输入只读；所有产物写入仓库的 网站源/ 目录。新增一讲时在 LECTURES 里加一行再运行本脚本。
用法: python 工具/转换网页版.py
"""
import re
import shutil
import sys
from pathlib import Path

SRC_ROOT = Path(r"D:\Development\Codex\学习\复变函数与数理方程\.制作")
COURSE_SRC = Path(r"D:\Development\Codex\学习\复变函数与数理方程")
REPO = Path(r"D:\Development\Codex\大学课程学习资料")
SITE = REPO / "网站源"

# (讲次目录, 插图目录, 正式讲义所在课次目录, 讲次号)
LECTURES = [
    (SRC_ROOT / "前四讲重制" / "第一讲", "第一节课", 1),
    (SRC_ROOT / "前四讲重制" / "第二讲", "第二节课", 2),
    (SRC_ROOT / "前四讲重制" / "第三讲", "第三节课", 3),
    (SRC_ROOT / "前四讲重制" / "第四讲", "第四节课", 4),
    (SRC_ROOT / "第五节课", "第五节课", 5),
]

ADMONITION_TYPE = {"A": "abstract", "B": "info", "C": "warning"}
PRIORITY_BADGE = {
    "必须掌握": '<span class="pill pill-must">必须掌握</span>',
    "建议理解": '<span class="pill pill-rec">建议理解</span>',
    "拓展阅读": '<span class="pill pill-ext">拓展阅读</span>',
}


def find_handout(lecture_dir: Path, no: int, folder: str):
    """按命名规范找到该讲的正式 PDF 和 Word 文件名。"""
    pattern = f"复变函数与数理方程_第{no}讲_*_学习讲义"
    hits = list((COURSE_SRC / folder).glob(pattern + ".pdf"))
    if len(hits) != 1:
        raise FileNotFoundError(f"第{no}讲 正式PDF未唯一找到: {hits}")
    pdf_name = hits[0].name
    return pdf_name, pdf_name[:-4] + ".docx"


def convert_line(line: str, lecture_tag: str, figures_dir: Path, used_names: set) -> str:
    """转换单行：插图标记、优先级徽章。"""
    m = re.match(r"^@figure\s+(\S+)\s*$", line)
    if m:
        name = m.group(1)
        used_names.add(name)
        if (figures_dir / f"{name}.svg").exists():
            ext = "svg"
        elif (figures_dir / f"{name}.png").exists():
            ext = "png"
        else:
            raise FileNotFoundError(f"第{lecture_tag}讲 缺少插图 {name}")
        return f"![{lecture_tag} 插图 {name}](插图/{lecture_tag}/{name}.{ext}){{ loading=lazy }}\n"
    for tag, badge in PRIORITY_BADGE.items():
        line = line.replace(f"【{tag}】", badge)
    return line


def is_structural(line: str) -> bool:
    """模块块遇到这些行必须截止：空行、标题、@标记、新的【X】模块。"""
    s = line.strip()
    if not s:
        return True
    if re.match(r"^#{1,5} ", s):
        return True
    if s.startswith("@"):
        return True
    if re.match(r"^【[ABC] ", s):
        return True
    return False


def convert(src: Path, lecture_tag: str, figures_dir: Path) -> str:
    lines = src.read_text(encoding="utf-8").splitlines()
    out, used_names = [], set()
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        # 制作流程标记：整行移除
        if stripped in ("@break", "@contents"):
            i += 1
            continue
        m = re.match(r"^【([ABC]) ([^】]+)】\s*(.*)$", stripped)
        if m:
            kind, title, first = m.groups()
            body = [first] if first else []
            i += 1
            while i < len(lines) and not is_structural(lines[i]):
                body.append(lines[i].strip())
                i += 1
            out.append(f'!!! {ADMONITION_TYPE[kind]} "{title}"')
            for para in body:
                para = convert_line(para, lecture_tag, figures_dir, used_names)
                for pl in para.splitlines():
                    out.append("    " + pl)
            out.append("")
            continue
        # 普通行：标题降一级，其余按行转换
        if re.match(r"^#{1,5} ", raw):
            raw = "#" + raw
        out.append(convert_line(raw, lecture_tag, figures_dir, used_names))
        i += 1

    # 收尾：清除多余空行（3 连空行压成 1 行由 markdown 处理，这里只保结尾整洁）
    text = "\n".join(out).replace("\n\n\n\n", "\n\n")
    return text, used_names


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


def main() -> int:
    ok = True
    for lecture_dir, folder, no in LECTURES:
        src = lecture_dir / "讲义源稿.md"
        if not src.exists():
            print(f"[跳过] {src} 不存在")
            continue
        pdf_name, docx_name = find_handout(lecture_dir, no, folder)
        topic = re.match(rf"复变函数与数理方程_第{no}讲_(.+)_学习讲义", pdf_name).group(1)
        lecture_tag = f"第{no}讲"
        page_slug = f"{lecture_tag}_{topic}"

        # 插图复制
        figures_dir = lecture_dir / "插图"
        dst_fig = SITE / "插图" / lecture_tag
        dst_fig.mkdir(parents=True, exist_ok=True)
        n_fig = 0
        for f in figures_dir.glob("*"):
            shutil.copy2(f, dst_fig / f.name)
            n_fig += 1

        # 讲义文件复制到站点文件区
        dst_files = SITE / "文件"
        dst_files.mkdir(parents=True, exist_ok=True)
        for name in (pdf_name, docx_name):
            shutil.copy2(COURSE_SRC / folder / name, dst_files / name)

        # 转换正文
        body, used = convert(src, lecture_tag, figures_dir)
        body_lines = isolate_display_math(body.splitlines())
        body = "\n".join(body_lines)
        head = (
            f"# {lecture_tag} {topic}\n\n"
            f"!!! tip \"本讲配套文件\"\n"
            f"    - [在线阅读 PDF（排版与 Word 版一致）](文件/{pdf_name})\n"
            f"    - [下载 Word 版（公式可编辑）](文件/{docx_name})\n\n"
        )
        page = SITE / f"{page_slug}.md"
        page.write_text(head + body, encoding="utf-8")

        # 校验：源稿引用的插图是否都存在
        fig_names = {m.group(1) for m in re.finditer(r"^@figure\s+(\S+)\s*$", src.read_text(encoding="utf-8"), re.M)}
        missing = fig_names - used
        print(f"[完成] {page_slug}.md  插图{n_fig}个  引用{len(fig_names)}个  未引用{sorted(missing) if missing else '无'}")
        if missing:
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
