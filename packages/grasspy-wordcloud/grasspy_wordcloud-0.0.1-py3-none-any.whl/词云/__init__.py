导入 wordcloud
从 .词云命令行 导入 _颜色字典

# 匚无用词集 = wordcloud.STOPWORDS  # 一个集合

类 〇词云:
    """
    用于生成词云和绘图的词云对象.

    参数
    ---------
    字体路径 : 字符串
        要使用的字体路径 (OTF 或 TTF).
        对于 Linux 系统, 默认为 DroidSansMono.
        对于其他 OS, 你需要调整此路径.

    宽度 : 整型 (默认值=400)
        画布的宽度.

    高度 : 整型 (默认值=200)
        画布的高度.

    水平优先值 : 浮点数 (默认值=0.90)
        The ratio of times to try horizontal fitting as opposed to vertical.
        If prefer_horizontal < 1, the algorithm will try rotating the word
        if it doesn't fit. (There is currently no built-in way to get only
        vertical words.)

    蒙版 : nd-array 或空 (默认值=空)
        指定一个二进制蒙版以在上面绘制词语. 如果 '蒙版' 不是空,
        则将忽略 '宽度' 和 '高度', 并使用蒙版形状.
        All white (#FF or #FFFFFF) entries will be considerd
        "masked out" while other entries will be free to draw on. [This
        changed in the most recent version!]

    轮廓宽度: 浮点数 (默认值=0)
        如果蒙版非空且 '轮廓宽度' > 0, 则绘制蒙版轮廓.

    轮廓颜色: 颜色值 (默认值="黑色")
        蒙版轮廓颜色.

    比例 : 浮点数 (默认值=1)
        Scaling between computation and drawing. For large word-cloud images,
        using scale instead of larger canvas size is significantly faster, but
        might lead to a coarser fit for the words.

    最小字号 : 整型 (默认值=4)
        要使用的最小字号. 若剩余空间容纳不下此字号则停用.

    字号步进 : 整型 (默认值=1)
        字体字号的步进间隔. 字号步进 > 1 可加快计算, 但拟合会变差.

    最大词数 : 数字 (默认值=200)
        词语最大数量.

    无用词集 : 字符串集合或空
        将被剔除的词语. 使用 '从词频产生' 函数时会忽略此参数.

    背景颜色 : 颜色值 (默认值="black")
        词云图像的背景颜色.

    最大字号 : 整型或空 (默认值=空)
        最大词语的最大字号. 如果为空, 则使用图像的高度.

    模式 : 字符串 (默认值="RGB")
        若模式为 "RGBA" 且 '背景颜色' 为空, 将产生透明背景.

    相对比例 : 浮点数 (默认值='自动')
        Importance of relative word frequencies for font-size.  With
        relative_scaling=0, only word-ranks are considered.  With
        relative_scaling=1, a word that is twice as frequent will have twice
        the size.  If you want to consider the word frequencies and not only
        their rank, relative_scaling around .5 often looks good.
        If 'auto' it will be set to 0.5 unless repeat is true, in which
        case it will be set to 0.

        .. versionchanged: 2.0
            Default is now 'auto'.

    颜色函数 : 可调用对象, 默认值=空
        Callable with parameters word, font_size, position, orientation,
        font_path, random_state that returns a PIL color for each word.
        Overwrites "colormap".
        See colormap for specifying a matplotlib colormap instead.
        To create a word cloud with a single color, use
        ``color_func=lambda *args, **kwargs: "white"``.
        The single color can also be specified using RGB code. For example
        ``color_func=lambda *args, **kwargs: (255,0,0)`` sets color to red.

    正则表达式 : 字符串或空 (可选)
        Regular expression to split the input text into tokens in process_text.
        If None is specified, ``r"\w[\w']+"`` is used. Ignored if using
        generate_from_frequencies.

    搭配 : 布尔型, 默认值=True
        是否包括双词搭配. 若使用 '从词频产生' 则忽略此参数.

        .. versionadded: 2.0

    颜色映射 : 字符串或 matplotlib colormap, 默认值="viridis"
        Matplotlib colormap to randomly draw colors from for each word.
        Ignored if "color_func" is specified.

        .. versionadded: 2.0

    复数归一化 : 布尔型, 默认值=真
        Whether to remove trailing 's' from words. If True and a word
        appears with and without a trailing 's', the one with trailing 's'
        is removed and its counts are added to the version without
        trailing 's' -- unless the word ends with 'ss'. Ignored if using
        generate_from_frequencies.

    重复 : 布尔型, 默认值=假
        是否重复词语和短语, 直至达到 '最大词数' 或 '最小字号'.

    包括数字 : 布尔型, 默认值=假
        是否将数字算作短语.

    最小词长 : 整型, 默认值=0
        一个词语至少必须包含多少字符.

    搭配阈值: 整型, 默认值=30
        Bigrams must have a Dunning likelihood collocation score greater than this
        parameter to be counted as bigrams. Default of 30 is arbitrary.
    """
    套路 __初始化__(分身, 字体路径=空, 宽度=400, 高度=200, 边距=2, 水平优先值=.9,
                   蒙版=空, 比例=1, 颜色函数=空, 最大词数=200, 最小字号=4, 无用词集=空,
                   随机数状态=空, 背景颜色='黑色', 最大字号=空, 字号步进=1, 模式='RGB',
                   相对比例='自动', 正则表达式=空, 搭配=真, 颜色映射=空,
                   复数归一化=真, 轮廓宽度=0, 轮廓颜色='黑色', 重复=假, 
                   包括数字=假, 最小词长=0, 搭配阈值=30):
        背景颜色 = _颜色字典.获取(背景颜色, 背景颜色)
        轮廓颜色 = _颜色字典.获取(背景颜色, 轮廓颜色)
        如果 相对比例 == '自动': 相对比例 = 'auto'
        分身.__苦力 = wordcloud.WordCloud(font_path=字体路径, width=宽度, height=高度,
                      margin=边距, prefer_horizontal=水平优先值, mask=蒙版, scale=比例,
                      color_func=颜色函数, max_words=最大词数, min_font_size=最小字号,
                      stopwords=无用词集, random_state=随机数状态, background_color=背景颜色,
                      max_font_size=最大字号, font_step=字号步进, mode=模式,
                      relative_scaling=相对比例, regexp=正则表达式, collocations=搭配,
                      colormap=颜色映射, normalize_plurals=复数归一化, contour_width=轮廓宽度,
                      contour_color=轮廓颜色, repeat=重复, include_numbers=包括数字,
                      min_word_length=最小词长, collocation_threshold=搭配阈值)

    套路 产生(分身, 文本):
        """从 '文本' 产生词云.

        '文本' 应为自然文本. 如果传入的是排序好的词语列表, 词语将在输出中出现两次.
        要消除这种重复, 请设置 ``搭配=假``.
        """
        返回 分身.__苦力.generate(文本)

    套路 从词频产生(分身, 词频字典, 最大字号=空):
        """根据词语及其频率创建词云.

        '词频字典' : 以词语(字符串)和频率(浮点数)为键值对的字典
        """
        返回 分身.__苦力.generate_from_frequencies(词频字典, max_font_size=最大字号)

    套路 改色(分身, 随机数状态=空, 颜色函数=空, 颜色映射=空):
        """给现有布局重新着色.

        应用新颜色比生成整个词云要快得多.
        """
        返回 分身.__苦力.recolor(random_state=随机数状态, color_func=颜色函数,
                                colormap=颜色映射)

    套路 转为文件(分身, 文件名):
        """
        导出到图像文件
        """
        返回 分身.__苦力.to_file(文件名)

    套路 转为数组(分身):
        """转为 nunpy 数组.
        """
        返回 分身.__苦力.to_array()

    套路 转为html(分身):
        返回 分身.__苦力.to_html()

    套路 转为svg(分身, 嵌入字体=假, 优化嵌入字体=真, 嵌入图像=假):
        """
        导出为 SVG
        """
        返回 分身.__苦力.to_svg(embed_font=嵌入字体,
                        optimize_embedded_font=优化嵌入字体,
                        embed_image=嵌入图像)        

