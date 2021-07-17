from typing import Iterator

from darts.Profile import Profile
from darts.errors import ProfileNotFoundError
from .JsonFilesManager import JsonFilesManager


class ProfilesManager(JsonFilesManager):
    def __init__(self, path: str):
        super().__init__(path, factory=Profile)

    def create_profile(self, name: str) -> Profile:
        uuid = self.new_uid()
        profile = self.factory(uuid=uuid, name=name)
        self.save_json_file(str(uuid), profile)
        return profile

    def find_profiles_by_name(self, name: str) -> Iterator[Profile]:
        for view in self.file_views:
            if view.resource.name == name:
                yield view.resource

    def find_profile_by_name(self, name: str) -> Profile:
        for profile in self.find_profiles_by_name(name):
            return profile
        else:
            raise ProfileNotFoundError()

    def find_profile_by_uuid(self, uuid: int) -> Profile:
        for view in self.file_views:
            if view.resource.uuid == uuid:
                return view.resource

        else:
            return self.load_json_file(str(uuid), Profile)
