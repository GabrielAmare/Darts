from darts.app_logger import app_logger
from darts.app_settings import app_settings
from darts.base import AppEngines
from darts.base_engines import fr, en

app_engines = AppEngines(
    engines={
        'fr': fr.engine,
        'en': en.engine
    },
    lang_ISO_639_1=app_settings.lang_ISO_639_1,
    logger=app_logger
)
