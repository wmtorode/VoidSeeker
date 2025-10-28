class CommandAuth:

    def __init__(self, owners, restrict, allowAdmins, allowMods):
        self.owners = owners
        self.restrict = restrict
        self.allowAdmins = allowAdmins
        self.allowMods = allowMods

    def canRun(self, author, serverSettings) -> bool:
        if self.restrict:
            try:
                if author.id in self.owners:
                    return True
                if self.allowAdmins and author.id in serverSettings.serverAdmins:
                    return True
                if self.allowMods and author.id in serverSettings.serverModerators:
                    return True
            except:
                pass
            return False
        return True