from typing import TypeVar, Generic, List, Iterator, Tuple

K = TypeVar('K')
V = TypeVar('V')


class OrderedHash(Generic[K, V]):
    def __init__(self):
        self.keys: List[K] = []
        self.values: List[V] = []

    def __iter__(self) -> Iterator[K]:
        return iter(self.keys)

    def __len__(self) -> int:
        return len(self.keys)

    def __setitem__(self, key: K, value: V) -> None:
        if key in self.keys:
            index = self.keys.index(key)
            self.values[index] = value

        else:
            self.keys.append(key)
            self.values.append(value)

    def __getitem__(self, key: K) -> V:
        if key in self.keys:
            index = self.keys.index(key)
            return self.values[index]

        else:
            raise KeyError(key)

    def __delitem__(self, key: K) -> None:
        if key in self.keys:
            index = self.keys.index(key)
            del self.keys[index]
            del self.values[index]

        else:
            raise KeyError(key)

    def items(self) -> Iterator[Tuple[K, V]]:
        return iter(zip(self.keys, self.values))
