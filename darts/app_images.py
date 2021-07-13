from darts.base import AppImages
from darts.app_settings import app_settings
from darts.app_logger import app_logger

app_images = AppImages(
    root=app_settings.images_fp,
    logger=app_logger
)
