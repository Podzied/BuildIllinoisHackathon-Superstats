from nextcord.ext import commands
import asyncio, nextcord


class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		while True:
			await self.bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Game(name="Searching Amazon."))
			await asyncio.sleep(1)
			await self.bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Game(name="Searching Amazon.."))
			await asyncio.sleep(1)
			await self.bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Game(name="Searching Amazon..."))
			await asyncio.sleep(1)
		

def setup(bot):
	bot.add_cog(Events(bot))