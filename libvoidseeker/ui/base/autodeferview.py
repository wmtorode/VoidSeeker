from discord.ui import View, Item
from discord import Interaction

import time


class AutoDeferView(View):

    def __init__(self, voidseeker, userId, data):
        super().__init__(timeout=600)
        self.voidseeker = voidseeker
        self.userId = userId
        self.data = data

    async def _scheduled_task(self, item: Item, interaction: Interaction):
        try:
            item._refresh_state(interaction, interaction.data)  # type: ignore

            allow = await self.interaction_check(interaction)
            if not allow:
                return

            if self.timeout:
                self.__timeout_expiry = time.monotonic() + self.timeout

            await item.callback(interaction)
            if (not interaction.response.is_done() and not interaction.is_expired()):
                await interaction.response.defer()
        except Exception as e:
            return await self.on_error(interaction, e, item)