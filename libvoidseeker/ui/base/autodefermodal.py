from discord.ui import Modal
from discord import Interaction


class AutoDeferModal(Modal):

    def __init__(self, voidseeker, userId, data, title=None):
        super().__init__(timeout=600, title=title)
        self.voidseeker = voidseeker
        self.userId = userId
        self.data = data

    async def _scheduled_task(self, interaction: Interaction, components, resolved):
        try:
            self._refresh_timeout()
            self._refresh(interaction, components, resolved)

            allow = await self.interaction_check(interaction)
            if not allow:
                return

            await self.on_submit(interaction)
            if (not interaction.response.is_done() and not interaction.is_expired()):
                await interaction.response.defer()
        except Exception as e:
            return await self.on_error(interaction, e)
        else:
            # No error, so assume this will always happen
            # In the future, maybe this will require checking if we set an error response.
            self.stop()