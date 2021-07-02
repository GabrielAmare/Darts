from tools import Config


class AppConfig(Config):
    ALLOW_OVERWRITE = True

    def __init__(self, config):
        default = {

        }
        default.update(config)
        super().__init__(default)
