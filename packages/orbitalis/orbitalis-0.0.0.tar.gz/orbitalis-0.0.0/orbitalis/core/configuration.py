

class CoreConfiguration:

    def __init__(self, needed_plugins: list[str] | None = None):

        self.__needed_plugins = needed_plugins

    @property
    def needed_plugins(self) -> list[str] | None:
        return self.__needed_plugins