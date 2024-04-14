from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Tuple, final

from .metadata import FunctionMetadata
from .wrapper import function_wrapper


class DecoratorContext(ABC):
    """
    Decorator class that provides an interface to implement a decorator with the ability to retain data between
    `pre_cb` and `post_cb` callbacks. It works with `function_wrapper` in the back and its parameters are matched
    against this class attributes.
    """
    _use_result: bool = True
    ''' Whether to pass decorated function result to `post_func` as first arg. '''
    _force_args: bool = True
    ''' Whether to force `args` or `kwargs` to be passed tho callback functions. '''
    _forward_metadata: bool = False
    ''' Whether to add `_func_metadata` to `kwargs`. '''
    _return_metadata: bool = False
    ''' Whether to also return `_func_metadata` as result in a tuple (`result`, `metadata`). '''

    @final
    def __init__(self, func: Callable):
        self._decorated_function = func

    @final
    def __call__(self, *args, **kwargs) -> Any | Tuple[Any, FunctionMetadata]:
        decorator = function_wrapper(self.pre_cb, self.post_cb,
                                     use_result=self._use_result, force_args=self._force_args,
                                     forward_metadata=self._forward_metadata, return_metadata=self._return_metadata)
        callback = decorator(self._decorated_function)

        return callback(*args, **kwargs)

    @abstractmethod
    def pre_cb(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def post_cb(self, *args, **kwargs) -> None:
        raise NotImplementedError
