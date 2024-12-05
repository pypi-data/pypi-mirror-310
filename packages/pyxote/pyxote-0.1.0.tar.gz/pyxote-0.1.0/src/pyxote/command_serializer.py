from typing import Dict
from pyxote.installer import install_package


class CommandSerializer:
    def __init__(self, commands: Dict[str, str]) -> None:
        self.__commands = commands


    def _install(self, command, package_name) -> None:
        install_package(command, package_name)

    def execute(self) -> bool:
        for package_name, command in self.__commands.items():
            self._install(command, package_name)
        return True
