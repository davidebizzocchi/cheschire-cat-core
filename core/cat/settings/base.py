import importlib
import inspect
from typing import Any, Dict, Type
from functools import wraps

from cat.utils import singleton, get_true_class, get_class_only_with_singleton


def parse_key(func) -> str:
    """
    Parse the key to ensure it is a string.
    
    Args:
        key: The key to parse, can be a string or type.
    
    Returns:
        Parsed key as a string.
    """

    @wraps(func)
    def wrapper(self, key: Any, *args, **kwargs) -> str:
        if inspect.isfunction(key):
            key = get_true_class(key)

        if inspect.isclass(key): key = key.__name__
        else: key = str(key)

        return func(self, key, *args, **kwargs)
    
    return wrapper


class SettingElement:
    """
    Class representing a setting element.
    Provides methods to get, set, and delete settings.
    Check if the value is of the expected type.
    """

    def __init__(self, name: str, default: Any, type_: Type = str):
        self.name = name
        self.default = default
        self.type_ = Type if type_ == "class" else type_

        self.value = None
        self.set(default)

    def get(self) -> Any:
        return self.value

    def set(self, value: Any) -> None:
        value = self._parse_value(value)

        # Check if the value is of the expected type
        if self.type_ and not isinstance(value, self.type_):
            raise TypeError(f"Type mismatch for setting '{self.name}': expected {self.type_}, got {type(value)}")
            return

        self.value = value

    def delete(self) -> None:
        self.value = None


    def _parse_value(self, value: Any) -> Any:
        # Import class from string
        # e.g. "module.ClassName"
        if isinstance(value, str) and self.type_ is Type:
            try:
                module_name, class_name = value.rsplit(".", 1)
                module = importlib.import_module(module_name.replace("/", ".").replace(".py", ""))
                return  get_class_only_with_singleton(getattr(module, class_name))
            except (ImportError, AttributeError) as e:
                raise ImportError(f"Error importing class '{value}': {e}")
            
        return value


@singleton
class WonderlandSettings:
    """
    Singleton class to manage application settings.
    Provides a unified interface to access and modify settings.
    """
    
    def __init__(self):
        self._settings: Dict[str, Any] = {}

    @parse_key
    def get(self, key) -> Any | None:
        """Get a setting value."""
        value = self._settings.get(key, None)

        if value and isinstance(value, SettingElement):
            return value.get()
        return value
    
    @parse_key
    def set(self, key: str, value: Any, force: bool = False) -> None:
        """
        Set a setting value.
        
        Args:
            key: The key for the setting.
            value: The value to set.
            force: If True and the value is not a SettingElement, set it directly.
        """
        if value and isinstance(value, SettingElement):
            self._settings[key] = value
        elif force:
            # If the setting is not a SettingElement, set it directly
            self._settings[key] = value

    @parse_key
    def delete(self, key: str) -> None:
        """Delete a setting."""
        if key in self._settings:
            self._settings[key] = None

    @parse_key
    def get_default(self, key: str) -> Any | None:
        """Get the default value for a setting or None."""
        value = self._settings.get(key, None)

        if value and  isinstance(value, SettingElement):
            return value.default
        return None
    
    @parse_key
    def has(self, key: str) -> bool:
        """Check if a setting exists."""
        return key in self._settings
