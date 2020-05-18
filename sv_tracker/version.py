
MAJOR_VERSION = 0
MINOR_VERSION = 4


class Version:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.major_version = MAJOR_VERSION
        self.minor_version = MINOR_VERSION

    def version_str(self):
        return 'v' + str(self.major_version) + '.' + str(self.minor_version)
