from qdrant_client.http.models import (
    CollectionInfo,
    CollectionStatus,
    OptimizersStatusOneOf,
    CollectionConfig,
    CollectionParams,
    HnswConfig,
    OptimizersConfig
)
from cat.memory.vector_memory.abstract import AbstractVectorMemory
from cat.memory.vector_memory_collection.no_db import VectorMemoryCollection

# This are mock classes for use a valid CollectInfo (pydantic) object.
# In version 1.9.1, only the following parameters are used:
# - points_count = 0

# CollectionConfig
mock_collection_param = CollectionParams(
    vectors=None,
    shard_number=1,
    sharding_method=None,
    replication_factor=1,
    write_consistency_factor=1,
    read_fan_out_factor=None,
    on_disk_payload=True,
    sparse_vectors=None
)
mock_hnsw_config = HnswConfig(
    m=1,
    ef_construct=0,
    full_scan_threshold=1,
    max_indexing_threads=0,
    on_disk=True,
    payload_m=None
)
mock_optimizer_config = OptimizersConfig(
    deleted_threshold=0.42,
    vacuum_min_vector_number=1,
    default_segment_number=10,
    max_segment_size=100,
    memmap_threshold=1,
    indexing_threshold=1,
    flush_interval_sec=1,
    max_optimization_threads=1
)
mock_config = CollectionConfig(
    params=mock_collection_param,
    hnsw_config=mock_hnsw_config,
    optimizer_config=mock_optimizer_config,
    wal_config=None,
    quantization_config=None,
    strict_mode_config=None
)

# CollectionInfo
mock_status = CollectionStatus("green")
mock_optimizer_status = OptimizersStatusOneOf("ok")
mock_collection = CollectionInfo(
    status=mock_status,
    optimizer_status=mock_optimizer_status,
    vectors_count=0,
    indexed_vectors_count=1,
    points_count=0,
    segments_count=0,
    config=mock_config,
    payload_schema={},
)


class VectorMemory(AbstractVectorMemory):
    """
    No vector memory implementation.
    This class is a placeholder for cases where no vector memory is needed.
    """

    def __init__(self):
        """
        Initialize the NoVectorMemory instance.
        """
        self.collections = {}
        for collection_name in ["episodic", "declarative", "procedural"]:
            # Instantiate collection
            collection = VectorMemoryCollection(
            )

            # Update dictionary containing all collections
            # Useful for cross-searching and to create/use collections from plugins
            self.collections[collection_name] = collection

            # Have the collection as an instance attribute
            # (i.e. do things like cat.memory.vectors.declarative.something())
            setattr(self, collection_name, collection)

    def delete_collection(self, *args, **kwargs):
        True

    def get_collection(self, *args, **kwargs):
        return mock_collection
