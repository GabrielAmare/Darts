from darts.base import AppMessages
from darts.app_settings import app_settings
from darts.app_logger import app_logger

app_messages = AppMessages(
    lang_ISO_639_1=app_settings.lang_ISO_639_1,
    logger=app_logger
)
