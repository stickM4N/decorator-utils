from dataclasses import dataclass
from inspect import Parameter, signature
from typing import Callable, List, NoReturn


@dataclass
class FunctionMetadata:
    """
    Class to store function metadata.

    :var name: Name of the wrapped function.
    :vartype name: str
    :var params: Parameters of the function.
    :vartype params: List[Parameter]
    :var returns: Parameters of the function. NoReturn type will be provided by default (not auto-generated).
    :vartype returns: Type[Any]
    """

    def __init__(self, function: Callable):
        if not isinstance(function, Callable):
            raise TypeError('FunctionMetadata must be inited with a Callable.')

        self.name = function.__name__
        self.params = list(signature(function).parameters.values())
        self.returns = type(NoReturn)

    def accepts_pos_params(self, params: List[str], explicit: bool = False) -> bool:
        """
        Checks if the function accepts positional parameters with `name`.

        :param params: List of the positional params names to check.
        :type params: List[str]
        :param explicit: Whether the function accepts positional named params explicitly or not.
        :type explicit: bool

        :returns: True if the function accepts the positional params, False otherwise.
        :rtype: bool
        """
        valid_params = (p.name for p in self.params
                        if p.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD))

        return set(params).issubset(valid_params) \
            or (not explicit and self.accepts_var_args())

    def accepts_kw_params(self, params: List[str], explicit: bool = False) -> bool:
        """
        Checks if the function accepts keyword parameters with `name`.

        :param params: List of the keyword params names to check.
        :type params: List[str]
        :param explicit: Whether the function accepts named keyword params explicitly or not.
        :type explicit: bool

        :returns: True if the function accepts the keyword params, False otherwise.
        :rtype: bool
        """
        valid_params = (p.name for p in self.params
                        if p.kind in (Parameter.KEYWORD_ONLY, Parameter.POSITIONAL_OR_KEYWORD))

        return set(params).issubset(valid_params) \
            or (not explicit and self.accepts_var_kwargs())

    def accepts_var_args(self) -> bool:
        """
        Checks if the function accepts `args` parameters.

        :returns: True if the function accepts `args` parameters.
        :rtype: bool
        """
        return any([p.kind == p.VAR_POSITIONAL for p in self.params])

    def accepts_var_kwargs(self) -> bool:
        """
        Checks if the function accepts `kwargs` parameters.

        :returns: True if the function accepts `kwargs` parameters.
        :rtype: bool
        """
        return any([p.kind == p.VAR_KEYWORD for p in self.params])
