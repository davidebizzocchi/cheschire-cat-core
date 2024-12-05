from typing import List
from abc import ABC, abstractmethod, ABCMeta
from cat.utils import singleton_meta


from cat.utils import BaseModelDict

class AgentOutput(BaseModelDict):
    output: str | None = None
    intermediate_steps: List = []
    return_direct: bool = False

class Meta(singleton_meta, ABCMeta):
    pass

class BaseAgent(ABC, metaclass=Meta):

    @abstractmethod
    async def execute(*args, **kwargs) -> AgentOutput:
        pass