from cat.env import get_env
from cat.memory.long_term_memory import NoLongTermMemory, LongTermMemory


def get_long_term_memory_class():
    """
    Get the long-term memory instance.
    This function is a placeholder for the actual implementation.
    """
    not_use_db = get_env("CCAT_USE_VECTOR_DB") == "false"
    print(f"get_long_term_memory_class: not_use_db={not_use_db}")

    if not_use_db:
        return NoLongTermMemory
    
    return LongTermMemory
