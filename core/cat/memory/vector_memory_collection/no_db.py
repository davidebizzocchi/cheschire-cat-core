from typing import Any, List, Iterable, Optional
from qdrant_client.http.models import PointStruct

from cat.memory.vector_memory_collection.abstract import AbstractVectorMemoryCollection


class VectorMemoryCollection(AbstractVectorMemoryCollection):
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
        return PointStruct(
            id=id or "mock_id",
            payload={
                "page_content": content,
                "metadata": metadata,
            },
            vector=vector
        )

    def delete_points_by_metadata_filter(self, *args, **kwargs):
        pass

    def delete_points(self, *args, **kwargs):
        """Delete point in collection"""
        pass

    def recall_memories_from_embedding(self, *args, **kwargs):
        """Retrieve similar memories from embedding"""
        return []
    
    def get_points(self, ids: List[str]):
        return []

    def get_all_points(
            self,
            limit: int = 10000,
            offset: str | None = None
        ):
        """Retrieve all the points in the collection with an optional offset and limit."""
        return [], None
