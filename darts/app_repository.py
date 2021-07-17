from darts.base import AppRepository
from darts.app_data import app_data

app_repository = AppRepository(
    root=app_data.games_fp
)
