# import darts.base
# import darts.base_actions
# import darts.base_commands
# import darts.base_engines
# import darts.base_events
# import darts.base_games
# import darts.base_gui
# import darts.core_actions
# import darts.core_commands
# import darts.core_games
# import darts.core_gui

from darts.app_data import app_data

from darts.core_gui import App

if __name__ == '__main__':
    app_data.logger.info("creating session")
    app = App()
    app_data.logger.info("starting session")
    app.mainloop()
    app_data.logger.info("quitting session")
