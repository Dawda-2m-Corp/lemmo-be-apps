import importlib
import logging
import yaml
import os

from apps.core import CONFIG_FILE, CONFIG_DATA

logger = logging.getLogger(__name__)


class AppManager:
    @classmethod
    def _validate_module(cls, module_path: str):
        try:
            module = importlib.import_module(module_path)
            return module
        except ImportError as e:
            logger.debug(f"Failed to import module {module_path}: {e}")
            logger.error(f"Module {module_path} not found. Please check the path.")

    @classmethod
    def _check_file_exists(cls, file_path: str):
        is_file_exists = os.path.exists(file_path)

        if is_file_exists:
            return True

    @classmethod
    def load_data_to_file_config(cls):
        with open(CONFIG_FILE, "r") as file:
            yaml.safe_dump(CONFIG_DATA, file)

        return True

    @classmethod
    def get_apps_from_apps_config_file(cls) -> dict:
        apps = {}
        with open(CONFIG_FILE, "r") as file:
            file_data = yaml.safe_load(file)
            apps = file_data.get("apps")
        return apps

    @classmethod
    def load_apps_into_settings(cls) -> list[str]:
        pass
