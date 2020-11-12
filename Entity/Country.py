class Country:
    """

    Attributes:
        name        The full name of country
        code        Shortcut name of country
    """
    __name: str
    __code: str

    def __init__(self, name: str = '', code: str = '', **json_text: dict):
        if name != '':
            self.__name = name
            self.__code = code
        else:
            try:
                json_text = json_text["dict"]
            except Exception:
                pass
            self.__code = str(json_text["code"])
            self.__name = str(json_text["name"])

    def to_json(self):
        """
        :return dictionary with all attributes
        :rtype: dict
        """
        return {
            "code": self.__code,
            "name": self.__name
        }

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
