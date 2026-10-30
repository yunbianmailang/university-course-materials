"""按已有讲义标题生成知识点与复习入口，不另编课程内容。"""
import re
from pathlib import Path
from urllib.parse import quote

from markdown.extensions.toc import slugify_unicode

TOPICS = [
    ('复数与解析性', ['复数', '复幂', '解析', '柯西', 'Cauchy']),
    ('展开、奇点与留数', ['泰勒', '洛朗', 'Taylor', 'Laurent', '奇点', '留数']),
    ('映射与保角', ['映射', '保角', '分式线性']),
    ('时域、卷积与系统性质', ['卷积', '冲激', '零输入', '零状态', '系统性质']),
    ('傅里叶、频谱与抽样', ['傅里叶', '频谱', '抽样', '采样', '周期延拓']),
    ('拉普拉斯、ROC与稳定性', ['拉普拉斯', '拉氏', '收敛域', '稳定性', '零极点']),
    ('频率响应、滤波与Hilbert', ['频率响应', '滤波', 'Hilbert', '希尔伯特', '无失真']),
    ('几何光学、光程与成像', ['光程', '费马', '界面定律', '透镜', '成像']),
    ('干涉与相干性', ['干涉', '相干', '牛顿环', '劈尖', '迈克耳孙']),
    ('衍射与分辨本领', ['衍射', '光栅', '分辨', '瑞利']),
    ('偏振与晶体光学', ['偏振', '菲涅耳公式', '双折射', '波片', '旋光']),
]


def generate(root, manifest):
    pages = []
    for course in manifest['courses']:
        for lecture in course['lectures']:
            path = root / '网站源' / course['name'] / (lecture['slug'] + '.md')
            text = path.read_text(encoding='utf-8')
            # 与 MkDocs 的 Unicode 标题锚点规则保持一致，并处理同名标题。
            seen, headings = {}, []
            for heading in re.findall(r'^#{1,6} (.+)$', text, re.M):
                base = slugify_unicode(heading, '-')
                index = seen.get(base, 0)
                seen[base] = index + 1
                anchor = base + (f'_{index}' if index else '')
                headings.append((heading, anchor))
            pages.append((course, lecture, path, text, headings))
    lines = ['# 知识点索引', '', '按已有讲义的章节标题查找。每个入口直达正文位置；搜索框也支持检索讲义内容。', '']
    for title, words in TOPICS:
        hits = []
        for course, lecture, path, text, headings in pages:
            match = next(((h, a) for h, a in headings[1:] if any(w.lower() in h.lower() for w in words)), None)
            if match:
                h, a = match
                target = f"{course['name']}/{lecture['slug']}.md#{a}"
                hits.append(f"- {course['label']} · 第{lecture['number']}讲：[ {h} ](<{target}>)")
        lines += ['## ' + title, ''] + hits + ['']
    lines += ['## 跨课程阅读入口', '', '- 留数计算与复积分 → 拉普拉斯逆变换：对照复变函数与信号与系统的相关章节。', '- 傅里叶与频谱 → 光的衍射：对照信号的频域表示与光学的衍射模型。', '- 复数幅相 → 干涉与偏振：对照复数几何、频率响应和光场叠加的符号约定。', '', '这些入口用于联结已有内容；不同课程的变换约定、变量与近似条件仍需分别核对。', '']
    (root / '网站源/知识点索引.md').write_text('\n'.join(lines), encoding='utf-8')
    lines = ['# 学习与复习', '', '## 选一条阅读路线', '', '- **课前 3–5 分钟**：课堂核心速览 → 核心问题与先修 → 本讲重点。', '- **课后理解**：按薄弱知识点读正文，保留模型条件和关键推导；需要时进入详细参考。', '- **复习定位**：先看课末回顾与公式入口，再回到不熟悉的例题和易错处。', '- **平板批注**：使用每讲顶部的 PDF；修改内容或公式时下载 Word。', '', '## 公式、回顾与易错入口', '', '以下入口从各讲既有内容生成，完整条件和推导在原讲义中。', '', '| 课程 | 讲次 | 公式与回顾 | 易错提醒 |', '|---|---|---|---|']
    for course, lecture, path, text, headings in pages:
        base = f"{course['name']}/{lecture['slug']}.md"
        match = next(((h, a) for h, a in headings if '回顾' in h), None)
        match = match or next(((h, a) for h, a in headings if '重要结论' in h or '公式' in h), None)
        formula = f'[{match[0]}](<{base}#{match[1]}>)' if match else f'[本讲正文](<{base}>)'
        error = f'[易错提醒](<{base}#error-1>)' if 'id="error-1"' in text else f'[本讲正文](<{base}>)'
        lines.append(f"| {course['label']} | 第{lecture['number']}讲 | {formula} | {error} |")
    lines += ['', '先修知识、定理条件、近似范围与符号约定应与公式一同阅读。教师布置的作业用于练习，本项目不另设成套自测题。', '']
    (root / '网站源/学习与复习.md').write_text('\n'.join(lines), encoding='utf-8')
