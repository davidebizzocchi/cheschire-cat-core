from abc import ABC, abstractmethod


# @singleton REFACTOR: worth it to have this (or LongTermMemory) as singleton?
class AbstractVectorMemory(ABC):
    """
    Cat's non-volatile memory.
    This is an abstract class to interface with the Cat's vector memory collections.

    Attributes
     - local_vector_db : QdrantClient
    """


    local_vector_db = None

    @abstractmethod
    def delete_collection(self, collection_name: str):
        """Delete specific vector collection"""
        pass
    
    @abstractmethod
    def get_collection(self, collection_name: str):
        """Get collection info"""
        pass
