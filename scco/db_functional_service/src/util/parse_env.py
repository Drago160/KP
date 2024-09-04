import os


def _init_config() -> dict[str, str]:
    # service_dir = os.path.dirname(os.path.dirname(
    #     os.path.dirname(os.path.realpath(__file__))
    # ))
    # path_to_local_venv = os.path.realpath(f"{service_dir}/.env")
    # path_to_local_secrets_venv = os.path.realpath(
    #     f"{service_dir}/.env.secret.postgres"
    # )

    res = {
        # **dotenv_values(path_to_local_venv),
        # **dotenv_values(path_to_local_secrets_venv),
        **os.environ,
    }

    return res


class _EnvVars:
    _config = _init_config()

    def __class_getitem__(cls, env_var: str) -> str:
        return cls._config[env_var]

    @classmethod
    def contains(cls, env_var: str) -> bool:
        return env_var in cls._config

    @classmethod
    def get_val(cls, env_var: str) -> str:
        return cls._config[env_var]

    @classmethod
    def set_val(cls, env_var: str, val: str) -> None:
        os.environ[env_var] = val
        cls._config[env_var] = val

    @classmethod
    def get_or_default(cls, env_var: str, default: str) -> str:
        if env_var in cls._config:
            return cls._config[env_var]
        return default

    @classmethod
    def get_or_set(cls, env_var: str, new_val: str) -> str:
        if env_var in cls._config:
            return cls._config[env_var]
        cls.set_val(env_var, new_val)
        return new_val

    @classmethod
    def print_all(cls) -> None:
        print("Environment variables\n-----------------")
        for key, value in cls._config.items():
            print(f"{key}: {value}")
        print("Environment variables finished\n-----------------")


def get(env_var: str) -> str:
    return _EnvVars.get_val(env_var)


def contains(env_var: str) -> bool:
    return _EnvVars.contains(env_var)


def get_or_default(env_var: str, default: str) -> str:
    return _EnvVars.get_or_default(env_var, default)


def get_or_set(env_var: str, new_val: str) -> str:
    return _EnvVars.get_or_set(env_var, new_val)


def setdefault(env_var: str, val: str) -> None:
    return _EnvVars.set_val(env_var, val)
