import importlib
import os
import json


def load_json(fp: str):
    with open(fp, mode="r", encoding="utf-8") as file:
        return json.load(file)


def load_module(fp: str):
    return importlib.import_module(os.path.relpath(fp).replace("\\", "/").replace("/", "."))


def load_class_module(fp: str, class_name: str):
    module_path = os.path.relpath(fp + "/" + class_name).replace("\\", "/").replace("/", ".")
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


class Game:
    Party: type
    Score: type
    text: dict
    info: dict

    def __init__(self, Party, Score, text, about):
        self.Party = Party
        self.Score = Score
        self.text = text
        self.info = about

    @classmethod
    def load(cls, fp: str):
        Party = load_class_module(fp, "Party")
        Score = load_class_module(fp, "Score")

        text = {}
        info = {}

        for fn in os.listdir(fp):
            name, ext = os.path.splitext(fn)
            if ext == ".json":
                path = os.path.join(fp, fn)
                data = load_json(path)
                if name == "_":
                    info = data
                else:
                    text[name] = data

        return cls(
            Party=Party,
            Score=Score,
            text=text,
            about=info
        )

    @classmethod
    def loadall(cls, dp: str):
        return [cls.load(os.path.join(dp, fn)) for fn in os.listdir(dp)]
