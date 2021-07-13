from tkinter import Frame
from typing import Dict

from .SettingOption import SettingOption
from . import Config


class Settings(Frame):
    def __init__(self, root, cfg: Config):
        super().__init__(root)
        self.cfg = cfg

        self.fields: Dict[str, SettingOption] = {}
        default_score = IntOption(
            'default_score',
            {
                '301': dict(text='301'),
                '501': dict(text='501'),
                '801': dict(text='801'),
            },
            '301'
        )

        self.default_score = SettingOption(
            self,
            game_uid='301',
            key='default_score',
            options={
                '301': dict(text='301'),
                '501': dict(text='501'),
                '801': dict(text='801'),
            },
            default_option=str(cfg.default_score),
            parse_key={'301': 301, '501': 501, '801': 801}.__getitem__
        )
        self.double_in = SettingOption(
            self,
            game_uid='301',
            key='double_in',
            options={
                'True': dict(code='APP.YES'),
                'False': dict(code='APP.NO'),
            },
            default_option=str(cfg.double_in),
            parse_key={'True': True, 'False': False}.__getitem__
        )
        self.double_out = SettingOption(
            self,
            game_uid='301',
            key='double_out',
            options={
                'True': dict(code='APP.YES'),
                'False': dict(code='APP.NO'),
            },
            default_option=str(cfg.double_out),
            parse_key={'True': True, 'False': False}.__getitem__
        )
        self.default_score.pack(side="top", fill="x")
        self.double_in.pack(side="top", fill="x")
        self.double_out.pack(side="top", fill="x")
