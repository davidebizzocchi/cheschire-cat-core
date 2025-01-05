from typing import Union, Callable, Type, Any

class CatOption:
    def __init__(self, name: str, new_class_: Type[Any], old_class: Type, priority: int):
        self.class_ = new_class_
        self.old_class = old_class
        self.name = name
        self.priority = priority

    def __repr__(self) -> str:
        return f"CatOption(name={self.name}, old_class={self.old_class}, new_class={self.class_} priority={self.priority})"

def option(old_class: Type, *args: Union[str, Type[Any]], priority: int = 1) -> Union[CatOption, Callable]:
    """
    Make options out of classes, can be used with or without arguments.
    old_class: The class to be replaced
    
    Examples:
        .. code-block:: python
            @option(OldClass)
            class MyOption:
                pass
            
            @option(OldClass, priority=2)
            class MyOption:
                pass
    """

    def _make_with_name() -> Callable:
        option_name = old_class.__name__
        def _make_option(class_: Type[Any]) -> CatOption:
            option_ = CatOption(name=option_name, new_class_=class_, old_class=old_class, priority=priority)
            return option_
        return _make_option
    
    try:
        old_class.__name__
    except AttributeError:
        raise ValueError("old_class must be a class")

    return _make_with_name()
