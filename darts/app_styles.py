from darts.app_logger import app_logger
from darts.base import AppStyles
from darts.style_data import STYLES, PACK_STYLES

app_styles = AppStyles(
    config_styles=STYLES,
    pack_styles=PACK_STYLES,
    logger=app_logger
)
