import discord
import discord.ui
from discord.ui import RoleSelect


class CustomRoleSelect(RoleSelect):

    def __init__(self, placeholder=None, min_values=1, max_values=1, disabled=False, required=True, row=None, default_values=None, viewCallback=None, userId=None):
        super().__init__(placeholder=placeholder,
                         min_values=min_values,
                         max_values=max_values,
                         disabled=disabled,
                         required=required,
                         row=row,
                         default_values=default_values)
        self.viewCallback = viewCallback
        self.userId = userId

    async def callbackInternal(self):
        if self.viewCallback:
            await self.viewCallback(self.values)

    async def callback(self, interaction: discord.Interaction):
        if self.userId:
            if self.userId == interaction.user.id:
                await self.callbackInternal()
        else:
            await self.callbackInternal()