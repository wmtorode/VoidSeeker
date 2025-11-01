import discord
import discord.ui
from discord.ui import ChannelSelect

from ...data import ServerSettings

from ..base import AutoDeferModal, BooleanSelect, CustomRoleSelect


class ImmuneRolesConfigModal(AutoDeferModal):

    def __init__(self, voidseeker, userId, data: ServerSettings):
        super().__init__(voidseeker, userId, data, title="Configure Role Immunity")


        selectedRoles = []
        guildRoles = voidseeker.get_guild(data.serverId).roles
        for role in guildRoles:
            if role.id in data.antiSpamImmuneRoles:
                selectedRoles.append(role)

        self.immuneRolesSelect = CustomRoleSelect(
            placeholder="Select Immune Roles",
            disabled=False,
            default_values=selectedRoles,
            min_values=0,
            max_values=25,
            required=False,
            row=1)


        self.immuneRolesSelectLabel = discord.ui.Label(text="Select Immune Roles", description="Select Roles to be immune from spam-bot detection rules", component=self.immuneRolesSelect)

        self.add_item(self.immuneRolesSelectLabel)

    async def on_submit(self, interaction: discord.Interaction):

        roleIds = []
        for role in self.immuneRolesSelect.values:
            roleIds.append(role.id)
        self.data.antiSpamImmuneRoles = roleIds

        self.stop()