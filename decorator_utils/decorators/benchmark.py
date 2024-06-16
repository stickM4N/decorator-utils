from sys import stdout
from time import perf_counter_ns
from typing import final

from ..context import DecoratorContext
from ..metadata import FunctionMetadata


@final
class Benchmark(DecoratorContext):
    """
    Decorator to benchmark function execution. Logs function call time after it returns to the stream.

    :var __time: Function call start time.
    :vartype __time: int
    :var _format: Format of the string to print to `_stram`. First param is function name, second param is execution
        time in seconds with nanoseconds precision.
    :vartype _format: str
    :var _stram: Output stream. Defaults to stdout.
    :vartype _stram: SupportsWrite[str]
    """
    __time: int

    _format: str = 'Function `{}` execution took {:.6f} seconds to finish.'
    _stram = stdout

    def pre_cb(self, *args, **kwargs) -> None:
        self.__time = perf_counter_ns()

    def post_cb(self, *args, **kwargs) -> None:
        elapsed_time = (perf_counter_ns() - self.__time) / 1e+9
        function = FunctionMetadata(self._decorated_function).name

        print(self._format.format(function, elapsed_time), file=self._stram)
