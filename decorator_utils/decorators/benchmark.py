from sys import stdout
from time import perf_counter_ns
from typing import final

from ..context import DecoratorContext
from ..metadata import FunctionMetadata


class Benchmark(DecoratorContext):
    __time: int
    ''' Function call start time. '''

    _format: str = 'Function `{}` execution took {:.6f} seconds to finish.'
    ''' Format of the string to print to `_file`. First param is function name, second param is execution time in
    seconds with nanoseconds precision. '''
    _file = stdout
    ''' Output stream of type SupportsWrite[str]. '''

    @final
    def pre_cb(self, *args, **kwargs) -> None:
        self.__time = perf_counter_ns()

    @final
    def post_cb(self, *args, **kwargs) -> None:
        elapsed_time = (perf_counter_ns() - self.__time) / 1e+9
        function = FunctionMetadata(self._decorated_function).name

        print(self._format.format(function, elapsed_time), file=self._file)
