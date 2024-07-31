import ssl

class WebConfig:
    port = 80
    ssl_enabled = False
    cert_path = ""
    key_path = ""

    @classmethod
    def configure(cls, SETTINGS):
        cls.port = SETTINGS["PORT"]
        cls.ssl_enabled = SETTINGS["SSL"]["ENABLED"]
        cls.cert_path = SETTINGS["SSL"]["CERT_PATH"]
        cls.key_path = SETTINGS["SSL"]["KEY_PATH"]

    @staticmethod
    def ssl():
        if (WebConfig.ssl_enabled):
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.load_cert_chain(
                WebConfig.cert_path,
                WebConfig.key_path
            )

            return context

        return "adhoc"
    
    @staticmethod
    def get_port():
        return WebConfig.port