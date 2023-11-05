from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import nextcord



class AddChannel(commands.Cog):
    def __init__(self, bot: object) -> None:
        self.bot = bot
    

    @nextcord.slash_command(name="addchannel", description="Add channel to monitor")
    async def addchannel( self, interaction: nextcord.Interaction):
        pass


def setup(bot):
    bot.add_cog(AddChannel(bot))