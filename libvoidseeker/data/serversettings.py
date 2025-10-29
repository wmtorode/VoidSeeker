import discord

from ..model import *
from .enums import TermType, UserRole


class ServerSettings:

    def __init__(self, serverId=None):
        self.serverId = serverId
        self.serverAdmins = []
        self.serverModerators = []
        self.honeyPotChannelEnabled = False
        self.honeyPotChannelId = 0
        self.honeyPotChannelText = ""
        self.antiSpamImmuneRoles = []

        self.antiSpamHeuristicsEnabled = False
        self.spamTerms = []
        self.spamUrls = []
        self.banOnPingAll = False

        self._adminNames = []
        self._modNames = []
        self._roleNames = []

    def initSettings(self, serverSettingDb: ServerSetting, honeyPotChannel: HoneyPotChannel, authUsers: list, antiSpamImmuneRoles: list, banTerms: list, roles: list):
        self.honeyPotChannelEnabled = serverSettingDb.honeyPotEnabled
        self.honeyPotChannelText = serverSettingDb.honeyPotText
        self.antiSpamHeuristicsEnabled = serverSettingDb.heuristicsEnabled
        self.banOnPingAll = serverSettingDb.banOnPingAll

        self.honeyPotChannelId = 0
        self.serverAdmins.clear()
        self.serverModerators.clear()
        self.antiSpamImmuneRoles.clear()
        self.spamTerms.clear()
        self.spamUrls.clear()
        self._adminNames.clear()
        self._modNames.clear()
        self._roleNames.clear()

        if honeyPotChannel:
            self.honeyPotChannelId = honeyPotChannel.channelId

        for user in authUsers: # type: AuthUser
            if user.role == UserRole.ADMIN or user.role == UserRole.SERVER_OWNER:
                self.serverAdmins.append(user.userId)
                self._adminNames.append(user.userName)
            elif user.role == UserRole.MOD:
                self.serverModerators.append(user.userId)
                self._modNames.append(user.userName)

        for role in antiSpamImmuneRoles: # type: ImmuneRole
            self.antiSpamImmuneRoles.append(role.roleId)
            for discordRole in roles:  # type: discord.Role
                if discordRole.id == role.roleId:
                    self._roleNames.append(discordRole.name)

        for term in banTerms: # type: BanTerm
            if term.termType == TermType.URL:
                self.spamUrls.append(term.term)
            else:
                self.spamTerms.append(term.term)

    def _renderList(self, prop):
        if len(prop) == 1:
            return prop[0]
        stMsg = ''
        for item in prop:
            stMsg += f'- {item}\n'
        return stMsg

    @property
    def adminList(self):
        return self._renderList(self._adminNames)

    @property
    def modList(self):
        return self._renderList(self._modNames)

    @property
    def antiSpamImmuneList(self):
        return self._renderList(self._roleNames)

    @property
    def spamTermList(self):
        return self._renderList(self.spamTerms)

    @property
    def spamUrlList(self):
        return self._renderList(self.spamUrls)



