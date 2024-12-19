from typing import Dict, List
from pydantic import BaseModel
from fastapi import Query, Request, APIRouter, HTTPException, Depends

from cat.auth.connection import HTTPAuth
from cat.auth.permissions import AuthPermission, AuthResource


class MemoryPointBase(BaseModel):
    content: str
    metadata: Dict = {}

# TODOV2: annotate all endpoints and align internal usage (no qdrant PointStruct, no langchain Document)
class MemoryPoint(MemoryPointBase):
    id: str
    vector: List[float]

class MetadataUpdate(BaseModel):
    search: Dict = {}
    update: Dict = {}

router = APIRouter()


# GET memories from recall
@router.get("/recall")
async def recall_memories_from_text(
    request: Request,
    text: str = Query(description="Find memories similar to this text."),
    k: int = Query(default=100, description="How many memories to return."),
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.READ)),
) -> Dict:
    """Search k memories similar to given text."""

    ccat = request.app.state.ccat
    vector_memory = ccat.memory.vectors

    # Embed the query to plot it in the Memory page
    query_embedding = ccat.embedder.embed_query(text)
    query = {
        "text": text,
        "vector": query_embedding,
    }

    # Loop over collections and retrieve nearby memories
    collections = list(vector_memory.collections.keys())
    recalled = {}
    for c in collections:
        # only episodic collection has users
        user_id = stray.user_id
        if c == "episodic":
            user_filter = {"source": user_id}
        else:
            user_filter = None

        memories = vector_memory.collections[c].recall_memories_from_embedding(
            query_embedding, k=k, metadata=user_filter
        )

        recalled[c] = []
        for metadata, score, vector, id in memories:
            memory_dict = dict(metadata)
            memory_dict.pop("lc_kwargs", None)  # langchain stuff, not needed
            memory_dict["id"] = id
            memory_dict["score"] = float(score)
            memory_dict["vector"] = vector
            recalled[c].append(memory_dict)

    return {
        "query": query,
        "vectors": {
            "embedder": str(
                ccat.embedder.__class__.__name__
            ),  # TODO: should be the config class name
            "collections": recalled,
        },
    }


# GET collection list with some metadata
@router.get("/collections")
async def get_collections(
    request: Request, stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.READ))
) -> Dict:
    """Get list of available collections"""

    ccat = request.app.state.ccat
    vector_memory = ccat.memory.vectors
    collections = list(vector_memory.collections.keys())

    collections_metadata = []

    for c in collections:
        coll_meta = vector_memory.vector_db.get_collection(c)
        collections_metadata += [{"name": c, "vectors_count": coll_meta.vectors_count}]

    return {"collections": collections_metadata}


# DELETE all collections
@router.delete("/collections")
async def wipe_collections(
    request: Request,
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.DELETE)),
) -> Dict:
    """Delete and create all collections"""

    ccat = request.app.state.ccat
    collections = list(ccat.memory.vectors.collections.keys())
    vector_memory = ccat.memory.vectors

    to_return = {}
    for c in collections:
        ret = vector_memory.vector_db.delete_collection(collection_name=c)
        to_return[c] = ret

    ccat.load_memory()  # recreate the long term memories
    ccat.mad_hatter.find_plugins()

    return {
        "deleted": to_return,
    }


# DELETE one collection
@router.delete("/collections/{collection_id}")
async def wipe_single_collection(
    request: Request,
    collection_id: str,
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.DELETE)),
) -> Dict:
    """Delete and recreate a collection"""

    ccat = request.app.state.ccat
    vector_memory = ccat.memory.vectors

    # check if collection exists
    collections = list(vector_memory.collections.keys())
    if collection_id not in collections:
        raise HTTPException(
            status_code=400, detail={"error": "Collection does not exist."}
        )

    to_return = {}

    ret = vector_memory.vector_db.delete_collection(collection_name=collection_id)
    to_return[collection_id] = ret

    ccat.load_memory()  # recreate the long term memories
    ccat.mad_hatter.find_plugins()

    return {
        "deleted": to_return,
    }


# CREATE a point in memory
@router.post("/collections/{collection_id}/points", response_model=MemoryPoint)
async def create_memory_point(
    request: Request,
    collection_id: str,
    point: MemoryPointBase,
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.WRITE)),
) -> MemoryPoint:
    """Create a point in memory"""

    # do not touch procedural memory
    if collection_id == "procedural":
        raise HTTPException(
            status_code=400, detail={"error": "Procedural memory is read-only."}
        )

    # check if collection exists
    collections = list(stray.memory.vectors.collections.keys())
    if collection_id not in collections:
        raise HTTPException(
            status_code=400, detail={"error": "Collection does not exist."}
        )
    
    # embed content
    embedding = stray.embedder.embed_query(point.content)
    
    # ensure source is set
    if not point.metadata.get("source"):
        point.metadata["source"] = stray.user_id # this will do also for declarative memory

    # create point
    qdrant_point = stray.memory.vectors.collections[collection_id].add_point(
        content=point.content,
        vector=embedding,
        metadata=point.metadata
    )

    return MemoryPoint(
        metadata=qdrant_point.payload["metadata"],
        content=qdrant_point.payload["page_content"],
        vector=qdrant_point.vector,
        id=qdrant_point.id
    )

# DELETE memories
@router.delete("/collections/{collection_id}/points/{point_id}")
async def delete_memory_point(
    request: Request,
    collection_id: str,
    point_id: str,
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.DELETE)),
) -> Dict:
    """Delete a specific point in memory"""

    ccat = request.app.state.ccat
    vector_memory = ccat.memory.vectors

    # check if collection exists
    collections = list(vector_memory.collections.keys())
    if collection_id not in collections:
        raise HTTPException(
            status_code=400, detail={"error": "Collection does not exist."}
        )

    # check if point exists
    points = vector_memory.vector_db.retrieve(
        collection_name=collection_id,
        ids=[point_id],
    )
    if points == []:
        raise HTTPException(status_code=400, detail={"error": "Point does not exist."})

    # delete point
    vector_memory.collections[collection_id].delete_points([point_id])

    return {"deleted": point_id}


@router.delete("/collections/{collection_id}/points")
async def delete_memory_points_by_metadata(
    request: Request,
    collection_id: str,
    metadata: Dict = {},
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.DELETE)),
) -> Dict:
    """Delete points in memory by filter"""

    ccat = request.app.state.ccat
    vector_memory = ccat.memory.vectors

    # delete points
    result = vector_memory.collections[collection_id].delete_points_by_metadata_filter(metadata)

    return {
        "deleted": [],  # TODO: Qdrant does not return deleted points?
        "status": result
    }


# DELETE conversation history from working memory
@router.delete("/conversation_history")
async def wipe_conversation_history(
    request: Request,
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.DELETE)),
) -> Dict:
    """Delete the specified user's conversation history from working memory"""

    stray.working_memory.history = []

    return {
        "deleted": True,
    }

# DELETE vector memory by chat_id
@router.delete("/conversation_history/{chat_id}")
async def wipe_vector_memory_by_chat(
    request: Request,
    chat_id: str,
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.DELETE)),
) -> Dict:
    """Delete vector memory points for a specific chat_id"""
    
    stray.working_memories[chat_id].history = []
    
    return {
        "deleted": True,
        "chat_id": chat_id
    }

# GET conversation history from working memory
@router.get("/conversation_history")
async def get_conversation_history(
    request: Request,
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.READ)),
) -> Dict:
    """Get the specified user's conversation history from working memory"""

    return {"history": stray.working_memory.history}


# GET lista delle working memories
@router.get("/working_memories")
async def get_working_memories_list(
    request: Request,
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.READ)),
) -> Dict:
    """Get list of available working memories"""
    return {"working_memories": list(stray.working_memories.keys())}

# GET una specifica working memory
@router.get("/working_memories/{chat_id}")
async def get_working_memory(
    request: Request,
    chat_id: str,
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.READ)),
) -> Dict:
    """Get a specific working memory"""
    if chat_id not in stray.working_memories:
        raise HTTPException(
            status_code=404, 
            detail={"error": f"Working memory {chat_id} does not exist."}
        )
    
    return {"history": stray.working_memories[chat_id].history}

# DELETE una working memory
@router.delete("/working_memories/{chat_id}") 
async def delete_working_memory(
    request: Request,
    chat_id: str,
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.DELETE)),
) -> Dict:
    """Delete a specific working memory"""
    if chat_id not in stray.working_memories:
        return {
            "deleted": False,
            "message": "There is no working memory"
        }
        
    del stray.working_memories[chat_id]
    return {
        "deleted": True,
        "chat_id": chat_id
    }

# PATCH collection points metadata
@router.patch("/collections/{collection_id}/points/metadata")
async def update_points_metadata(
    request: Request,
    metadata: MetadataUpdate,
    collection_id: str = "declarative",
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.WRITE)),
) -> Dict:
    """Update points metadata in a collection by metadata filter"""
    
    vector_memory = stray.memory.vectors
    collection = vector_memory.collections.get(collection_id)
    
    if not collection:
        raise HTTPException(
            status_code=400,
            detail={"error": "Collection does not exist."}
        )

    # Construct filter from search metadata
    query_filter = collection._qdrant_filter_from_dict(metadata.search)
    
    # Search directly using the constructed filter
    points = vector_memory.vector_db.scroll(
        collection_name=collection_id,
        scroll_filter=query_filter,
        with_payload=True,
        with_vectors=False,
        limit=10000 
    )[0]

    if not points:
        return {
            "matched_points": [],
            "message": "No points found matching search criteria"
        }

    # Extract points data and update metadata
    matched_points = []
    for p in points:
        current_metadata = p.payload.get("metadata", {}).copy()
        current_metadata.update(metadata.update)
        matched_points.append({
            "id": p.id,
            "metadata": current_metadata
        })

    # Update metadata for all points at once, using the complete updated metadata
    # corretto perché memorie delle stesso file
    result = collection.update_points_by_metadata(
        points_ids=[p["id"] for p in matched_points],
        metadata={"metadata": matched_points[0]["metadata"]}  # Usiamo il metadata completo aggiornato
    )

    return {
        "matched_points": matched_points,
        "count": len(matched_points),
        "status": result
    }

# GET points by metadata
@router.get("/collections/{collection_id}/points")
async def get_points_by_metadata(
    request: Request,
    collection_id: str,
    metadata: Dict = {},
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.READ)),
) -> Dict:
    """Get points in a collection by metadata filter"""
    
    vector_memory = stray.memory.vectors
    collection = vector_memory.collections.get(collection_id)
    
    if not collection:
        raise HTTPException(
            status_code=400,
            detail={"error": "Collection does not exist."}
        )

    # Construct filter from metadata
    query_filter = collection._qdrant_filter_from_dict(metadata)
    
    # Search points with the filter
    points = vector_memory.vector_db.scroll(
        collection_name=collection_id,
        scroll_filter=query_filter,
        with_payload=True,
        with_vectors=False,
        limit=10000 
    )[0]  # scroll returns (points, next_page_offset)

    if not points:
        return {
            "points": [],
            "count": 0,
            "message": "No points found matching metadata criteria"
        }

    # Extract points data
    matched_points = [{
        "id": p.id,
        "metadata": p.payload.get("metadata", {}),
    } for p in points]

    return {
        "points": matched_points,
        "count": len(matched_points)
    }

# GET points filtered by metadata
@router.get("/collections/{collection_id}/points/by_metadata")
async def get_points_metadata_only(
    request: Request,
    collection_id: str,
    metadata: Dict = {},
    stray=Depends(HTTPAuth(AuthResource.MEMORY, AuthPermission.READ)),
) -> Dict:
    """Get only metadata of points in a collection filtered by metadata criteria"""
    
    vector_memory = stray.memory.vectors
    collection = vector_memory.collections.get(collection_id)
    
    if not collection:
        raise HTTPException(
            status_code=400,
            detail={"error": "Collection does not exist."}
        )

    # Construct filter from metadata
    query_filter = collection._qdrant_filter_from_dict(metadata)
    
    # Search points with the filter
    points = vector_memory.vector_db.scroll(
        collection_name=collection_id,
        scroll_filter=query_filter,
        with_payload=True,
        with_vectors=False,
        limit=10000 
    )[0]  # scroll returns (points, next_page_offset)

    if not points:
        return {
            "points": [],
            "count": 0,
            "message": "No points found matching metadata criteria"
        }

    # Extract points data
    matched_points = [{
        "id": p.id,
        "metadata": p.payload.get("metadata", {}),
    } for p in points]

    return {
        "points": matched_points,
        "count": len(matched_points)
    }
