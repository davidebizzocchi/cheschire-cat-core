import re
from cat.utils import get_true_class, singleton


def format_setting_name(name: str) -> str:
    """Convert camelCase/PascalCase names to SCREAMING_SNAKE_CASE format.

    Args:
        name: Input name in camelCase or PascalCase format

    Returns:
        str: Converted name in SCREAMING_SNAKE_CASE format

    Examples:
        >>> format_setting_name("CheshireCat")
        'CHESHIRE_CAT'
        >>> format_setting_name("maxFileSize")
        'MAX_FILE_SIZE'
        >>> format_setting_name("HTTPResponse")
        'HTTP_RESPONSE'
    """
    # Handle all-uppercase acronyms at start of string
    name = re.sub(r'^([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    # Insert underscores between camelCase and convert to uppercase
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.upper()


def setting_redirect(safe=False):
    """
    Decorator to redirect class instantiation to a setting.
    safe: If True, return the original class if setting not found
    """
    from cat.settings import cat_settings

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
