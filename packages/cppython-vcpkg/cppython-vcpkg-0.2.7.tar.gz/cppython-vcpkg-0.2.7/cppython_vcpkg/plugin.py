"""
TODO
"""
import subprocess
from os import name as system_name
from pathlib import Path, PosixPath, WindowsPath
from typing import Type

from cppython_core.schema import Generator, GeneratorData


class VcpkgData(GeneratorData):
    """
    TODO
    """


class VcpkgGenerator(Generator):
    """
    _summary_

    Arguments:
        Generator {_type_} -- _description_
    """

    def __init__(self, pyproject) -> None:
        """
        TODO
        """
        self.data = pyproject

        super().__init__(pyproject)

    def _update_generator(self, path: Path):

        # TODO: Identify why Shell is needed and refactor
        try:
            if system_name == "nt":
                subprocess.check_output([str(WindowsPath("bootstrap-vcpkg.bat"))], cwd=path, shell=True)
            elif system_name == "posix":
                subprocess.check_output(["sh", str(PosixPath("bootstrap-vcpkg.sh"))], cwd=path, shell=True)
        except subprocess.CalledProcessError as error:
            print(error.output)

    @staticmethod
    def name() -> str:
        return "vcpkg"

    @staticmethod
    def data_type() -> Type[GeneratorData]:
        return VcpkgData

    def generator_downloaded(self, path: Path) -> bool:

        try:
            subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], cwd=path)

        except subprocess.CalledProcessError as error:
            print(error.output)
            return False

        return True

    def download_generator(self, path: Path) -> None:

        try:
            subprocess.check_output(
                ["git", "clone", "--depth", "1", "https://github.com/microsoft/vcpkg", "."],
                cwd=path,
            )

        except subprocess.CalledProcessError as error:
            print(error.output)

        self._update_generator(path)

    def update_generator(self, path: Path) -> None:
        try:
            subprocess.check_output(["git", "fetch", "origin", "--depth", "1"], cwd=path)
            subprocess.check_output(["git", "pull"], cwd=path)
        except subprocess.CalledProcessError as error:
            print(error.output)

        self._update_generator(path)

    def install(self) -> None:
        """
        TODO
        """

    def update(self) -> None:
        """
        TODO
        """

    def build(self) -> None:
        """
        TODO
        """
