from darts.AppService import AppService
from darts.app_repository import app_repository
from darts.app_data import app_data

app_service = AppService(
    data=app_data,
    repository=app_repository,
)
