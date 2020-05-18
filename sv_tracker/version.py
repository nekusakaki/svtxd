
CURRENT_VERSION = '0.4'


class Version:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.major_version = 0
        self.minor_version = 0

        self.parse_version()

    def parse_version(self):
        version_split = CURRENT_VERSION.split('.')
        self.major_version = int(version_split[0])
        self.minor_version = int(version_split[1])

    def version_str(self):
        return 'v' + str(self.major_version) + '.' + str(self.minor_version)
