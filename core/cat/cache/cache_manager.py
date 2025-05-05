from cat.env import get_env
from cat.settings.lazy import cat_settings
from cat.settings.redirect import setting_redirect


@setting_redirect()
class CacheManager:
    """Class to instantiate different cache types."""

    def __init__(self):

        self.cache_type = cat_settings.CCAT_CACHE_TYPE
        
        if self.cache_type == "in_memory":
            from cat.cache.in_memory_cache import InMemoryCache
            self.cache = InMemoryCache()
        elif self.cache_type == "file_system":
            cache_dir = cat_settings.CCAT_CACHE_DIR
            from cat.cache.file_system_cache import FileSystemCache
            self.cache = FileSystemCache(cache_dir)
        else:
            raise ValueError(f"Cache type {self.cache_type} not supported")