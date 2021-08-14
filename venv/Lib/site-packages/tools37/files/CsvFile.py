from typing import List, Union, Generator, Dict, Tuple
from .BaseFile import BaseFile


class CsvFile(BaseFile):
    extension = ".csv"
    COMMA_ALT = "<COMMA>"
    NEWLINE_ALT = "<NEWLINE>"

    @classmethod
    def _save_arg(cls, arg: str) -> str:
        return arg.replace(',', cls.COMMA_ALT).replace('\n', cls.NEWLINE_ALT)

    @classmethod
    def _save_line(cls, keys: List[str], vals: Dict[str, str]):
        return "\n" + ",".join(cls._save_arg(str(vals.get(key, ''))) for key in keys)

    @classmethod
    def save(cls, fp: str, keys: List[str], data: List[Dict[str, str]]) -> None:
        with cls._open_w(fp) as file:
            file.write(",".join(keys))
            for vals in data:
                file.write(cls._save_line(keys, vals))

    @classmethod
    def _load_arg(cls, arg: str) -> str:
        return arg.replace(cls.COMMA_ALT, ',').replace(cls.NEWLINE_ALT, '\n')

    @classmethod
    def _load_line(cls, line: str) -> Tuple[str]:
        return tuple(
            cls._load_arg(arg.strip())
            for arg in line.split(',')
        )

    @classmethod
    def load(cls, fp: str) -> Generator[Dict[str, str], None, None]:
        with cls._open_r(fp) as file:
            keys = None
            for line in file.readlines():
                if keys is None:
                    keys = cls._load_line(line)
                else:
                    vals = cls._load_line(line)
                    yield dict(zip(keys, vals))

    @classmethod
    def add(cls, fp: str, keys: List[str], data: Union[Dict[str, str], List[Dict[str, str]]]):
        if isinstance(data, dict):
            data = [data]

        with cls._open_a(fp) as file:
            for vals in data:
                file.write(cls._save_line(keys, vals))
