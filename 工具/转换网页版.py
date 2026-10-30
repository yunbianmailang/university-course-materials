"""兼容原有命令；网页现在直接从仓库内的内容源生成。"""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).with_name('构建站点.py')), run_name='__main__')
