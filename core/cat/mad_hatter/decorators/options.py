from typing import Union, Callable, Type, Any

class CatOption:
    def __init__(self, name: str, class_: Type[Any], priority: int):
        self.class_ = class_
        self.name = name
        self.priority = priority

    def __repr__(self) -> str:
        return f"CatOption(name={self.name}, priority={self.priority})"

def option(*args: Union[str, Type[Any]], priority: int = 1) -> Union[CatOption, Callable]:
    """
    Make options out of classes, can be used with or without arguments.
    Examples:
        .. code-block:: python
            @option
            class MyOption:
                pass
            
            @option("custom_name", priority=2)
            class MyOption:
                pass
    """

    def _make_with_name(option_name: Any) -> Callable:
        if not isinstance(option_name, str):
            option_name = option_name.__name__
        def _make_option(class_: Type[Any]) -> CatOption:
            option_ = CatOption(name=option_name, class_=class_, priority=priority)
            return option_
        return _make_option

    if len(args) == 1 and isinstance(args[0], str):
        # Example usage: @option("custom_name", priority=2)
        return _make_with_name(args[0])
    elif len(args) == 1 and isinstance(args[0], type):
        # Example usage: @option
        return _make_with_name(args[0].__name__)(args[0])
    elif len(args) == 0:
        # Example usage: @option(priority=2)
        def _partial(class_: Type[Any]) -> CatOption:
            return _make_with_name(class_.__name__)(class_)
        return _partial
    else:
        raise ValueError("Too many arguments for option decorator")
