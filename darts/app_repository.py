from darts.base import AppRepository
from darts.app_settings import app_settings

app_repository = AppRepository(
    root=app_settings.games_fp
)
