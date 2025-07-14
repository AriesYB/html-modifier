import jsbeautifier
from lxml import etree
from lxml.html import html5parser


class HtmlModifierService:
    _cache = {}  # 新增缓存字典

    @staticmethod
    def save_html(html_str, key) -> str:
        """
        暂存 HTML 内容
        :param html_str: 待存储的 HTML 字符串
        :param key: 用于后续查询的键
        :return: 返回用于查询的键
        """
        HtmlModifierService._cache[key] = html_str
        return key

    @staticmethod
    def get_html(key):
        """
        查询暂存的 HTML 内容
        :param key: 查询键
        :return: 对应的 HTML 字符串（若不存在则返回 None）
        """
        return HtmlModifierService._cache.get(key)

    @staticmethod
    def has_key(key):
        """
        检查缓存中是否存在指定键
        :param key: 需要检查的键
        :return: 布尔值，表示键是否存在
        """
        return key in HtmlModifierService._cache

    @staticmethod
    def apply_modifications_by_key(key, modifications):
        if not HtmlModifierService.has_key(key):
            return "未找到key对应的html"
        HtmlModifierService.save_html(
            HtmlModifierService.apply_modifications(HtmlModifierService.get_html(key), modifications), key)
        return "修改成功"


@staticmethod
def apply_modifications(html_content, modifications):
    """
    应用修改点到 HTML 内容，支持 XPath 和行号两种方式
    :param html_content: 原始 HTML 字符串
    :param modifications: 修改点列表，JSON数组
    :return: 修改后的 HTML 字符串
    """
    # 初始化行偏移量
    line_offset = 0
    lines = html_content.split('\n')

    tree = html5parser.fromstring(html_content)

    for mod in modifications:
        try:
            if 'xpath' in mod:
                # 使用 XPath 定位节点
                nodes = tree.xpath(mod['xpath'])

                if not nodes:
                    print(f"未找到节点: {mod.get('description', '')} (XPath: {mod['xpath']})")
                    continue

                # 解析新 HTML 片段
                new_content = mod['new_html']

                # 处理多个匹配节点
                for node in nodes:
                    # 创建新节点
                    if new_content.strip().startswith('<') and new_content.strip().endswith('>'):
                        if new_content.startswith("<script>"):
                            new_node = html5parser.fragment_fromstring(new_content, create_parent='')
                            node.getparent().replace(node, new_node)
                        else:
                            # 完整的 HTML 元素
                            new_node = html5parser.fragment_fromstring(new_content, create_parent='div')
                            node.getparent().replace(node, new_node)
                    else:
                        # 文本内容
                        node.text = new_content

                    print(f"修改成功 (XPath): {mod.get('description', '')}")

            elif 'line_range' in mod:
                start, end = mod['line_range']
                adjusted_start = start + line_offset
                adjusted_end = end + line_offset

                new_lines = mod['new_html'].split('\n')

                # 计算行数变化
                delta = len(new_lines) - (adjusted_end - adjusted_start + 1)
                line_offset += delta

                if 1 <= adjusted_start <= len(lines) and 1 <= adjusted_end <= len(
                        lines) and adjusted_start <= adjusted_end:
                    lines[adjusted_start - 1:adjusted_end] = new_lines
                    print(f"行修改成功: {start}-{end}行")
                else:
                    print(f"无效行范围: {adjusted_start}-{adjusted_end}")

            else:
                print(f"未知修改类型: {mod}")

        except Exception as e:
            print(f"修改失败: {mod.get('description', '')} - {str(e)}")

    # 若有 DOM 节点操作后需重新格式化脚本
    for script in tree.xpath('//script'):
        if script.text and script.get('type') in [None, 'script', 'text/javascript']:
            opts = jsbeautifier.default_options()
            opts.indent_size = 4
            opts.brace_style = "expand"
            opts.preserve_newlines = True
            script.text = jsbeautifier.beautify(script.text, opts)

    result_tree = html5parser.fromstring('\n'.join(lines))
    result = etree.tostring(result_tree, encoding='unicode', method='html', pretty_print=True)
    result = result.replace('U00040', '@').replace('U0003A', ':').replace('=""', "")

    return result

    @staticmethod
    def export_html(key, file_path):
        """
        将缓存中的 HTML 内容导出到文件
        :param key: 缓存键
        :param file_path: 目标文件路径
        :return: 成功返回 True，失败返回 False
        """
        html_content = HtmlModifierService.get_html(key)
        if html_content is None:
            raise Exception(f"缓存中未找到 key: {key}")
            return False

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML 已成功导出至: {file_path}")
        return True
