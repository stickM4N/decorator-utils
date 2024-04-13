decorator-utils
===============


Installation
------------

```shell
python3 -m pip install decorator-utils
```

Usage
-----

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
