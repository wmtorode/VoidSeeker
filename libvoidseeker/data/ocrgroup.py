

class OcrGroup:

    def __init__(self):
        self.groupName = ""
        self.allOf = []
        self.anyOf = []
        self.noneOf = []

    def toJson(self):
        return {
            'allOf': self.allOf,
            'anyOf': self.anyOf,
            'noneOf': self.noneOf,
            'groupName': self.groupName
        }

    def fromJson(self, json):
        self.allOf = json['allOf']
        self.anyOf = json['anyOf']
        self.noneOf = json['noneOf']
        self.groupName = json['groupName']

    def _checkAllOf(self, text):
        result = True
        for pattern in self.allOf:
            if pattern not in text:
                result = False
                break
        return result

    def _checkAnyOf(self, text):
        for pattern in self.anyOf:
            if pattern in text:
                return True
        return False

    def _checkNoneOf(self, text):
        for pattern in self.noneOf:
            if pattern in text:
                return False
        return True

    def check(self, text):
        return self._checkAllOf(text) and self._checkAnyOf(text) and self._checkNoneOf(text)