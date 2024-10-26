"""td models"""
import pkgutil
import importlib
from pathlib import Path

def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent

    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="app.db.models.",
    )

    for module_info in modules:
        if module_info.ispkg:
            continue
        module_name = module_info.name
        try:
            importlib.import_module(module_name)
        except ImportError as e:
            print(f"Failed to import {module_name}: {e}")