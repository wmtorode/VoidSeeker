import datetime

import discord

from ..data import Command, UserRole, ServerSettings
from ..model import AuthUser
from ..ui import StartSpamConfigView
from .basemodule import BaseModule



class AdminModule(BaseModule):

    addAdminCmd = BaseModule.CmdPrefix + "aAdmin"
    removeAdminCmd = BaseModule.CmdPrefix + "rAdmin"

    addServerOwnerCmd = BaseModule.CmdPrefix + "aSOwner"
    removeServerOwnerCmd = BaseModule.CmdPrefix + "rSOwner"

    addModeratorCmd = BaseModule.CmdPrefix + "aModerator"
    removeModeratorCmd = BaseModule.CmdPrefix + "rModerator"

    startAntiSpamConfigCmd = BaseModule.CmdPrefix + "sConfig"

    RoleRanks = {
        UserRole.ADMIN: 10,
        UserRole.MOD: 5,
        UserRole.SERVER_OWNER: 25
    }


    def registerCommands(self):
        return {
            self.addServerOwnerCmd: Command(self.addServerOwner, "Adds a server owner to the server", self.ownerAuth),
            self.removeServerOwnerCmd: Command(self.removeServerOwner, "Removes a server owner from the server", self.ownerAuth),
            self.addAdminCmd: Command(self.addAdmin, "Adds an admin to the server", self.adminAuth),
            self.removeAdminCmd: Command(self.removeAdmin, "Removes an admin from the server", self.adminAuth),
            self.addModeratorCmd: Command(self.addMod, "Adds a moderator to the server", self.adminAuth),
            self.removeModeratorCmd: Command(self.removeMod, "Removes a moderator from the server", self.adminAuth),
            self.startAntiSpamConfigCmd: Command(self.startAntiSpamConfig, "Starts the Anti-Spambot Configuration Wizard", self.adminAuth)
        }

    async def _promoteUserToRole(self, message: discord.Message, serverSettings: ServerSettings, role):
        self.startSqlEntry()
        self.ensureServerEntry(serverSettings)
        if len(message.mentions) == 0:
            await message.channel.send(f"Please mention a user to add as a {role}")
            return
        for mention in message.mentions:
            user = self.Session.query(AuthUser).filter(AuthUser.serverId == serverSettings.serverId,
                                                       AuthUser.userId == mention.id).first()  # type: AuthUser
            if user:
                if self.RoleRanks[user.role] < self.RoleRanks[role]:
                    await message.channel.send("User already has the requested or higher role")
                    self.Session.rollback()
                    return
                user.role = role
                user.updatedAt = datetime.datetime.now(datetime.UTC)
            else:
                user = AuthUser(serverId=serverSettings.serverId, userId=mention.id, role=role,
                                userName=mention.name)
                self.Session.add(user)
        self.Session.commit()
        self.voidseeker.rebuildServerSettings(serverSettings)
        await message.channel.send(f"Added {role}!")

    async def _removeUserFromRole(self, message: discord.Message, serverSettings: ServerSettings, role):
        self.startSqlEntry()
        if len(message.mentions) == 0:
            await message.channel.send("Please mention a user to remove from the requested role")
            return
        for mention in message.mentions:
            user = self.Session.query(AuthUser).filter(AuthUser.serverId == serverSettings.serverId,
                                                       AuthUser.userId == mention.id).first()  # type: AuthUser
            if user:
                if user.role == role:
                    self.Session.delete(user)
                else:
                    await message.channel.send(f"User is not a {role}")
                    return
            else:
                await message.channel.send(f"User is not a {role}")
                return
        self.Session.commit()
        self.voidseeker.rebuildServerSettings(serverSettings)
        await message.channel.send(f"removed {role}!")

    async def startAntiSpamConfig(self, message: discord.Message, serverSettings: ServerSettings):
        view = StartSpamConfigView(self.voidseeker, message.author.id, serverSettings)
        await message.channel.send("Starting Anti-Spambot Configurator", view=view)

    async def addServerOwner(self, message: discord.Message, serverSettings: ServerSettings):
        await self._promoteUserToRole(message, serverSettings, UserRole.SERVER_OWNER)

    async def removeServerOwner(self, message: discord.Message, serverSettings: ServerSettings):
        await self._removeUserFromRole(message, serverSettings, UserRole.SERVER_OWNER)

    async def addAdmin(self, message: discord.Message, serverSettings: ServerSettings):
        await self._promoteUserToRole(message, serverSettings, UserRole.ADMIN)

    async def removeAdmin(self, message: discord.Message, serverSettings: ServerSettings):
        await self._removeUserFromRole(message, serverSettings, UserRole.ADMIN)

    async def addMod(self, message: discord.Message, serverSettings: ServerSettings):
        await self._promoteUserToRole(message, serverSettings, UserRole.MOD)

    async def removeMod(self, message: discord.Message, serverSettings: ServerSettings):
        await self._removeUserFromRole(message, serverSettings, UserRole.MOD)