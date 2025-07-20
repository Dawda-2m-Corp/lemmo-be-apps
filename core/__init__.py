import pathlib
import os

PROJECT_ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

DEFAULT_APPS_CONFIG = [
    {
        "name": "Authentication",
        "path": "apps.authentication",
        "url_path": "apps.authentication.urls",
    },
    {
        "name": "System Integration",
        "path": "apps.integration",
        "url_path": "apps.integration.urls",
    },
    {
        "name": "Analytical Dashboard",
        "path": "apps.dashboard",
        "url_path": "apps.dashboard.urls",
    },
    {
        "name": "Facility Management",
        "path": "apps.facility",
        "url_path": "apps.facility.urls",
    },
    {
        "name": "Inventory Management",
        "path": "apps.inventory",
        "url_path": "apps.inventory.urls",
    },
    {
        "name": "Order Management",
        "path": "apps.order",
        "url_path": "apps.order.urls",
    },
]


EXTRA_TEMPLATE_CONFIG = {}

ADAPTER_INTEGRATIONS = {}

CONFIG_FILE = os.path.join(PROJECT_ROOT_DIR, "config.yml")
CONFIG_DATA = {
    "apps": DEFAULT_APPS_CONFIG,
    "extra_templates": EXTRA_TEMPLATE_CONFIG,
    "adapter_integrations": ADAPTER_INTEGRATIONS,
}
