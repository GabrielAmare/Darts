import os

from .AppData import AppData
from .AppEngines import AppEngines
from .AppGames import AppGames
from .AppImages import AppImages
from .AppLogger import AppLogger
from .AppMessages import AppMessages
from .AppSettings import AppSettings
from .AppStyles import AppStyles
from .AppVoice import AppVoice

__all__ = ['AppData', 'app_data']

app_data = AppData()
