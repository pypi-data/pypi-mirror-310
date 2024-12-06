from typing import Callable

from naotool.deco.funtool import fun_filter

__all__ = ["tight"]


def tight(
    s1: list[str] | str,
    sep1: str = "\n",
    _sep1: str = "\n",
    sep2: str = " ",
    _sep2: str = " ",
    ext_func: Callable = lambda x: x,
) -> str:
    """去除大部分空白字符，自定义1、2级分隔符、拼接符，自定义过滤函数

    Args:
        s1 (list[str]): 原始str | list. 如果是str会被处理为 `s1 = s1.split(sep1)`.
        sep1 (str, optional): 1级别分隔符, 用于分隔原始字符串列表. Defaults to "\\n".
        _sep1 (str, optional): 1级别拼接符, 用于拼接原始字符串列表. Defaults to "\\n".
        sep2 (str, optional): 2级别分隔符, 用于分隔原始字符串。Defaults to " ".
        _sep2 (str, optional): 2级别拼接符, 用于拼接原始字符串。Defaults to " ".
        ext_func (Callable, optional): 自定义过滤函数。Defaults to `None`.

    Returns:
        str:
    """
    if isinstance(s1, str):
        s1 = s1.split(sep1)
    if isinstance(s1, list):
        return _sep1.join(
            _s2
            for s2 in s1
            if (
                _s2 := ext_func(
                    _sep2.join(
                        _s3 for s3 in s2.split(sep2) if (_s3 := ext_func(s3.strip()))
                    )
                )
            )
        )
    raise TypeError(s1, "only support type str, list[str]")


if __name__ == "__main__":
    s = """ 去除大部分 空     白    字        符，
    自定义1、2级分隔符
    自定义过滤函数 # foo #  666
    """
    s = tight(
        s,
        sep1="\n",
        _sep1=" ",
        sep2=" ",
        _sep2="",
        ext_func=fun_filter(func=lambda x: x not in "#foo"),
    )
    print(s)
