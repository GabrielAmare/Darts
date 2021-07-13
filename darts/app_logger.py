from darts.base import AppLogger
from darts.app_settings import app_settings

app_logger = AppLogger(fp=app_settings.log_fp)
