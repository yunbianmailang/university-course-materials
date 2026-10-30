# 大学课程学习资料

个人大学课程笔记与学习资料，按学期、课程和讲次组织。网页适合查找和阅读，PDF 适合平板批注，Word 保留可编辑公式。

**[进入在线阅读站点](https://yunbianmailang.github.io/university-course-materials/)** · [参与贡献](CONTRIBUTING.md) · [许可范围](LICENSE)

## 当前内容

大二上共 **23 讲**，核对日期为 **2026-10-30**。

| 课程 | 讲次 | 获取方式 |
|---|---:|---|
| [复变函数与数理方程](大二上/复变函数与数理方程/README.md) | 1–6 | 网页、PDF、Word |
| [信号与系统](大二上/信号与系统/README.md) | 1–10 | 网页、PDF、Word；前 9 讲为 V3 重制版 |
| [基础物理学2（光学）](大二上/基础物理学2/README.md) | 1–7 | 网页、PDF、Word |

每讲采用“课堂核心速览 → 引导式正文 → 详细参考与拓展”的阅读结构，保留教师例题与课末回顾，不另设成套自测题。学习标识不代替教师公布的考试范围。

## 项目结构

```text
内容源/大二上/<课程>/        可维护的 Markdown 与必要插图
大二上/<课程>/笔记/          唯一正式配套 PDF 与 Word
课程目录.json                讲次、主题、网页路径及文件校验值
网站源/                      项目说明、样式与生成的阅读页面
工具/                        导入、构建与检查工具
mkdocs.yml                   网站配置；导航由课程目录生成
```

网页正文从内容源生成。PDF/Word 作为相应定稿的配套文件，更新时同步维护；构建会核对其校验值，并为网站复制下载文件。课堂录音、照片、整份教材和教师课件保存在本地。被替代的旧讲义保留在 [历史版本](历史版本/README.md)。

## 本地预览与检查

需要 Python 3.12（推荐），也可使用 Python 3.11。

```powershell
python -m pip install -r requirements.txt
python 工具/构建站点.py
python -m mkdocs build --strict
python 工具/检查资料.py
python -m mkdocs serve
```

所有构建输入均在本仓库内，下载项目即可构建，无需访问维护者的个人目录。新增一讲时登记 `课程目录.json`，再运行构建；首页、课程说明与导航会一起更新。维护者如需从现有本地定稿导入，使用 `python 工具/导入本地讲义.py --study-root <原材料目录> --date YYYY-MM-DD`。

当前可使用 `python -m mkdocs gh-deploy` 发布。自动发布方案见 [发布说明](工具/发布说明.md)，以实际启用状态为准。

## 纠错与复用

欢迎通过 Issue 或 Pull Request 改进讲义，注明课程、讲次、章节与依据。参与方法见 [CONTRIBUTING.md](CONTRIBUTING.md)。

原创笔记与原创图示采用 **CC BY-SA 4.0**，原创工具与自定义样式采用 **MIT**。引用的教材、课件、题目与教师原图保留原权利人的权利，不在本项目原创授权范围内。完整说明见 [LICENSE](LICENSE) 与 [来源与许可](网站源/项目说明/来源与许可.md)。
