from tinydb import TinyDB

from cat.utils import singleton
from cat.env import get_env
from cat.settings.lazy import cat_settings


@singleton
class Database:
    def __init__(self):
        self.db = TinyDB(self.get_file_name())

    def get_file_name(self):
        tinydb_file = cat_settings.CCAT_METADATA_FILE
        return tinydb_file


def get_db():
    return Database().db
