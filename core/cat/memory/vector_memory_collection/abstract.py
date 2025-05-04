from abc import ABC, abstractmethod
from typing import Any, List, Iterable, Optional


class AbstractVectorMemoryCollection(ABC):

    @abstractmethod
    def add_point(
        self,
        content: str,
        vector: Iterable,
        metadata: dict = None,
        id: Optional[str] = None,
        **kwargs: Any,
    ) -> List[str]:
        """Add a point (and its metadata) to the vectorstore.

        Args:
            content: original text.
            vector: Embedding vector.
            metadata: Optional metadata dict associated with the text.
            id:
                Optional id to associate with the point. Id has to be a uuid-like string.

        Returns:
            Point id as saved into the vectorstore.
        """
        pass

    @abstractmethod
    def delete_points_by_metadata_filter(self, metadata=None):
        pass

    @abstractmethod
    def delete_points(self, points_ids):
        """Delete point in collection"""
        pass

    @abstractmethod
    def recall_memories_from_embedding(
        self, embedding, metadata=None, k=5, threshold=None
    ):
        """Retrieve similar memories from embedding"""
        pass
    
    @abstractmethod
    def get_points(self, ids: List[str]):
        pass

    @abstractmethod
    def get_all_points(
            self,
            limit: int = 10000,
            offset: str | None = None
        ):
        """Retrieve all the points in the collection with an optional offset and limit."""
        pass
