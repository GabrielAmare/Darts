from darts.core_games import AppGames
from darts.app_repository import app_repository
from darts.app_voice import app_voice
from darts.app_messages import app_messages
from darts.app_settings import app_settings

app_games = AppGames(
    root='darts/games/',
    app_repository=app_repository,
    app_voice=app_voice,
    app_messages=app_messages,
    app_settings=app_settings
)
