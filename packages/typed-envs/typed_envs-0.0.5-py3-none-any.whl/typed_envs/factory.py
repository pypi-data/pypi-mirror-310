
import logging
import os
from functools import lru_cache
from contextlib import suppress
from types import new_class
from typing import Any, Callable, Optional, Type, TypeVar

from typed_envs import registry
from typed_envs._env_var import EnvironmentVariable

T = TypeVar('T')

class EnvVarFactory:
    def __init__(self, env_var_prefix: Optional[str] = None) -> None:
        self.prefix = env_var_prefix
    def create_env(
        self,
        env_var_name: Optional[str], 
        env_var_type: Type[T], 
        default: Any,
        *init_args, 
        string_converter: Optional[Callable[[str], Any]] = None, 
        verbose: bool = True,
        **init_kwargs
    ) -> "EnvironmentVariable[T]":
        """
        Returns a new EnvironmentVariable object with the prefix defined on the `EnvVarFactory`.

        function args:
        typ: blah blah 
        default: blah blah
        *init_args: blah blah
        string_converter: some more words
        verbose: words
        **init_kwargs: words
        
        Functionally, `EnvironmentVariable` objects will work exactly the same as any instance of specified `typ`.

        In the example below, `some_var` can be used just like as any other `int` object.
        
        ```
        import typed_envs
        some_var = typed_envs.create_env("SET_WITH_THIS_ENV", int, 10)

        >>> isinstance(some_var, int)
        True
        >>> isinstance(some_var, EnviromentVariable)
        True
        ```
        There are only 2 differences between `some_var` and `int(10)`:
        - `some_var` will properly type check as an instance of both `int` and `EnvironmentVariable`
        - `some_var.__repr__()` will include contextual information about the `EnvironmentVariable`.
        
        ```
        >>> some_var
        <EnvironmentVariable[name=`SET_WITH_THIS_ENV`, type=int, default_value=10, current_value=10, using_default=True]>
        >>> str(some_var)
        "10"
        >>> some_var + 5
        15
        >>> 20 / some_var
        2
        ```
        """
        if self.prefix:
            env_var_name = f"{self.prefix}_{env_var_name}"
        var_value = os.environ.get(env_var_name)
        using_default = var_value is None
        var_value = var_value or default
        if env_var_type is bool:
            var_value = bool(var_value)
        if any(iter_typ in env_var_type.__bases__ for iter_typ in [list, tuple, set]):
            var_value = var_value.split(',')
        if string_converter and not (using_default and isinstance(default, env_var_type)):
            var_value = string_converter(var_value)

        subclass = _create_subclass(env_var_type)
        instance = subclass(var_value, *init_args, **init_kwargs)
        # Set additional attributes
        instance._init_arg0 = var_value
        instance._env_name = env_var_name
        instance._default_value = default
        instance._using_default = using_default
        try:
            instance.name = env_var_name
        except AttributeError:
            # NOTE all the private attrs need to be set before this log msg, just in case it gets used
            logger.warning(f'{str(instance)} already has a name attribute defined. value can always be accessed with `instance._env_name`')

        # Finish up
        if verbose:
            # This code prints envs on script startup for convenience of your users.
            try:
                logger.info(instance.__repr__())
            except RecursionError:
                logger.debug(f"unable to properly display your `{env_var_name}` {instance.__class__.__base__} env due to RecursionError")
                with suppress(RecursionError):
                    logger.debug(f"Here is your `{env_var_name}` env in string form: {str(instance)}")
        _register_new_env(env_var_name, instance)
        return instance

@lru_cache(maxsize=None)
def _create_subclass(typ: Type[T]) -> Type["EnvironmentVariable[T]"]:
    """
    Returns a mixed subclass of `typ` and `EnvironmentVariable` that does 2 things:
     - modifies the __repr__ method so its clear an object's value was set with an env var while when inspecting variables
     - ensures the instance will type check as an EnvironmentVariable object without losing information about its actual type

    Aside from these two things, subclass instances will function exactly the same as any other instance of `typ`.
    """
    subclass_name = f'EnvironmentVariable_{typ.__name__}'
    # You can't subclass a boolean but its just an int anyway
    subclass_bases = (int if typ is bool else typ, EnvironmentVariable[typ])
    cls = new_class(subclass_name, subclass_bases, {})
    cls.__repr__ = EnvironmentVariable.__repr__
    cls.__str__ = EnvironmentVariable.__str__
    cls._base_type = typ
    return cls

def _register_new_env(name: str, instance: EnvironmentVariable) -> None:
    registry.ENVIRONMENT[name] = instance
    if instance._using_default:
        registry._ENVIRONMENT_VARIABLES_USING_DEFAULTS[name] = instance
    else:
        registry._ENVIRONMENT_VARIABLES_SET_BY_USER[name] = instance

# NOTE: While we create the TYPEDENVS_SHUTUP object in the ENVIRONMENT_VARIABLES file as an example,
#       we cannot use it here without creating a circular import.

logger = logging.getLogger('typed_envs')

from typed_envs import ENVIRONMENT_VARIABLES
if ENVIRONMENT_VARIABLES.SHUTUP:
    logger.disabled = True
else:
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

default_factory = EnvVarFactory()
