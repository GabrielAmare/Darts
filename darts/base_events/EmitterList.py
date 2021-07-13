from typing import Generic, List, TypeVar, Iterator
from .Emitter import Emitter

E = TypeVar('E')


class EmitterList(Generic[E], Emitter):
    def __init__(self, data: List[E] = None):
        super().__init__()
        self.data: List[E] = data or []

    def __iter__(self) -> Iterator[E]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int) -> E:
        return self.data[index]

    def __setitem__(self, index: int, item: E) -> None:
        self.data[index] = item
        self.emit('set', index, item)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data!r})"

    def append(self, item: E) -> None:
        """Append an `item`."""
        self.data.append(item)
        self.emit('append', item)

    def remove(self, item: E) -> None:
        """Remove and `item`."""
        self.data.remove(item)
        self.emit('remove', item)

    def insert(self, index: int, item: E) -> None:
        """Insert `item` at `index`."""
        self.data.insert(index, item)
        self.emit('insert', index, item)

    def pop(self, index: int) -> E:
        """Pop an item given it's `index`."""
        item = self.data.pop(index)
        self.emit('pop', index, item)
        return item

    def bind_to(self, emitter: Emitter, prefix: str) -> None:
        """Make the `emitter` re-emit `self` events with the given `prefix`"""
        self.on('append', lambda item: emitter.emit(f'{prefix}.append', item))
        self.on('remove', lambda item: emitter.emit(f'{prefix}.remove', item))
        self.on('insert', lambda index, item: emitter.emit(f'{prefix}.insert', index, item))
        self.on('pop', lambda index, item: emitter.emit(f'{prefix}.pop', index, item))
        self.on('set', lambda index, item: emitter.emit(f'{prefix}.set', index, item))

    def index(self, item: E) -> int:
        return self.data.index(item)
