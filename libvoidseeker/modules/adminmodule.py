import datetime

import discord

from ..data import Command, UserRole, ServerSettings
from ..model import AuthUser
from .basemodule import BaseModule



class AdminModule(BaseModule):

    addAdminCmd = BaseModule.CmdPrefix + "addAdmin"
    removeAdminCmd = BaseModule.CmdPrefix + "removeAdmin"

    addServerOwnerCmd = BaseModule.CmdPrefix + "addSOwner"
    removeServerOwnerCmd = BaseModule.CmdPrefix + "removeSOwner"

    addModeratorCmd = BaseModule.CmdPrefix + "addModerator"
    removeModeratorCmd = BaseModule.CmdPrefix + "removeModerator"

    def registerCommands(self):
        return {
            self.addServerOwnerCmd: Command(self.addServerOwner, "Adds a server owner to the server", self.ownerAuth),
            self.removeServerOwnerCmd: Command(self.removeServerOwner, "Removes a server owner from the server", self.ownerAuth),
            self.addAdminCmd: Command(self.addAdmin, "Adds an admin to the server", self.adminAuth),
            self.removeAdminCmd: Command(self.removeAdmin, "Removes an admin from the server", self.adminAuth),
            self.addModeratorCmd: Command(self.addMod, "Adds a moderator to the server", self.adminAuth),
            self.removeModeratorCmd: Command(self.removeMod, "Removes a moderator from the server", self.adminAuth)
        }

    async def addServerOwner(self, message: discord.Message, serverSettings: ServerSettings):
        self.startSqlEntry()
        self.ensureServerEntry(serverSettings)
        if len(message.mentions) == 0:
            await message.channel.send("Please mention a user to add as a server owner")
            return
        for mention in message.mentions:
            user = self.Session.query(AuthUser).filter(AuthUser.serverId == serverSettings.serverId,
                                                       AuthUser.userId == mention.id).first()  # type: AuthUser
            if user:
                if user.role == UserRole.SERVER_OWNER:
                    await message.channel.send("User is already a server owner")
                    return
                user.role = UserRole.SERVER_OWNER
                user.updatedAt = datetime.datetime.now(datetime.UTC)
            else:
                user = AuthUser(serverId=serverSettings.serverId, userId=mention.id, role=UserRole.SERVER_OWNER,
                                userName=mention.name)
                self.Session.add(user)
        self.Session.commit()
        self.voidseeker.rebuildServerSettings(serverSettings)
        await message.channel.send("Added server owner!")

    async def removeServerOwner(self, message: discord.Message, serverSettings: ServerSettings):
        self.startSqlEntry()
        if len(message.mentions) == 0:
            await message.channel.send("Please mention a user to remove as an server owner")
            return
        for mention in message.mentions:
            user = self.Session.query(AuthUser).filter(AuthUser.serverId == serverSettings.serverId,
                                                       AuthUser.userId == mention.id).first()  # type: AuthUser
            if user:
                if user.role == UserRole.SERVER_OWNER:
                    self.Session.delete(user)
                else:
                    await message.channel.send("User is not a server owner")
                    return
            else:
                await message.channel.send("User is not a server owner")
                return
        self.Session.commit()
        self.voidseeker.rebuildServerSettings(serverSettings)
        await message.channel.send("removed server owner!")

    async def addAdmin(self, message: discord.Message, serverSettings: ServerSettings):
        self.startSqlEntry()
        self.ensureServerEntry(serverSettings)
        if len(message.mentions) == 0:
            await message.channel.send("Please mention a user to add as an admin")
            return
        for mention in message.mentions:
            user = self.Session.query(AuthUser).filter(AuthUser.serverId == serverSettings.serverId, AuthUser.userId == mention.id).first() # type: AuthUser
            if user:
                if user.role == UserRole.ADMIN or user.role == UserRole.SERVER_OWNER:
                    await message.channel.send("User is already an admin")
                    return
                user.role = UserRole.ADMIN
                user.updatedAt = datetime.datetime.now(datetime.UTC)
            else:
                user = AuthUser(serverId=serverSettings.serverId, userId=mention.id, role=UserRole.ADMIN, userName=mention.name)
                self.Session.add(user)
        self.Session.commit()
        self.voidseeker.rebuildServerSettings(serverSettings)
        await message.channel.send("Added admin!")

    async def removeAdmin(self, message: discord.Message, serverSettings: ServerSettings):
        self.startSqlEntry()
        if len(message.mentions) == 0:
            await message.channel.send("Please mention a user to remove as an admin")
            return
        for mention in message.mentions:
            user = self.Session.query(AuthUser).filter(AuthUser.serverId == serverSettings.serverId, AuthUser.userId == mention.id).first() # type: AuthUser
            if user:
                if user.role == UserRole.ADMIN:
                    self.Session.delete(user)
                else:
                    await message.channel.send("User is not an admin")
                    return
            else:
                await message.channel.send("User is not an admin")
                return
        self.Session.commit()
        self.voidseeker.rebuildServerSettings(serverSettings)
        await message.channel.send("removed admin!")

    async def addMod(self, message: discord.Message, serverSettings: ServerSettings):
        self.startSqlEntry()
        self.ensureServerEntry(serverSettings)
        if len(message.mentions) == 0:
            await message.channel.send("Please mention a user to add as an moderator")
            return
        for mention in message.mentions:
            user = self.Session.query(AuthUser).filter(AuthUser.serverId == serverSettings.serverId,
                                                       AuthUser.userId == mention.id).first()  # type: AuthUser
            if user:
                if user.role == UserRole.ADMIN or user.role == UserRole.SERVER_OWNER:
                    await message.channel.send("User is an admin")
                    return
                elif user.role == UserRole.MOD:
                    await message.channel.send("User is already a moderator")
            else:
                user = AuthUser(serverId=serverSettings.serverId, userId=mention.id, role=UserRole.MOD,
                                userName=mention.name)
                self.Session.add(user)
        self.Session.commit()
        self.voidseeker.rebuildServerSettings(serverSettings)
        await message.channel.send("Added moderator!")

    async def removeMod(self, message: discord.Message, serverSettings: ServerSettings):
        self.startSqlEntry()
        if len(message.mentions) == 0:
            await message.channel.send("Please mention a user to remove as an moderator")
            return
        for mention in message.mentions:
            user = self.Session.query(AuthUser).filter(AuthUser.serverId == serverSettings.serverId,
                                                       AuthUser.userId == mention.id).first()  # type: AuthUser
            if user:
                if user.role == UserRole.MOD:
                    self.Session.delete(user)
                else:
                    await message.channel.send("User is not an moderator")
                    return
            else:
                await message.channel.send("User is not an moderator")
                return
        self.Session.commit()
        self.voidseeker.rebuildServerSettings(serverSettings)
        await message.channel.send("removed moderator!")