import os
import os.path
import logging
import logging.handlers
import traceback
import platform

import discord
import asyncio

from sqlalchemy.orm import sessionmaker

from libvoidseeker import *


def getIdList(stIds):
    ret = []
    if stIds is None:
        return ret
    ltIds = stIds.split(";")
    for sId in ltIds:
        try:
            iId = int(sId)
            ret.append(iId)
        except:
            pass
    return ret


INT_MAX_LOG_SIZE = 1024 * 1024 * 5  # ~5MB size
LOG_DIR = '/opt/voidseekerLog/'
STORE_DIR = '/opt/voidseekerStore/'
LOG_FILE = LOG_DIR + 'botlog.txt'

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.isdir(STORE_DIR):
    os.makedirs(STORE_DIR)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
obj_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=INT_MAX_LOG_SIZE, backupCount=5)
obj_handler.setLevel(logging.INFO)
obj_formatter = logging.Formatter('%(name)-18s %(levelname)-8s %(funcName)-25s %(asctime)-25s %(message)s')
obj_handler.setFormatter(obj_formatter)
LOGGER.addHandler(obj_handler)


TOKEN = os.getenv("DISCORD_BOT_SECRET")
OWNERS = getIdList(os.getenv("DISCORD_OWNING_USER_ID"))


class VoidSeeker(discord.Client):


    def __init__(self, logger):
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.message_content = True
        discord.Client.__init__(self, intents=intents)
        self.ownerIds = OWNERS
        self.logger = logger
        self.initComplete = False
        self.SessionMaker = sessionmaker()
        self.SessionMaker.configure(bind=ENGINE)
        self.Session = self.SessionMaker()
        self.CommandMap = {}
        self.baseModule = None
        self.statusModule = None
        self.adminModule = None
        self.modModule = None
        self.spamModule = None
        self.legacyModule = None
        self.settings = BotSettings()

        self.modules = []

    def initModulesAndCommands(self):

        self.baseModule = BaseModule(self.logger, self.settings, self.Session, self, STORE_DIR)

        self.initSettings()

        self.statusModule = StatusModule(self.logger, self.settings, self.Session, self, STORE_DIR)
        self.adminModule = AdminModule(self.logger, self.settings, self.Session, self, STORE_DIR)
        self.modModule = ModModule(self.logger, self.settings, self.Session, self, STORE_DIR)
        self.spamModule = SpamModule(self.logger, self.settings, self.Session, self, STORE_DIR)
        self.legacyModule = LegacyModule(self.logger, self.settings, self.Session, self, STORE_DIR)

        self.modules = [
            self.statusModule,
            self.adminModule,
            self.modModule,
            self.spamModule,
            self.legacyModule
        ]

        if self.baseModule.isInTestMode:
            testModule = TestModule(self.logger, self.settings, self.Session, self, STORE_DIR)
            self.modules.append(testModule)


        for module in self.modules:
            commands = module.registerCommands()
            self.CommandMap.update(commands)

        self.initComplete = True

    async def on_ready(self):
        msg = f'{self.user} has connected to Discord, using PY: {platform.python_version()}, DS: {discord.__version__}'
        self.logger.info(msg)
        print(msg)
        if not self.initComplete:
            self.initModulesAndCommands()
            await self.spamModule.initHoneyPots()

    async def on_member_remove(self, member: discord.Member):
        await self.adminModule.removeUserAuth(member.id, self.baseModule.getSettings(member.guild.id))

    def initSettings(self):
        self.baseModule.startSqlEntry()
        servers = self.Session.query(ServerSetting).all()
        for server in servers:
            settings = ServerSettings(server.serverId)
            self.rebuildServerSettings(settings)
            self.settings.serverSettings[server.serverId] = settings

    def rebuildServerSettings(self, serverSettings: ServerSettings):

        for guild in self.guilds:
            if serverSettings.serverId == guild.id:
                break
        else:
            self.logger.info(f"application is not part of guild: {serverSettings.serverId}")
            return

        self.baseModule.startSqlEntry()
        baseSettings = self.Session.query(ServerSetting).filter(ServerSetting.serverId == serverSettings.serverId).first()
        honeyPotChannel = self.Session.query(HoneyPotChannel).filter(HoneyPotChannel.serverId == serverSettings.serverId).first()
        authUsers = self.Session.query(AuthUser).filter(AuthUser.serverId == serverSettings.serverId).all()
        antiSpamImmuneRoles = self.Session.query(ImmuneRole).filter(ImmuneRole.serverId == serverSettings.serverId).all()
        banTerms = self.Session.query(BanTerm).filter(BanTerm.serverId == serverSettings.serverId).all()

        roles = self.get_guild(baseSettings.serverId).roles

        serverSettings.initSettings(baseSettings, honeyPotChannel, authUsers, antiSpamImmuneRoles, banTerms, roles)

    async def on_message(self, message:discord.Message):
        if not self.initComplete:
            self.logger.info("Bot not yet ready to handle messages")
            return

        try:
            if message.author == self.user:
                return
            if await self.spamModule.checkIfSpambot(message):
                return
            for user in message.mentions: # type: discord.abc.User
                if user.mention == self.user.mention:
                    await message.channel.trigger_typing()
                    await message.channel.send("VoidSeeker Mk. 39 online")
                    return

            cmd = None
            try:
                cmd = message.content.split()[0]
            except:
                pass
            if cmd:
                if cmd in self.CommandMap:
                    botCommand = self.CommandMap[cmd]
                    await botCommand.runCommand(message, self.baseModule.getSettings(message.guild.id))

        except:
            trace = traceback.format_exc()
            lst_trace = trace.split('\n')
            for line in lst_trace:
                self.logger.critical(line)
            if TEST_MODE.lower() == "yes":
                print(trace)

client = VoidSeeker(LOGGER)
client.run(TOKEN)
