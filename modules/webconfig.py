import ssl

class WebConfig:
    port = 80
    debug = True

    @classmethod
    def configure(cls, SETTINGS):
        cls.debug = SETTINGS["DEBUG"]
        cls.port = SETTINGS["PORT"]

    @staticmethod
    def get_port():
        return WebConfig.port
    
    @staticmethod
    def get_debug():
        return WebConfig.debug
