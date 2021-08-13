from tkinter import *

STYLE = {
    'bg': {
        'primary': 'darkgreen',
        'secondary': 'black',
        'selected': 'lime'
    },
    'fg': {
        'primary': 'black',
        'secondary': 'white',
        'selected': 'black',
        'error': 'red',
        'warning': 'yellow',
        'success': 'lime',
    }
}


# STYLE = {
#     'bg': {
#         'primary': 'darkblue',
#         'secondary': 'black',
#         'selected': 'blue'
#     },
#     'fg': {
#         'primary': 'black',
#         'secondary': 'white',
#         'selected': 'black',
#         'error': 'red',
#         'warning': 'yellow',
#         'success': 'lime',
#     }
# }


class FONT:
    SM = ("Times", 15)
    MD = ("Times", 18)
    LG = ("Times", 20)
    XL = ("Times", 40)

    SM_OS = ("Times", 15, "overstrike")
    MD_OS = ("Times", 18, "overstrike")
    LG_OS = ("Times", 20, "overstrike")


STYLES = {
    'default': dict(bg='black'),

    'Main': dict(bg=STYLE['bg']['secondary']),
    'Main.holder': dict(bg=STYLE['bg']['secondary']),

    'VoiceInterfaceIcon': dict(bg=STYLE['bg']['secondary']),
    'TextFeedBack': dict(bg=STYLE['bg']['secondary']),
    'Main.quit_button': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], font=FONT.MD),

    'SettingsMenu': dict(bg=STYLE['bg']['secondary'], padx=8, pady=8),
    'CurrentParty': dict(bg=STYLE['bg']['secondary'], padx=8, pady=8),
    'GameSettings': dict(bg=STYLE['bg']['secondary'], padx=8, pady=8, bd=2, relief=RIDGE),
    'GameMenu': dict(bg=STYLE['bg']['secondary'], padx=8, pady=8),

    'Body': dict(bg=STYLE['bg']['secondary']),
    'Body.menu': dict(bg=STYLE['bg']['secondary']),
    'Body.menu.button': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], font=FONT.MD),
    'Body.menu.button:selected': dict(bg=STYLE['bg']['selected'], fg=STYLE['fg']['selected'], font=FONT.MD),

    'GameMenu.holder': dict(bg='blue'),

    'SelectLang': dict(bg=STYLE['bg']['secondary']),
    'SelectLang.label': dict(bg=STYLE['bg']['secondary'], fg=STYLE['fg']['secondary'], font=FONT.SM),
    'SelectLang.button': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], font=FONT.SM, padx=5),
    'SelectLang.button:selected': dict(bg=STYLE['bg']['selected'], fg=STYLE['fg']['selected'], font=FONT.SM, padx=5),

    'SelectPath': dict(bg=STYLE['bg']['secondary']),
    'SelectPath.title': dict(bg=STYLE['bg']['secondary'], fg=STYLE['fg']['secondary'], font=FONT.SM),
    'SelectPath.label': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['secondary'], font=FONT.SM, bd=2, relief=SUNKEN,
                             padx=4, pady=4),
    'SelectPath.button': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], font=FONT.SM, padx=5),

    'GameBadge': dict(bg=STYLE['bg']['primary'], padx=4, pady=4, bd=2, relief=RIDGE),
    'GameBadge.top': dict(bg=STYLE['bg']['primary']),
    'GameBadge.bot': dict(bg=STYLE['bg']['primary']),

    'GameBadge.name': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], padx=8, pady=8, font=FONT.LG),
    'GameBadge.description': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], padx=8, pady=0, font=FONT.SM,
                                  justify=LEFT, anchor=NW),

    'GameBadge.start': dict(bg=STYLE['bg']['primary'], padx=0, pady=0),
    'GameBadge.settings': dict(bg=STYLE['bg']['primary'], padx=0, pady=0),

    'TextFeedBack.NORMAL': dict(bg=STYLE['bg']['secondary'], fg=STYLE['fg']['secondary'], font=FONT.MD),
    'TextFeedBack.ERROR': dict(bg=STYLE['bg']['secondary'], fg=STYLE['fg']['error'], font=FONT.MD),
    'TextFeedBack.WARNING': dict(bg=STYLE['bg']['secondary'], fg=STYLE['fg']['warning'], font=FONT.MD),
    'TextFeedBack.SUCCESS': dict(bg=STYLE['bg']['secondary'], fg=STYLE['fg']['success'], font=FONT.MD),

    'GameSettings.label': dict(bg=STYLE['bg']['secondary'], fg=STYLE['fg']['secondary'], font=FONT.SM),
    'GameSettings.options': dict(bg=STYLE['bg']['secondary']),
    'GameSettings.options.button': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], font=FONT.SM, padx=5),
    'GameSettings.options.button:selected': dict(bg=STYLE['bg']['selected'], fg=STYLE['fg']['selected'], font=FONT.SM, padx=5),

    'DartResult': dict(bg=STYLE['bg']['secondary'], bd=2, relief=RIDGE, padx=4, pady=4),
    'DartResult.values': dict(bg=STYLE['bg']['secondary'], padx=4, pady=4),
    'DartResult.factors': dict(bg=STYLE['bg']['secondary'], padx=4, pady=4),

    'DartResult.button': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], font=FONT.MD),
    'DartResult.button:selected': dict(bg=STYLE['bg']['selected'], fg=STYLE['fg']['selected'], font=FONT.MD),

    'ScoreBoard': dict(bg=STYLE['bg']['secondary']),
    'ScoreBoardHandler.entry': dict(bg=STYLE['bg']['secondary'], fg=STYLE['fg']['secondary']),
}

PACK_STYLES = {
    'default': dict(),

    'Main': dict(side=TOP, fill=BOTH, expand=True),

    'GameMenu.holder': dict(side=TOP),

    'Body.menu': dict(side=TOP, fill=X),
    'Body.menu.button': dict(side=LEFT, fill=BOTH, expand=True, padx=4),

    'SelectLang': dict(side=TOP),
    'SelectLang.label': dict(side=LEFT, fill=Y),
    'SelectLang.button': dict(side=LEFT, padx=8),

    'SelectPath': dict(side=TOP),
    'SelectPath.title': dict(side=LEFT, fill=Y),
    'SelectPath.label': dict(side=LEFT, fill=Y, expand=True),
    'SelectPath.button': dict(side=LEFT, fill=Y),

    'GameBadge': dict(side=TOP, fill=X),

    'GameBadge.top': dict(side=TOP, fill=X),
    'GameBadge.bot': dict(side=TOP, fill=BOTH, expand=True),

    'GameBadge.name': dict(side=LEFT, fill=BOTH, expand=True),
    'GameBadge.description': dict(side=LEFT, fill=BOTH, expand=True),

    'GameBadge.start': dict(side=LEFT, anchor=CENTER, padx=0, pady=0),
    'GameBadge.settings': dict(side=LEFT, anchor=CENTER, padx=0, pady=0),

    'GameSettings': dict(side=TOP, anchor=N, pady=10),
    'GameSettings.options.button': dict(side=LEFT, fill=BOTH, expand=True),

    'CurrentParty': dict(side=TOP, fill=BOTH, expand=True),
    'ScoreBoard': dict(side=TOP, fill=BOTH, expand=True),
    'ScoreBoardHandler.entry': dict(side=TOP, fill=X)
}

STYLES_301 = {
    '301.PlayerBadge': dict(bg=STYLE['bg']['secondary'], bd=2, relief=RIDGE),
    '301.PlayerBadge:selected': dict(bg=STYLE['bg']['secondary'], bd=2, relief=RIDGE),
    '301.PlayerBadge.label': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], font=FONT.MD, bd=2,
                                  relief=RAISED),
    '301.PlayerBadge.label:selected': dict(bg=STYLE['bg']['selected'], font=FONT.MD),
    '301.PlayerBadge.score': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['secondary'], font=FONT.XL, padx=15, pady=15),
}

STYLES_RTC = {
    'RTC.PlayerBadge': dict(bg=STYLE['bg']['secondary'], bd=2, relief=RIDGE),
    'RTC.PlayerBadge:selected': dict(bg=STYLE['bg']['secondary'], bd=2, relief=RIDGE),
    'RTC.PlayerBadge.label': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], font=FONT.MD, bd=2,
                                  relief=RAISED),
    'RTC.PlayerBadge.label:selected': dict(bg=STYLE['bg']['selected'], font=FONT.MD),
    'RTC.PlayerBadge.score': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['secondary'], font=FONT.XL, padx=15, pady=15),
}
STYLES_TRAINING = {
    'TRAINING.PlayerBadge': dict(bg=STYLE['bg']['secondary'], bd=2, relief=RIDGE),
    'TRAINING.PlayerBadge:selected': dict(bg=STYLE['bg']['secondary'], bd=2, relief=RIDGE),
    'TRAINING.PlayerBadge.label': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['primary'], font=FONT.MD, bd=2,
                                  relief=RAISED),
    'TRAINING.PlayerBadge.label:selected': dict(bg=STYLE['bg']['selected'], font=FONT.MD),
    'TRAINING.PlayerBadge.score': dict(bg=STYLE['bg']['primary'], fg=STYLE['fg']['secondary'], font=FONT.XL, padx=15, pady=15),
}
STYLES_CRICKET = {
    'Cricket.ScoreBoard.DoorLabel': dict(
        bg=STYLE['bg']['secondary'],
        fg=STYLE['fg']['secondary'],
        font=FONT.LG,
        padx=10,
        pady=10,
        bd=2,
        relief=RIDGE
    ),
    'Cricket.ScoreBoard.DoorLabel:opened': dict(
        bg='#137307',
        fg=STYLE['fg']['primary'],
        font=FONT.LG,
        padx=10,
        pady=10,
        bd=2,
        relief=RIDGE
    ),
    'Cricket.ScoreBoard.DoorLabel:closed': dict(
        bg='#a82207',
        fg=STYLE['fg']['primary'],
        font=FONT.LG,
        padx=10,
        pady=10,
        bd=2,
        relief=RIDGE
    ),
    'Cricket.ScoreBoard.PlayerName': dict(
        bg=STYLE['bg']['primary'],
        fg=STYLE['fg']['primary'],
        font=FONT.MD,
        bd=2,
        relief=RAISED
    ),
    'Cricket.ScoreBoard.PlayerName:selected': dict(
        bg=STYLE['bg']['selected'],
        fg=STYLE['fg']['primary'],
        font=FONT.MD,
        bd=2,
        relief=RAISED
    ),

    'Cricket.ScoreBoard.PlayerTotal': dict(
        bg=STYLE['bg']['secondary'],
        fg=STYLE['fg']['secondary'],
        font=FONT.LG,
        padx=10,
        pady=10,
        bd=2,
        relief=RIDGE
    ),
    'Cricket.ScoreBoard.Player': dict(
        bg=STYLE['bg']['secondary'],
        fg=STYLE['fg']['secondary'],
        font=FONT.LG,
        padx=10,
        pady=10,
        bd=2,
        relief=RIDGE
    ),
    'Cricket.ScoreBoard.Player:opener': dict(
        bg='#137307',
        fg=STYLE['fg']['primary'],
        font=FONT.LG,
        padx=10,
        pady=10,
        bd=2,
        relief=RIDGE
    ),
    'Cricket.ScoreBoard.Player:opener-closed': dict(
        bg='#a82207',
        fg=STYLE['fg']['primary'],
        font=FONT.LG_OS,
        padx=10,
        pady=10,
        bd=2,
        relief=RIDGE
    ),
    'Cricket.ScoreBoard.Player:closed': dict(
        bg='#a82207',
        fg=STYLE['fg']['primary'],
        font=FONT.LG,
        padx=10,
        pady=10,
        bd=2,
        relief=RIDGE
    ),
}

STYLES.update(STYLES_301)
STYLES.update(STYLES_RTC)
STYLES.update(STYLES_CRICKET)
STYLES.update(STYLES_TRAINING)
