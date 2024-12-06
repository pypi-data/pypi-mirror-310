from .utils.collections import deep_update
from .utils.settings import get_settings_from_environment

def load_envvars():
    deep_update(globals(), get_settings_from_environment(ENVVAR_SETTINGS_PREFIX))  # type: ignore # noqa: F821
    