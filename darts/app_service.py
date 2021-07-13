from darts.AppService import AppService
from darts.app_engines import app_engines
from darts.app_games import app_games
from darts.app_images import app_images
from darts.app_logger import app_logger
from darts.app_messages import app_messages
from darts.app_repository import app_repository
from darts.app_settings import app_settings
from darts.app_styles import app_styles
from darts.app_voice import app_voice

app_service = AppService(
    settings=app_settings,
    logger=app_logger,
    styles=app_styles,
    images=app_images,
    messages=app_messages,
    voice=app_voice,
    repository=app_repository,
    games=app_games,
    engines=app_engines,
)
