def load_default_settings():
    from cat.settings.base import WonderlandSettings, SettingElement
    import cat.settings.default as default_settings

    settings = WonderlandSettings()

    # Load default settings
    for var_name, setting in default_settings.__dict__.items():
        if var_name.startswith("_") or not isinstance(setting, SettingElement):
            continue

        if isinstance(setting, SettingElement):
            settings.set(setting.name, setting)
