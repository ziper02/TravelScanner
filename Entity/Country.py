

class Country:
    def __init__(self,name='',code='',**dict):
         if name!='':
             self._name=name
             self._code=code
         else:
             self.__dict__.update(dict["dict"])



    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    def __eq__(self, other):
        if isinstance(other,Country):
            return self.code==other.name and self.code==other.name
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'Country:: name: '+self.name+' code: '+self.code