from cat.settings.base import SettingElement
from cat.env import get_env


CCAT_CORE_HOST = SettingElement(
    name="CCAT_CORE_HOST",
    default=get_env("CCAT_CORE_HOST"),
    type_=str
)

CCAT_CORE_PORT = SettingElement(
    name="CCAT_CORE_PORT",
    default=get_env("CCAT_CORE_PORT"),
    type_=str | int
)

CCAT_CORE_USE_SECURE_PROTOCOLS = SettingElement(
    name="CCAT_CORE_USE_SECURE_PROTOCOLS",
    default=get_env("CCAT_CORE_USE_SECURE_PROTOCOLS"),
    type_=str | None | bool
)

CCAT_API_KEY = SettingElement(
    name="CCAT_API_KEY",
    default=get_env("CCAT_API_KEY"),
    type_=str | None
)

CCAT_API_KEY_WS = SettingElement(
    name="CCAT_API_KEY_WS",
    default=get_env("CCAT_API_KEY_WS"),
    type_=str | None
)

CCAT_DEBUG = SettingElement(
    name="CCAT_DEBUG",
    default=get_env("CCAT_DEBUG"),
    type_=str | bool
)

CCAT_LOG_LEVEL = SettingElement(
    name="CCAT_LOG_LEVEL",
    default=get_env("CCAT_LOG_LEVEL"),
    type_=str
)

CCAT_CORS_ALLOWED_ORIGINS = SettingElement(
    name="CCAT_CORS_ALLOWED_ORIGINS",
    default=get_env("CCAT_CORS_ALLOWED_ORIGINS"),
    type_=str | None
)

CCAT_QDRANT_HOST = SettingElement(
    name="CCAT_QDRANT_HOST",
    default=get_env("CCAT_QDRANT_HOST"),
    type_=str | None
)

CCAT_QDRANT_PORT = SettingElement(
    name="CCAT_QDRANT_PORT",
    default=get_env("CCAT_QDRANT_PORT"),
    type_=str | int
)

CCAT_QDRANT_API_KEY = SettingElement(
    name="CCAT_QDRANT_API_KEY",
    default=get_env("CCAT_QDRANT_API_KEY"),
    type_=str | None
)

CCAT_SAVE_MEMORY_SNAPSHOTS = SettingElement(
    name="CCAT_SAVE_MEMORY_SNAPSHOTS",
    default=get_env("CCAT_SAVE_MEMORY_SNAPSHOTS"),
    type_=str | bool
)

CCAT_METADATA_FILE = SettingElement(
    name="CCAT_METADATA_FILE",
    default=get_env("CCAT_METADATA_FILE"),
    type_=str
)

CCAT_JWT_SECRET = SettingElement(
    name="CCAT_JWT_SECRET",
    default=get_env("CCAT_JWT_SECRET"),
    type_=str
)

CCAT_JWT_ALGORITHM = SettingElement(
    name="CCAT_JWT_ALGORITHM",
    default=get_env("CCAT_JWT_ALGORITHM"),
    type_=str
)

CCAT_JWT_EXPIRE_MINUTES = SettingElement(
    name="CCAT_JWT_EXPIRE_MINUTES",
    default=get_env("CCAT_JWT_EXPIRE_MINUTES"),  # JWT expires after 1 day
    type_=str
)

CCAT_HTTPS_PROXY_MODE = SettingElement(
    name="CCAT_HTTPS_PROXY_MODE",
    default=get_env("CCAT_HTTPS_PROXY_MODE"),
    type_=str | bool
)

CCAT_CORS_FORWARDED_ALLOW_IPS = SettingElement(
    name="CCAT_CORS_FORWARDED_ALLOW_IPS",
    default=get_env("CCAT_CORS_FORWARDED_ALLOW_IPS"),
    type_=str
)

CCAT_CORS_ENABLED = SettingElement(
    name="CCAT_CORS_ENABLED",
    default=get_env("CCAT_CORS_ENABLED"),
    type_=str | bool
)

CCAT_CACHE_TYPE = SettingElement(
    name="CCAT_CACHE_TYPE",
    default=get_env("CCAT_CACHE_TYPE"),
    type_=str
)

CCAT_CACHE_DIR = SettingElement(
    name="CCAT_CACHE_DIR",
    default=get_env("CCAT_CACHE_DIR"),
    type_=str
)

CCAT_QDRANT_CLIENT_TIMEOUT = SettingElement(
    name="CCAT_QDRANT_CLIENT_TIMEOUT",
    default=get_env("CCAT_QDRANT_CLIENT_TIMEOUT"),
    type_=str | None
)
