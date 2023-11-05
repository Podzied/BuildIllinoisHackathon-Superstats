import nextcord, os, json, asyncio, signal, threading
from nextcord.ext import commands

from database import dbclient
from utility import embed_sender
from superstats import task_gather_runner, pending_tasks, completed_tasks


bot = commands.Bot(
    command_prefix="oo!", 
    intents=nextcord.Intents.all()
)


# Globalize the database handler
database = dbclient.DatabaseHandler()


def refresh_watchdog(): bot.watchdog_channels = database.get_active_channels()
# Load the currently monitored channels into the watchdog
currently_monitored = database.get_active_channels()
bot.watchdog_channels = currently_monitored
bot.refresh_watchdog = refresh_watchdog


def refresh_guilds(): bot.watchdog_guilds = database.get_active_guilds()
currently_monitored_guilds = database.get_active_guilds()
bot.watchdog_guilds = currently_monitored_guilds
bot.refresh_guilds = refresh_guilds


async def keyword_resolver( search_value: str ) -> None:
	pending_search: dict = {"_id": search_value, "stage": 1}
	pending_tasks.append(pending_search)
	
	task_completed = False
	while task_completed == False:
		
		if not len(completed_tasks) == 0:
			for task in completed_tasks:
				if task["_id"] == search_value:
					task_completed = True
					completed_tasks.remove(task)
				else:
					pass
	
	return task


bot.send_channel_embed = embed_sender.send_channel_embed
bot.send_user_embed = embed_sender.send_user_embed
bot.embed_sender = embed_sender
bot.database = database


bot.tasks_list = pending_tasks
bot.completed_list = completed_tasks
bot.keyword_resolver = keyword_resolver


# Load all of the cogs to the main
if __name__ == "__main__":
    for cogfile in os.listdir("./cogs"):
        if cogfile.endswith(".py"):
            bot.load_extension(f"cogs.{cogfile[:-3]}")
            # Print out that the cogfile has been loaded
            print(f"[+] Cog {cogfile[:-3]} Loaded [+]")

with open("../database/config.json", "r") as json_file: 
    config_data = json.load(json_file)

bot.run(config_data['token'])