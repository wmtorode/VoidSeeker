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

    def initSettings(self, serverSettingDb: ServerSetting, honeyPotChannel: HoneyPotChannel, authUsers: list, antiSpamImmuneRoles: list, banTerms: list):
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

        if honeyPotChannel:
            self.honeyPotChannelId = honeyPotChannel.channelId

        for user in authUsers: # type: AuthUser
            if user.role == UserRole.ADMIN:
                self.serverAdmins.append(user.userId)
            elif user.role == UserRole.MOD:
                self.serverModerators.append(user.userId)

        for role in antiSpamImmuneRoles: # type: ImmuneRole
            self.antiSpamImmuneRoles.append(role.roleId)

        for term in banTerms: # type: BanTerm
            if term.termType == TermType.URL:
                self.spamUrls.append(term.term)
            else:
                self.spamTerms.append(term.term)



