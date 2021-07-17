from darts.__meta__ import ENV
from .AppData import AppData
from .AppEngines import AppEngines
from .AppImages import AppImages
from .AppLogger import AppLogger
from .AppMessages import AppMessages
from .AppSettings import AppSettings
from .AppStyles import AppStyles
from .AppVoice import AppVoice
from .GameManager import GameManager

__all__ = ['AppData', 'app_data']

app_data = AppData(name={'PROD': 'Darts', 'DEV': 'DartsTests'}[ENV])
