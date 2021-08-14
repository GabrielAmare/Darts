import os


class BaseFile:
    extension: str = ""

    @classmethod
    def exists(cls, fp: str) -> bool:
        return os.path.exists(cls.parse_fp(fp))

    @classmethod
    def parse_fp(cls, fp: str) -> str:
        if fp.endswith(cls.extension):
            return fp
        else:
            return fp + cls.extension

    @classmethod
    def _open_w(cls, fp: str):
        try:
            return open(cls.parse_fp(fp), mode="w", encoding="utf-8")
        except FileNotFoundError as e:
            raise FileNotFoundError(os.path.abspath(e.filename))

    @classmethod
    def _open_r(cls, fp: str):
        try:
            return open(cls.parse_fp(fp), mode="r", encoding="utf-8")
        except FileNotFoundError as e:
            raise FileNotFoundError(os.path.abspath(e.filename))

    @classmethod
    def _open_a(cls, fp: str):
        try:
            return open(cls.parse_fp(fp), mode="a", encoding="utf-8")
        except FileNotFoundError as e:
            raise FileNotFoundError(os.path.abspath(e.filename))
