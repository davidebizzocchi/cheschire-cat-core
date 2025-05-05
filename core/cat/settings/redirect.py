from cat.utils import get_true_class, singleton
from cat.settings.utils import format_setting_name


def setting_redirect(safe=False):
    """
    Decorator to redirect class instantiation to a setting.
    safe: If True, return the original class if setting not found
    """
    from cat.settings.lazy import cat_settings

    def decorator_wrapper(cls):
        true_class = get_true_class(cls, exclude=[singleton])
        def wrapper(*args, **kwargs):
            setting_name = format_setting_name(true_class.__name__)
            target_class = cat_settings.get(setting_name)

            if not target_class:
                if safe:
                    return cls(*args, **kwargs)

                raise ValueError(f"Setting '{setting_name}' not found in settings")
            
            # If the decorated class/method true class is the target_class,
            # return the oringinal class
            # This let execute decorators on the passed class, also if the class saved not have them
            if get_true_class(target_class) is true_class:
                return cls(*args, **kwargs)

            return target_class(*args, **kwargs)

        return wrapper
    return decorator_wrapper
