# -*- coding: utf-8 -*-
"""生成词云的命令行工具

用法:

* 使用 ``词云命令行`` 可执行文件::

    $ cat word.txt | 词云命令行

    $ 词云命令行 --text=words.txt --stopwords=stopwords.txt

* 使用 ``词云`` 模块::

    $ cat word.txt | python -m 词云

    $ python -m 词云 --text=words.txt --stopwords=stopwords.txt
"""

import sys

from .词云命令行 import main as 词云命令行主函数
from .词云命令行 import parse_args as 词云命令行参数解析


def main():
    """``词云命令行`` 的入口函数.

    此函数安装为脚本入口点.
    """
    词云命令行主函数(*词云命令行参数解析(sys.argv[1:]))


if __name__ == '__main__':  # pragma: no cover
    main()
