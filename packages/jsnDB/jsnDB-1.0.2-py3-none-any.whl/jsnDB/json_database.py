import logging
from colorlog import ColoredFormatter
import json
from pathlib import Path




class CustomDict(dict):
    """Custom dict with logging for all CRUD operations."""
    
    def __delitem__(self, key):
        if key in self:
            logging.info(f"Deleted key: {key}")
        else:
            logging.warning(f"Tried to delete non-existent key: {key}")
        super().__delitem__(key)

    def __setitem__(self, key, value):
        action = "Updated" if key in self else "Added"
        logging.info(f"{action} key: {key}, value: {value}")
        super().__setitem__(key, value)
        
    def clear(self):
        logging.info("Cleared all keys from CustomDict")
        super().clear()

    def pop(self, key, default=None):
        if key in self:
            logging.info(f"Popped key: {key}, value: {self[key]}")
        else:
            logging.warning(f"Tried to pop non-existent key: {key}")
        return super().pop(key, default)

    def popitem(self):
        try:
            key, value = super().popitem()
            logging.info(f"Popped item: key: {key}, value: {value}")
            return key, value
        except KeyError:
            logging.error("Tried to popitem from an empty CustomDict")
            raise

    def update(self, *args, **kwargs):
        updates = dict(*args, **kwargs)
        for key, value in updates.items():
            action = "Updated" if key in self else "Added"
            logging.info(f"{action} key: {key}, value: {value}")
        super().update(*args, **kwargs)

    def setdefault(self, key, default=None):
        if key not in self:
            logging.info(f"Set default for key: {key}, value: {default}")
        else:
            logging.info(f"Key: {key} already exists with value: {self[key]}")
        return super().setdefault(key, default)

    def __getitem__(self, key):
        if key in self:
            logging.info(f"Accessed key: {key}, value: {self[key]}")
        else:
            logging.warning(f"Tried to access non-existent key: {key}")
        return super().__getitem__(key)

    def __contains__(self, key):
        exists = super().__contains__(key)
        logging.info(f"Key {'exists' if exists else 'does not exist'}: {key}")
        return exists

class JsonDB:
    """A lightweight JSON-based database."""

    def __init__(self, filename: str = "db.json", enable_logging: bool = True):
        """
        Initialize the database.

        :param filename: Name of the JSON database file.
        :param enable_logging: Enable or disable logging.
        """
        self.file = Path(filename)
        self.db = self._initialize_file()
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.DEBUG if enable_logging else logging.WARNING,
        )
        logging.info("Database initialized.")
    
    def _initialize_file(self) -> dict:
        """Ensure the database file exists and is valid JSON."""
        if not self.file.exists():
            self.file.write_text("{}") 
        try:
            return CustomDict(json.loads(self.file.read_text()))
        except json.JSONDecodeError:
            logging.error("Database file contains invalid JSON.")
            return CustomDict()

    def _write_to_file(self):
        """Write the current database state to the file."""
        try:
            self.file.write_text(json.dumps(self.db, indent=4))
            logging.info("Database committed to file.")
        except Exception as e:
            logging.error(f"Failed to write to file: {e}")

    def add(self, key: str, value: any):
        """
        Add or update a key-value pair in the database.

        :param key: The key to add or update.
        :param value: The value to associate with the key.
        """
        self.db[key] = value
        logging.info(f"Added/Updated key: {key}, Value: {value}")
    def addMany(self, data : dict):
        """Add or update multiple entries in the database
        :param data: The dict to add or update
        """
        self.db.update(data)
        logging.info(f"Added/Updated {data} in the database")

    def pop(self, key: str):
        """
        Remove a key-value pair from the database.

        :param key: The key to remove.
        :raises KeyError: If the key does not exist in the database.
        """
        if key in self.db:
            self.db.pop(key)
            logging.info(f"Popped key: {key}")
        else:
            logging.error(f"Key '{key}' not found in database.")
            raise KeyError(f"Key '{key}' not found.")

    def get(self, key: str) -> any:
        """
        Retrieve a value from the database by key.

        :param key: The key to retrieve.
        :return: The value associated with the key.
        :raises KeyError: If the key does not exist in the database.
        """
        if key in self.db:
            return self.db[key]
        else:
            logging.error(f"Key '{key}' not found in database.")
            raise KeyError(f"Key '{key}' not found.")

    def get_all(self) -> dict:
        """
        Get the entire database.

        :return: A dictionary representing the database.
        """
        logging.info("Fetched the entire database.")
        return self.db

    def commit(self):
        """Commit the current state of the database to the file."""
        self._write_to_file()

    def close(self):
        """Close database by clearing all entries"""
        self.db.clear()
        logging.info("Closed the database.")

    def set_logging(self, enable: bool):
        """
        Enable or disable logging.

        :param enable: True to enable debug-level logging, False for warnings only.
        """
        logging.getLogger().setLevel(logging.DEBUG if enable else logging.WARNING)
    
    