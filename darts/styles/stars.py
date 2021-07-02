class COLORS:
    class BG:
        MAIN = "#080843"
        ACTIVE = "#2020d0"
        ENABLED = "#1e1e99"
        DISABLED = "#50507d"

    class FG:
        MAIN = "#908a0a"
        ACTIVE = "#fff300"
        ENABLED = "#bdb619"
        DISABLED = "#979453"

        ERROR = "red"
        WARNING = "yellow"
        SUCCESS = "lime"


class PAD:
    P2 = dict(padx=2, pady=2)
    P15 = dict(padx=15, pady=15)
    P20 = dict(padx=20, pady=20)
    P10_5 = dict(padx=10, pady=5)
    P40_8 = dict(padx=40, pady=8)
    P76_20 = dict(padx=76, pady=20)


class FONT:
    SM = dict(font=("Times", 15))
    MD = dict(font=("Times", 18))
    LG = dict(font=("Times", 20))

    SM_OS = dict(font=("Times", 15, "overstrike"))
    MD_OS = dict(font=("Times", 18, "overstrike"))
    LG_OS = dict(font=("Times", 20, "overstrike"))


class CONTRAST:
    MAIN = dict(bg=COLORS.BG.MAIN, fg=COLORS.FG.MAIN)

    ERROR = dict(bg=COLORS.BG.MAIN, fg=COLORS.FG.ERROR)
    WARNING = dict(bg=COLORS.BG.MAIN, fg=COLORS.FG.WARNING)
    SUCCESS = dict(bg=COLORS.BG.MAIN, fg=COLORS.FG.SUCCESS)

    ENABLED = dict(bg=COLORS.BG.ENABLED, fg=COLORS.FG.ENABLED)
    DISABLED = dict(bg=COLORS.BG.DISABLED, disabledforeground=COLORS.FG.DISABLED)
    ACTIVE = dict(bg=COLORS.BG.ACTIVE, disabledforeground=COLORS.FG.ACTIVE)


class RELIEF:
    NULL = dict(bd=0, relief=None)
    Ri2 = dict(bd=2, relief="ridge")
    Ri1 = dict(bd=1, relief="ridge")
    Su2 = dict(bd=2, relief="sunken")
    Su4 = dict(bd=4, relief="sunken")
    Fl2 = dict(bd=2, relief="flat")
    Ra2 = dict(bd=2, relief="raised")


class STYLE:
    class APP_HEADER:
        CFG = dict(
            bg=COLORS.BG.MAIN,
            **RELIEF.NULL
        )

        BTN_CFG = dict(
            width=15,
            **RELIEF.Ri1,
            **CONTRAST.ENABLED,
            **FONT.MD,
            **PAD.P2
        )
        LBL_CFG = dict(
            **CONTRAST.MAIN,
            **FONT.MD,
            **PAD.P10_5
        )
        ICN_CFG = dict(
            bg=COLORS.BG.MAIN, **RELIEF.NULL
        )

    class APP_INTERFACE:
        FRAME = dict(bg=COLORS.BG.MAIN, **RELIEF.NULL)

        CFG = dict(
            **FRAME,
            **PAD.P20
        )

        TAB = dict(
            **FONT.MD,
            **PAD.P2
        )

        TAB_ACTIVE = dict(
            **CONTRAST.ACTIVE,
            **RELIEF.Fl2,
            **TAB
        )
        TAB_ENABLED = dict(
            **CONTRAST.ENABLED,
            **RELIEF.Ra2,
            **TAB
        )
        TAB_DISABLED = dict(
            **CONTRAST.DISABLED,
            **RELIEF.Ri2,
            **TAB
        )

        TAB_BODY = dict(bg=COLORS.BG.MAIN, **RELIEF.Su4)

        class TEXT:
            NORMAL = CONTRAST.MAIN
            ERROR = CONTRAST.ERROR
            WARNING = CONTRAST.WARNING
            SUCCESS = CONTRAST.SUCCESS

    class MAIN_MENU:
        BTN_CFG = dict(
            width=30,
            **RELIEF.Ri2,
            **CONTRAST.ENABLED,
            **FONT.LG,
            **PAD.P15
        )

    class SETTINGS_MENU:
        LBL_CFG = dict(
            **CONTRAST.ENABLED,
            **FONT.SM,
            **PAD.P10_5,
            **RELIEF.Fl2
        )

        ENT_CFG = dict(
            **CONTRAST.ACTIVE,
            **FONT.SM,
            **PAD.P10_5,
            **RELIEF.Ra2
        )

        KEYVAL_CFG = dict(
            bg=COLORS.BG.MAIN
        )

    class PARTY_HANDLER:
        SCOREBOARD = dict(
            bg=COLORS.BG.MAIN
        )

    class SCOREBOARD:
        LABEL = dict(
            bg=COLORS.BG.MAIN,
            fg=COLORS.FG.MAIN,
            **RELIEF.Ri1,
            **FONT.SM,
            **PAD.P40_8
        )

        ACTIVE_PLAYER = dict(
            bg=COLORS.BG.ACTIVE,
            fg=COLORS.FG.ACTIVE,
            **FONT.LG
        )

        LABEL_LG = dict(
            bg=COLORS.BG.MAIN,
            fg=COLORS.FG.MAIN,
            **RELIEF.Ri1,
            **PAD.P76_20,
            **FONT.LG
        )

        class CRICKET:
            DOOR_OPEN = dict(bg="#064001")
            DOOR_CLOSED = dict(bg="#8a0b00")

            DISABLED = dict(
                fg=COLORS.FG.DISABLED,
                **FONT.MD_OS
            )

        class MOLKKY:
            LABEL = dict(
                **FONT.SM,
                bg=COLORS.BG.MAIN,
                fg=COLORS.FG.MAIN,
                **PAD.P40_8,
                **RELIEF.Ri1
            )
