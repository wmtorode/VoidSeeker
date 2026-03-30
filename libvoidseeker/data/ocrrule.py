from .ocrgroup import OcrGroup


class OcrRule:

    def __init__(self):
        self.ruleName = ""
        self.groups = []  # type: List[OcrGroup]
        self.groupsMatchesNeeded = 0

    def toJson(self):
        groupsJson = []
        for group in self.groups:
            groupsJson.append(group.toJson())
        return {
            'ruleName': self.ruleName,
            'groups': groupsJson,
            'groupsMatchesNeeded': self.groupsMatchesNeeded
        }

    def fromJson(self, json):

        self.groups = []
        for groupJson in json['groups']:
            group = OcrGroup()
            group.fromJson(groupJson)
            self.groups.append(group)

        self.ruleName = json['ruleName']
        self.groupsMatchesNeeded = json['groupsMatchesNeeded']
        return self

    def check(self, text):
        groupMatches = 0
        for group in self.groups:
            if group.check(text):
                groupMatches += 1

        # when zero all groups must be a match
        if self.groupsMatchesNeeded == 0:
            return groupMatches == len(self.groups)

        return groupMatches >= self.groupsMatchesNeeded
