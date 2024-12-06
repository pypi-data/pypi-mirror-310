from collections.abc import Callable
from functools import wraps

__all__ = [
    "decodeco",
]


def decodeco(
    func_deco: Callable[..., Callable] = None,
    arg_func_name: str = "func",
    func_args_name: str = "func_args",
    func_kwargs_name: str = "func_kwargs",
) -> Callable[..., Callable]:
    """
    装饰器代理，在装饰器前后做一些通用处理:
        1. 让装饰器可以带括号或者不带括号调用
        2. 让装饰器可以只写内部逻辑不需要关注任何其他事情
    因此，装饰器只需要做一件事：接收函数，给函数增加功能就够了

    Args:
        func_deco (Callable[..., Callable]): 装饰器.
        arg_func_name (str): 装饰器中, 被装饰函数的形式参数的命名
        func_args_name (str): 装饰器中, 用于接收实际函数位置参数 `args` 的命名
        func_kwargs_name (str): 装饰器中, 用于接收实际函数kw参数 `kwargs` 的命名

    Returns:
        Callable[..., Callable]: _description_
    """
    if not func_deco:
        return lambda f: decodeco(func_deco=f)

    @wraps(func_deco)
    def wrapwrap(*deco_args, **deco_kwargs):
        if deco_args and isinstance(deco_args[0], Callable):  # 如果第一个参数是可调用的
            func = deco_args[0]
        if (f := deco_kwargs.get(arg_func_name)) and isinstance(
            f, Callable
        ):  # kwargs中 func=xxx 优先级更高
            func = f
        if not func:
            return lambda f: func_deco(f, *deco_args, **deco_kwargs)

        # func就是真正要包装的函数了，这里我们不执行他，而是执行装饰器函数

        @wraps(func)
        def wrap(*func_args, **func_kwargs):
            # 给装饰器注入函数参数
            deco_kwargs[func_args_name] = func_args
            deco_kwargs[func_kwargs_name] = func_kwargs
            return func_deco(*deco_args, **deco_kwargs)

        return wrap

    return wrapwrap


if __name__ == "__main__":
    # 示例用法
    @decodeco(arg_func_name="func")
    def deco_exp(func: Callable, func_args, func_kwargs) -> Callable:
        print("before the real function")
        res = func(*func_args, **func_kwargs)
        print("after the real function")
        return res

    @deco_exp
    def test(a, b=2):
        print("test")
        print(f"a={a}")
        print(f"b={b}")

    test(6)
