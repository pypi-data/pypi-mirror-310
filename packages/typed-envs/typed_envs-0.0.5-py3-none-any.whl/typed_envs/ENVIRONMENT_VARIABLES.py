
from typed_envs.factory import EnvVarFactory

_factory = EnvVarFactory("TYPEDENVS")

SHUTUP = _factory.create_env("SHUTUP", bool, False, verbose=False)
