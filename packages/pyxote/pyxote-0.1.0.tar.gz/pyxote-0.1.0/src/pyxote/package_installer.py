from pyxote.command_serializer import CommandSerializer
from pyxote.package_checker import is_package_installed
from typing import Dict


class PackageInstaller(CommandSerializer):
    def __init__(self, package_name: str, commands: Dict[str, str]) -> None:
        super().__init__(commands)
        self.__package_name: str = package_name

    def _is_package_installed(self, package_name: str)-> None:
        is_package_installed(package_name)

    def install(self) -> bool:
        if self._is_package_installed(self.__package_name):
            return False
        self.execute()
        return True
