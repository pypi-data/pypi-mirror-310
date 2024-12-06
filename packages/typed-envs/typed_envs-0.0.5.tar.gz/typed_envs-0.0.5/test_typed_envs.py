
import asyncio

import pytest

from typed_envs import EnvironmentVariable, create_env


def test_int_env():
    env = create_env("TEST", int, 10)
    assert isinstance(env, int)
    assert isinstance(env, EnvironmentVariable)
    env + 10
    env - 10
    env * 10
    env / 10

def test_str_env():
    env = create_env("TEST", str, 10)
    assert isinstance(env, str)
    assert isinstance(env, EnvironmentVariable)
    env.upper()
    env.lower()
    with pytest.raises(TypeError):
        env + 10

def test_complex_env():
    env = create_env("TEST", asyncio.Semaphore, default=10, string_converter=int)
    assert isinstance(env, asyncio.Semaphore)
    assert isinstance(env, EnvironmentVariable)
    assert hasattr(env, 'acquire')
    assert hasattr(env, 'release')

def test_bool_conversion():
    env = create_env("TEST", bool, default='test')
    # You can't subclass a bool so its the only type that breaks our type checking
    with pytest.raises(AssertionError):
        assert isinstance(env, bool)
    assert isinstance(env, int)