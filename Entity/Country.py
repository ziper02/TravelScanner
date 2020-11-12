class Country:
    """

    Attributes:
        name        The full name of country
        code        Shortcut name of country
    """
    __name: str
    __code: str

    def __init__(self, name: str = '', code: str = '', **json_text):
        if name != '':
            self.__name = name
            self.__code = code
        else:
            self.__dict__.update(json_text["dict"])

    @property
    def name(self) -> str:
        return self.__name

    @property
    def code(self) -> str:
        return self.__code

    def __eq__(self, other):
        if isinstance(other, Country):
            return self.code == other.name and self.code == other.name
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'Country:: name:  ' + self.name + ' code:  ' + self.code
