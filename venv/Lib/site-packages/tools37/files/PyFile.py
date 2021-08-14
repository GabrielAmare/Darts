from .BaseFile import BaseFile


class PyFile(BaseFile):
    extension = ".py"

    @classmethod
    def save(cls, fp: str, content: str) -> None:
        with cls._open_w(fp) as file:
            file.write(content)

    @classmethod
    def load(cls, fp: str) -> str:
        with cls._open_r(fp) as file:
            return file.read()
