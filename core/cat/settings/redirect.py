from cat.utils import get_true_class, singleton
from cat.settings.utils import format_setting_name


class Wrapper:
    def __init__(self, original_class, is_safe: bool = False, need_instantiate: bool = True):
        self.original_class = original_class
        self.true_class = get_true_class(original_class, exclude=[singleton])
        self.setting_name = format_setting_name(self.true_class.__name__)

        self._safe = is_safe
        self._need_instantiate = need_instantiate

        from cat.settings.lazy import cat_settings
        self._setting = cat_settings

    def _get_class_from_settings(self):
        target_class = self._setting.get(self.setting_name)

        if not target_class:
            if self._safe:
                return self.original_class
            raise ValueError(f"Setting '{self.setting_name}' not found in settings")
        
        # If the decorated class/method true class is the target_class,
        # return the oringinal class
        # This let execute decorators on the passed class, also if the class saved not have them
        if get_true_class(target_class) is self.true_class:
            target_class = self.original_class

        return target_class

    def __call__(self, *args, **kwargs):
        if self._need_instantiate:
            return self._get_class_from_settings()(*args, **kwargs)
        
        return self._get_class_from_settings()

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError()

        return getattr(self._get_class_from_settings(), name)
    
    def __instancecheck__(self, instance):
        """Check if the instance is an instance of the original class."""
        return isinstance(instance, self.original_class)


def setting_redirect(safe=False, instanziate=True):
    """
    Decorator to redirect class instantiation to a setting.
    safe: If True, return the original class if setting not found
    """

    def decorator_wrapper(cls):
        return Wrapper(
            original_class=cls,
            is_safe=safe,
            need_instantiate=instanziate
        )
    return decorator_wrapper
