import re


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
