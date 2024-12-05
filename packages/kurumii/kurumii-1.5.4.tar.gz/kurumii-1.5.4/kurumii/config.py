import os
import configparser
import logging

class ConfigRegistry:
    """
    A global registry to manage and access Config instances by ID.
    """
    _registry = {}

    @classmethod
    def register(cls, config_id, config_instance):
        """
        Register a new Config instance with a unique ID.
        """
        if config_id in cls._registry:
            raise ValueError(f"Config ID '{config_id}' is already registered.")
        cls._registry[config_id] = config_instance

    @classmethod
    def get(cls, config_id):
        """
        Retrieve a Config instance by its ID.
        """
        if config_id not in cls._registry:
            raise ValueError(f"Config ID '{config_id}' is not registered.")
        return cls._registry[config_id]

    @classmethod
    def unregister(cls, config_id):
        """
        Remove a Config instance from the registry.
        """
        if config_id in cls._registry:
            del cls._registry[config_id]
        else:
            raise ValueError(f"Config ID '{config_id}' is not registered.")


class Config:
    """
    Configuration manager with optional integration into a global registry.
    """
    def __init__(self, config_file=None, log_namespace="default"):
        self.config = configparser.ConfigParser()
        self.config_file = config_file or os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
        self.log_dir = os.path.join(os.path.dirname(self.config_file), "logs", log_namespace)
        self.filepath = os.path.join(self.log_dir, f"config_{log_namespace}.log")
        os.makedirs(self.log_dir, exist_ok=True)
        self._setup_logger()
        self.load_config()

    def _setup_logger(self):
        logging.basicConfig(
            filename=self.filepath,
            filemode='a',
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(f"ConfigLogger_{id(self)}")

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                self.config.read(self.config_file)
                self.logger.info("Configuration loaded successfully.")
            except Exception as e:
                self.logger.error(f"Failed to load configuration: {e}")
        else:
            self.logger.error(f"Config file '{self.config_file}' not found.")

    def register(self, config_id):
        """
        Register this Config instance in the global registry.
        """
        ConfigRegistry.register(config_id, self)

