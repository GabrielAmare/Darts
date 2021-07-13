import os
from typing import Dict

from tools37 import JsonFile

from darts.base import ValueHolder


class AppRepository:
    def __init__(self, root: str):
        self.root: str = root
        self.uids: Dict[str, ValueHolder] = {}

    def load_repo(self, repo: str):
        """Load the repository, all the existing file uids are stored."""
        assert repo not in self.uids

        path = os.path.join(self.root, repo)

        os.makedirs(path, exist_ok=True)

        uids = []

        for filename in os.listdir(path):
            basename, extension = os.path.splitext(filename)
            if basename.isnumeric() and extension == '.json':
                uid = int(basename)
                uids.append(uid)

        self.uids[repo] = ValueHolder(uids)

    def _get_path(self, repo: str, uid: int) -> str:
        return os.path.join(self.root, repo, str(uid))

    def _new_uid(self, repo: str) -> int:
        if repo not in self.uids:
            self.load_repo(repo)
        return self.uids[repo].create()

    def _add_uid(self, repo: str, uid: int) -> None:
        if repo not in self.uids:
            self.load_repo(repo)
        self.uids[repo].append(uid)

    def _del_uid(self, repo: str, uid: int) -> None:
        if repo not in self.uids:
            self.load_repo(repo)
        self.uids[repo].remove(uid)

    def create(self, repo: str, data: dict) -> int:
        uid = self._new_uid(repo)
        self._add_uid(repo, uid)

        path = self._get_path(repo, uid)
        JsonFile.save(path, data)
        return uid

    def access(self, repo: str, uid: int) -> dict:
        path = self._get_path(repo, uid)
        data = JsonFile.load(path)
        return data

    def update(self, repo: str, uid: int, data: dict) -> None:
        path = self._get_path(repo, uid)
        JsonFile.save(path, data)

    def delete(self, repo: str, uid: int) -> None:
        self._del_uid(repo, uid)
        path = self._get_path(repo, uid)
        os.remove(path)
