# -*- coding: utf-8 -*-
"""生成词云的命令行接口.
"""
from __future__ import absolute_import

import sys
import textwrap

if __name__ == '__main__':  # pragma: no cover
    sys.exit(textwrap.dedent(
        """
        要执行词云命令行, 请考虑运行:

          词云命令行 --help

        or

          python -m 词云 --help
        """))

import io
import re
import argparse
import wordcloud as wc
import numpy as np
from PIL import Image

__version__ = '1.8.1'

_颜色字典 = {
    '爱丽丝蓝': 'aliceblue',
    '古董白': 'antiquewhite',
    '湖绿': 'aqua',
    '碧绿': 'aquamarine',
    '青白色': 'azure',
    '米色': 'beige',
    '陶坯黄': 'bisque',
    '黑色': 'black',
    '杏仁白': 'blanchedalmond',
    '蓝色': 'blue',
    '蓝紫色': 'blueviolet',
    '褐色': 'brown',
    '硬木褐': 'burlywood',
    '军服蓝': 'cadetblue',
    '查特酒绿': 'chartreuse',
    '巧克力色': 'chocolate',
    '珊瑚红': 'coral',
    '矢车菊蓝': 'cornflowerblue',
    '玉米穗黄': 'cornsilk',
    '绯红': 'crimson',
    '青色': 'cyan',
    '深蓝': 'darkblue',
    '深青': 'darkcyan',
    '深金菊黄': 'darkgoldenrod',
    '暗灰': 'darkgray',
    '深绿': 'darkgreen',
    '深卡其色': 'darkkhaki',
    '深品红': 'darkmagenta',
    '深橄榄绿': 'darkolivegreen',
    '深橙': 'darkorange',
    '深洋兰紫': 'darkorchid',
    '深红': 'darkred',
    '深鲑红': 'darksalmon',
    '深海藻绿': 'darkseagreen',
    '深岩蓝': 'darkslateblue',
    '深岩灰': 'darkslategray',
    '深松石绿': 'darkturquoise',
    '深紫': 'darkviolet',
    '深粉': 'deeppink',
    '深天蓝': 'deepskyblue',
    '昏灰': 'dimgray',
    '道奇蓝': 'dodgerblue',
    '火砖红': 'firebrick',
    '花卉白': 'floralwhite',
    '森林绿': 'forestgreen',
    '紫红': 'fuchsia',
    '庚氏灰': 'gainsboro',
    '幽灵白': 'ghostwhite',
    '金色': 'gold',
    '金菊黄': 'goldenrod',
    '灰色': 'gray',
    '调和绿': 'green',
    '黄绿色': 'greenyellow',
    '蜜瓜绿': 'honeydew',
    '艳粉': 'hotpink',
    '印度红': 'indianred',
    '靛蓝': 'indigo',
    '象牙白': 'ivory',
    '卡其色': 'khaki',
    '薰衣草紫': 'lavender',
    '薰衣草红': 'lavenderblush',
    '草坪绿': 'lawngreen',
    '柠檬绸黄': 'lemonchiffon',
    '浅蓝': 'lightblue',
    '浅珊瑚红': 'lightcoral',
    '浅青': 'lightcyan',
    '浅金菊黄': 'lightgoldenrodyellow',
    '浅金菊黄': 'lightgoldenrod',
    '亮灰': 'lightgray',
    '浅绿': 'lightgreen',
    '浅粉': 'lightpink',
    '浅鲑红': 'lightsalmon',
    '浅海藻绿': 'lightseagreen',
    '浅天蓝': 'lightskyblue',
    '浅岩灰': 'lightslategray',
    '浅钢青': 'lightsteelblue',
    '浅黄': 'lightyellow',
    '绿色': 'lime',
    '青柠绿': 'limegreen',
    '亚麻色': 'linen',
    '洋红': 'magenta',
    '栗色': 'maroon',
    '中碧绿': 'mediumaquamarine',
    '中蓝': 'mediumblue',
    '中洋兰紫': 'mediumorchid',
    '中紫': 'mediumpurple',
    '中海藻绿': 'mediumseagreen',
    '中岩蓝': 'mediumslateblue',
    '中嫩绿': 'mediumspringgreen',
    '中松石绿': 'mediumturquoise',
    '中紫红': 'mediumvioletred',
    '午夜蓝': 'midnightblue',
    '薄荷乳白': 'mintcream',
    '雾玫瑰红': 'mistyrose',
    '鹿皮色': 'moccasin',
    '土著白': 'navajowhite',
    '藏青': 'navy',
    '旧蕾丝白': 'oldlace',
    '橄榄色': 'olive',
    '橄榄绿': 'olivedrab',
    '橙色': 'orange',
    '橘红': 'orangered',
    '洋兰紫': 'orchid',
    '白金菊黄': 'palegoldenrod',
    '白绿色': 'palegreen',
    '白松石绿': 'paleturquoise',
    '白紫红': 'palevioletred',
    '番木瓜橙': 'papayawhip',
    '粉扑桃色': 'peachpuff',
    '秘鲁红': 'peru',
    '粉色': 'pink',
    '李紫': 'plum',
    '粉末蓝': 'powderblue',
    '紫色': 'purple',
    '红色': 'red',
    '瑞贝卡紫': 'rebeccapurple',
    '玫瑰褐': 'rosybrown',
    '品蓝': 'royalblue',
    '鞍褐': 'saddlebrown',
    '鲑红': 'salmon',
    '沙褐': 'sandybrown',
    '海藻绿': 'seagreen',
    '贝壳白': 'seashell',
    '土黄赭': 'sienna',
    '银色': 'silver',
    '天蓝': 'skyblue',
    '岩蓝': 'slateblue',
    '岩灰': 'slategray',
    '雪白': 'snow',
    '春绿': 'springgreen',
    '钢青': 'steelblue',
    '日晒褐': 'tan',
    '鸭翅绿': 'teal',
    '蓟紫': 'thistle',
    '番茄红': 'tomato',
    '松石绿': 'turquoise',
    '紫罗兰色': 'violet',
    '麦色': 'wheat',
    '白色': 'white',
    '烟雾白': 'whitesmoke',
    '黄色': 'yellow',
    '暗黄绿色': 'yellowgreen',
}

class FileType(object):
    """Factory for creating file object types.

    Port from argparse so we can support unicode file reading in Python2

    Instances of FileType are typically passed as type= arguments to the
    ArgumentParser add_argument() method.

    Keyword Arguments:
        - mode -- A string indicating how the file is to be opened. Accepts the
            same values as the builtin open() function.
        - bufsize -- The file's desired buffer size. Accepts the same values as
            the builtin open() function.

    """

    def __init__(self, mode='r', bufsize=-1):
        self._mode = mode
        self._bufsize = bufsize

    def __call__(self, string):
        # the special argument "-" means sys.std{in,out}
        if string == '-':
            if 'r' in self._mode:
                return sys.stdin
            elif 'w' in self._mode:
                return sys.stdout.buffer if 'b' in self._mode else sys.stdout
            else:
                msg = 'argument "-" with mode %r' % self._mode
                raise ValueError(msg)

        # all other arguments are used as file names
        try:
            encoding = None if 'b' in self._mode else "UTF-8"
            return io.open(string, self._mode, self._bufsize, encoding=encoding)
        except IOError as e:
            message = "无法打开 '%s': %s"
            raise argparse.ArgumentTypeError(message % (string, e))

    def __repr__(self):
        args = self._mode, self._bufsize
        args_str = ', '.join(repr(arg) for arg in args if arg != -1)
        return '%s(%s)' % (type(self).__name__, args_str)


class RegExpAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(RegExpAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            re.compile(values)
        except re.error as e:
            raise argparse.ArgumentError(self, 'Invalid regular expression: ' + str(e))
        setattr(namespace, self.dest, values)


def main(args, text, imagefile):
    wordcloud = wc.WordCloud(**args)
    wordcloud.generate(text)
    image = wordcloud.to_image()

    with imagefile:
        image.save(imagefile, format='png', optimize=True)


def make_parser():
    description = '词云模块的简单命令行接口.'
    parser = argparse.ArgumentParser(usage="%s -m 词云 [选项]" % sys.executable,
                description=description, epilog="若未指定文本文件, 则使用标准输入(STDIN).")
    parser.add_argument(
        '--文本文件', metavar='file', type=FileType(), default='-',
        help='指定用来构建词云的词语文件, 默认为标准输入(stdin)')
    parser.add_argument(
        '--正则表达式', metavar='regexp', default=None, action=RegExpAction, dest='regexp',
        help='覆盖默认的定义词语构成的正则表达式')
    parser.add_argument(
        '--无用词集文件', metavar='file', type=FileType(), dest='stopwords',
        help='指定无用词集文件, 每行一个词语,'
             ' 解析后的文本会删除这些词语')
    parser.add_argument(
        '--图像文件', metavar='file', type=FileType('wb'),
        default='-',
        help='生成的 PNG 图像应写入的文件名称,'
             ' 默认为标准输出(stdout)')
    parser.add_argument(
        '--字体文件', metavar='path', dest='font_path',
        help='要使用的字体文件路径 (默认为 DroidSansMono)')
    parser.add_argument(
        '--蒙版', metavar='file', type=argparse.FileType('rb'), dest='mask',
        help='图像蒙版')
    parser.add_argument(
        '--颜色蒙版', metavar='file', type=argparse.FileType('rb'),
        dest='colormask',
        help='用于图像着色的颜色蒙版')
    parser.add_argument(
        '--轮廓宽度', metavar='width', default=0, type=float,
        dest='contour_width',
        help='若大于 0, 则绘制蒙版轮廓 (默认值: 0)')
    parser.add_argument(
        '--轮廓颜色', metavar='color', default='黑色', type=str,
        dest='contour_color',
        help='使用给定颜色作为蒙版轮廓颜色 -'
             ' 接受 PIL.ImageColor.getcolor 中的任何值')
    parser.add_argument(
        '--相对比例', type=float, default=0, dest='relative_scaling',
        metavar='rs', help=' 按词频缩放词语的比例 (0 - 1)')
    parser.add_argument(
        '--边距', type=int, default=2, dest='margin',
        metavar='width', help='词语周围的边距')
    parser.add_argument(
        '--宽度', type=int, default=400, dest='width',
        metavar='width', help='定义输出图像的宽度')
    parser.add_argument(
        '--高度', type=int, default=200, dest='height',
        metavar='height', help='定义输出图像的高度')
    parser.add_argument(
        '--颜色', metavar='color', dest='color',
        help='使用给定颜色给图像着色 -'
             ' 接受 PIL.ImageColor.getcolor 中的任何值')
    parser.add_argument(
        '--背景颜色', metavar='color', default='黑色', type=str,
        dest='background_color',
        help='使用指定颜色作为图像的背景颜色 -'
             ' 接受 PIL.ImageColor.getcolor 中的任何值')
    parser.add_argument(
        '--no_collocations', action='store_false', dest='collocations',
        help='do not add collocations (bigrams) to word cloud '
             '(default: add unigrams and bigrams)')
    parser.add_argument(
        '--包括数字',
        action='store_true',
        dest='include_numbers',
        help='词云中是否包括数字?')
    parser.add_argument(
        '--最小词长',
        type=int,
        default=0,
        metavar='min_word_length',
        dest='min_word_length',
        help='所包含的词语至少必须有多少字符')
    parser.add_argument(
        '--水平优先值',
        type=float, default=.9, metavar='ratio', dest='prefer_horizontal',
        help='水平放置相对于垂直放置的比例')
    parser.add_argument(
        '--比例',
        type=float, default=1, metavar='scale', dest='scale',
        help='scaling between computation and drawing')
    parser.add_argument(
        '--颜色映射',
        type=str, default='viridis', metavar='map', dest='colormap',
        help='matplotlib 颜色映射名称')
    parser.add_argument(
        '--模式',
        type=str, default='RGB', metavar='mode', dest='mode',
        help='使用 RGB, 或对透明背景使用 RGBA')
    parser.add_argument(
        '--最大词数',
        type=int, default=200, metavar='N', dest='max_words',
        help='词语最大数量')
    parser.add_argument(
        '--最小字号',
        type=int, default=4, metavar='size', dest='min_font_size',
        help='要使用的最小字号')
    parser.add_argument(
        '--最大字号',
        type=int, default=None, metavar='size', dest='max_font_size',
        help='最大词语的最大字号')
    parser.add_argument(
        '--字号步进',
        type=int, default=1, metavar='step', dest='font_step',
        help='字号的步进间隔')
    parser.add_argument(
        '--随机数状态',
        type=int, default=None, metavar='seed', dest='random_state',
        help='随机数种子')
    parser.add_argument(
        '--复数不归一化',
        action='store_false',
        dest='normalize_plurals',
        help='是否移除词语的复数后缀 \'s\'')
    parser.add_argument(
        '--重复',
        action='store_true',
        dest='repeat',
        help='是否重复词语和短语')
    parser.add_argument(
        '--版本', action='version',
        version='%(prog)s {version}'.format(version=__version__))
    return parser


def parse_args(arguments):
    # prog = 'python wordcloud_cli.py'
    parser = make_parser()
    args = parser.parse_args(arguments)

    if args.colormask and args.color:
        raise ValueError('只能指定颜色蒙版和颜色函数中的一个')

    args = vars(args)

    with args.pop('文本文件') as f:
        text = f.read()

    if clr := args['color']:
        args['color'] = _颜色字典.获取(clr, clr)
    
    if clr := args['contour_color']:
        args['contour_color'] = _颜色字典.获取(clr, clr)
    
    if clr := args['background_color']:
        args['background_color'] = _颜色字典.获取(clr, clr)

    if args['stopwords']:
        with args.pop('stopwords') as f:
            args['stopwords'] = set(map(lambda l: l.strip(), f.readlines()))

    if args['mask']:
        mask = args.pop('mask')
        args['mask'] = np.array(Image.open(mask))

    color_func = wc.random_color_func
    colormask = args.pop('colormask')
    color = args.pop('color')
    if colormask:
        image = np.array(Image.open(colormask))
        color_func = wc.ImageColorGenerator(image)
    if color:
        color_func = wc.get_single_color_func(color)
    args['color_func'] = color_func

    imagefile = args.pop('图像文件')

    return args, text, imagefile
