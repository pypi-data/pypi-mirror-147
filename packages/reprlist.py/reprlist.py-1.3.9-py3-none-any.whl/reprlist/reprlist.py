from . import tools


class Reprlist:
    """

    """

    def __init__(self, extend="", /, file_start=None, file_end=None, file_max_width=None, file_max_lines=None,
                 repr_start=None, repr_end=None, repr_max_width=None, repr_max_lines=None,
                 str_start=None, str_end=None, str_max_width=None, str_max_lines=None,
                 format_start=None, format_end=None, format_max_width=None, format_max_lines=None):
        """

        """
        # load configs
        cfg = tools.get_global_config()
        settings = ["file_start", "file_end", "file_max_width", "file_max_lines",
                    "repr_start", "repr_end", "repr_max_width", "repr_max_lines",
                    "str_start", "str_end", "str_max_width", "str_max_lines",
                    "format_start", "format_end", "format_max_width", "format_max_lines"]
        for setting in settings:
            key, sub = setting.split("_", 1)
            g_cfg = cfg[key][sub.replace("_", " ")]
            l_cfg = locals()[setting]
            if l_cfg is None:
                setattr(self, setting, g_cfg)
            else:
                setattr(self, setting, l_cfg)

        # init
        self.main = []

        if extend:
            self.extend(extend)

    def extend(self, iterable, /, alignment_index_self=None, alignment_index_iter=None):
        """延长自身。
        iterable : 可迭代对象
        alignment_index_self: 自身与被对接者的
        """

