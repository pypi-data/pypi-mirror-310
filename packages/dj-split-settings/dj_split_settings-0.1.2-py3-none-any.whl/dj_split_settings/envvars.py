from .utils.collections import deep_update
from .utils.settings import get_settings_from_environment


def load_envvars(envvar_settings_prefix: str = "DJANGO_") -> None:
    deep_update(globals(), get_settings_from_environment(envvar_settings_prefix))
