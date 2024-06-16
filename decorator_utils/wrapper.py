from __future__ import annotations

from functools import wraps
from typing import Any, Callable, NoReturn, Tuple

from .metadata import FunctionMetadata


def function_wrapper(pre_cb: Callable = None, post_cb: Callable = None, *,
                     use_result: bool = True, force_args: bool = True, forward_metadata: bool = False,
                     return_metadata: bool = False) -> Callable[[...], Any | Tuple[Any, FunctionMetadata]]:
    """
    Decorator to wrap a function and execute callbacks before and after its execution.
    Both callback functions take the wrapped function parameters plus a `FunctionMetadata` object instance as
    `_func_metadata` kwarg if the function accepts them.

    Callback function will not get `args` or `kwargs` if they are not accepted unless they are forced and will check if
    they are accepted using their names.

    :param pre_cb: Callback to execute before the wrapped function.
    :type pre_cb: Callable
    :param post_cb: Callback to execute after the wrapped function.
    :type post_cb: Callable
    :param use_result: Whether to pass decorated function result to `post_func` as first arg.
    :type use_result: bool
    :param force_args: Whether to force `args` or `kwargs` to be passed tho callback functions.
    :type force_args: bool
    :param forward_metadata: Whether to add `_func_metadata` to `kwargs`.
    :type forward_metadata: bool
    :param return_metadata: Whether to also return `_func_metadata` as result in a tuple (`result`, `metadata`).
    :type return_metadata: bool

    :returns: The wrapped function return value.
    :rtype: Callable[[...], Any | Tuple[Any, FunctionMetadata]]
    """

    def __decorator(decorated_function) -> Callable[[...], Any | Tuple[Any, FunctionMetadata]]:
        def __exec_callback(function: Callable, *args, insert_result: Any = NoReturn, **kwargs) -> Any:
            """
            Utility to call functions and handle their supported `args` and `kwargs`.

            :param function: Callback function.
            :type function: Callable
            :param insert_result: Pass this value as first arg to the function if provided.
            :type insert_result: Any

            :returns: The wrapped function return value.
            :rtype: Any | Tuple[Any, ...]
            """

            if not force_args:
                metadata = FunctionMetadata(function)

                if metadata.accepts_pos_params(['self'], explicit=True):  # Handle class method self instance
                    args = [args[0], *[a for a in args[1:] if metadata.accepts_pos_params([a])]]
                else:
                    args = [a for a in args if metadata.accepts_pos_params([a])]

                kwargs = {p: v for p, v in kwargs.items() if metadata.accepts_kw_params([p])}

            if insert_result is not NoReturn:  # Pass result as first arg if provided
                if isinstance(args, tuple):
                    args = list(args)
                args.insert(0, insert_result)

            return function(*args, **kwargs)

        @wraps(decorated_function)
        def __wrapper(*args, **kwargs) -> Any | Tuple[Any, FunctionMetadata]:
            metadata = FunctionMetadata(decorated_function)

            if forward_metadata:
                kwargs['_func_metadata'] = metadata

            if pre_cb is not None:
                __exec_callback(pre_cb, *args, **kwargs)

            result = __exec_callback(decorated_function, *args, **kwargs)

            metadata.returns = type(result)

            if post_cb is not None:
                __exec_callback(post_cb, *args, insert_result=result if use_result else NoReturn, **kwargs)

            return (result, metadata) if return_metadata else result

        return __wrapper

    return __decorator
