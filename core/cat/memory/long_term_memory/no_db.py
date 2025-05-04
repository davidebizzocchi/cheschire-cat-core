from cat.memory.long_term_memory.abstract import AbstractLongTermMemory
from cat.memory.vector_memory.no_db import VectorMemory


class LongTermMemory(AbstractLongTermMemory):
    def __init__(self, *args, **kwargs):
        """
        No long-term memory implementation.
        This class is a placeholder for cases where no long-term memory is needed.
        """
        self.vectors = VectorMemory()
        print(f"args: {args}, kwargs: {kwargs}")
