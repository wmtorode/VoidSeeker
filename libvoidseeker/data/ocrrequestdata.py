

class OCRData:

    def __init__(self):
        self.images = []
        self.results = []

    def toJson(self):
        return {
            'images': self.images,
            'results': self.results
        }

    def fromJson(self, json):
        self.images = json['images']
        self.results = json['results']
        return self