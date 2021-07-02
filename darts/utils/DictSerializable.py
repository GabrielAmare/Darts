class DictSerializable:
    @classmethod
    def from_dict(cls, data: dict):
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError
