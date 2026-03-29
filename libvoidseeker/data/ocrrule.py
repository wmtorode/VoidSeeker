from .ocrgroup import OcrGroup


class OcrRule:

    def __init__(self):
        self.ruleName = ""
        self.groups = []  # type: List[OcrGroup]
        self.groupsMatchesNeeded = 0