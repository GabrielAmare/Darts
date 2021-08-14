import os
import json
from typing import Union
from .BaseFile import BaseFile


class JsonFile(BaseFile):
    extension = ".json"

    @classmethod
    def save(cls, fp: str, data: Union[dict, list]) -> None:
        with cls._open_w(fp) as file:
            json.dump(data, file)

    @classmethod
    def load(cls, fp: str) -> Union[dict, list]:
        with cls._open_r(fp) as file:
            return json.load(file)

    @classmethod
    def load_init(cls, fp: str, default: Union[dict, list]):
        if not os.path.exists(cls.parse_fp(fp)):
            cls.save(fp, default)

        return cls.load(fp)
