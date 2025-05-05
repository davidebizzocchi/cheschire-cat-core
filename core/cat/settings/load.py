from typing import Callable


def load_settings_from_module(module, exclude_private=True, exclude_non_setting=True, predicate: Callable = None, **kwargs):
    """
    Load settings from a given module.
    
    Args:
        module: The module to load settings from.
        exclude_private: If True, exclude private variables (starting with '_').
        exclude_non_setting: If True, exclude non-setting elements.
    """
    from cat.settings.base import WonderlandSettings, SettingElement
    settings = WonderlandSettings()

    # Search for all variables in the module
    for var_name, setting in module.__dict__.items():
        if exclude_private and var_name.startswith("_"): continue
        if exclude_non_setting and not isinstance(setting, SettingElement): continue
        if predicate and not predicate(setting): continue

        if isinstance(setting, SettingElement):
            settings.set(setting.name, setting, **kwargs)

    import pprint
    print(f"settings: {pprint.pformat(settings._settings)}")


def load_default_settings():
    import cat.settings.default as default_settings
    load_settings_from_module(
        module=default_settings,
        exclude_private=True,
        exclude_non_setting=True,
    )

def load_env_settings():
    import cat.settings.env as env_settings
    load_settings_from_module(
        module=env_settings,
        exclude_private=True,
        exclude_non_setting=True,
    )

def load_custom_settings():
    import cat.settings.settings as custom_settings
    load_settings_from_module(
        module=custom_settings,
        exclude_private=True,
        exclude_non_setting=False,
    )