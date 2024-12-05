import os
import shutil


def is_package_installed(package_name: str, default_path: str = "") -> bool:
    package_exist: str | None = shutil.which(package_name)
    default_path_exist: bool = (
        os.path.exists(os.path.expanduser(default_path)) if default_path else False
    )
    if package_exist or default_path_exist:
        print(f"Package {package_name} is already installed.")
        return True
    return False
