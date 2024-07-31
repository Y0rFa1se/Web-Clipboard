class Auth:
    admin_password = ""
    passwords = set()

    @classmethod
    def configure(cls, SETTINGS):
        cls.admin_password = SETTINGS["ADMIN_PASSWORD"]
        for i in SETTINGS["PASSWORDS"]:
            cls.passwords.add(i)

    @staticmethod
    def is_admin(password):
        return password == Auth.admin_password
    
    @staticmethod
    def is_valid(password):
        return password in Auth.passwords