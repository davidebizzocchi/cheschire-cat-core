from functools import wraps


class LazySettings:
    """
    A class that lazily loads settings from a configuration file.
    """

    def __init__(self):
        # Use object's __setattr__ to avoid recursion in our __setattr__
        object.__setattr__(self, "_settings", None)

    def _setup(self):
        from cat.settings.base import WonderlandSettings
        self._settings = WonderlandSettings()

    @staticmethod
    def _check_setup():
        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):
                self = args[0]
                if not self._settings:
                    self._setup()
                return func(*args, **kwargs)
            return inner
        return wrapper


    @_check_setup()
    def get(self, key):
        return self._settings.get(key)
    
    @_check_setup()
    def set(self, key, value):
        return self._settings.set(key, value)
    
    @_check_setup()
    def delete(self, key):
        return self._settings.delete(key)
    
    @_check_setup()
    def get_default(self, key):
        return self._settings.get_default(key)
    
    @_check_setup()
    def has(self, key):
        return self._settings.has(key)


    def __getattr__(self, name):
        """
        Get the value of a setting by its name.
        If the setting is not found, it will return None.
        """
        if name == "_settings":
            raise AttributeError()

        if not self._settings:
            self._setup()

        if self._settings.has(name):
            return self._settings.get(name)
        else:
            raise AttributeError(f"Setting '{name}' not found.")
        
    def __setattr__(self, name, value):
        """
        Set the value of a setting by its name.
        If the setting is not found, it will raise an AttributeError.
        """
        if name == '_settings':
            object.__setattr__(self, name, value)
            return

        if not self._settings:
            self._setup()

        if self._settings.has(name):
            self._settings.set(name, value)
        else:
            raise AttributeError(f"Setting '{name}' not found.")

cat_settings = LazySettings()