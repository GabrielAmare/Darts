from tools37.files import DictInterface


class Profile(DictInterface):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(uuid=data['uuid'], name=data['name'])

    def to_dict(self) -> dict:
        return dict(uuid=self.uuid, name=self.name)

    def __init__(self, uuid: int, name: str):
        """
        :param uuid: The player unique identifier.
        :param name: The player profile name.
        """
        self.uuid: int = uuid
        self.name: str = name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.uuid!r}, {self.name!r})"