from darts_v2 import ApplicationWrapper

if __name__ == '__main__':
    app = ApplicationWrapper(config_fp="assets/config.json")

    app.run()
