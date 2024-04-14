decorator-utils
===============


Installation
------------

```shell
python3 -m pip install decorator-utils
```

Usage
-----

### Without context

```python
from random import randint

from decorator_utils import function_wrapper


@function_wrapper(pre_cb=lambda i: print(f'Calling with param {i}'),
                  post_cb=lambda r, i: print(f'Function call result `{r}` with param `{i}`'))
def random_int(increment):
    number = randint(0, 10)
    print(f'-> Generated number {number}')

    return number + increment


if __name__ == '__main__':
    n = randint(0, 10)

    random_int(n)
```

### With context

```python
from random import randint
from time import perf_counter_ns
from typing import final

from decorator_utils import DecoratorContext


class TraceCall(DecoratorContext):
    __time: int

    @final
    def pre_cb(self, *args, **kwargs) -> None:
        self.__time = perf_counter_ns()
        print(f'Starting function call with args `{args}` and kwargs `{kwargs}`.')

    @final
    def post_cb(self, result, *args, **kwargs) -> None:
        elapsed_time = (perf_counter_ns() - self.__time) / 1e+9
        print(f'Function took {elapsed_time} seconds to return value `{result}`.')


@TraceCall
def random_int(increment):
    number = randint(0, 10)
    print(f'-> Generated number {number}')

    return number + increment


if __name__ == '__main__':
    n = randint(0, 10)

    random_int(n)
```
