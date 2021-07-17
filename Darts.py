from darts.app_data import app_data

from darts.core_gui import App

if __name__ == '__main__':
    app_data.logger.info("creating session")
    app = App()
    app_data.logger.info("starting session")
    app.mainloop()
    app_data.logger.info("quitting session")
