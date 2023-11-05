from nextcord.ext import commands
import asyncio, nextcord, ast, re, threading, time

# from superstats import task_gather_runner, pending_tasks, completed_tasks
import amazon
from utility import upc_resolver



# def amazon_search_product_data( search_value: str ) -> None:
# 	pending_search: dict = {"_id": search_value, "stage": 1}
# 	pending_tasks.append(pending_search)
	
# 	task_completed = False
# 	while task_completed == False:
		
# 		if not len(completed_tasks) == 0:
# 			for task in completed_tasks:
# 				if task["_id"] == search_value:
# 					task_completed = True
# 					completed_tasks.remove(task)
# 				else:
# 					pass
	
# 	return task





def clean_embed(old_embed_data: dict) -> dict:
	"""Remove all the formatting from the previous embeds"""
	embed_data = str(old_embed_data).replace("`", "").replace("*", "")
	try:
		return_data = ast.literal_eval(embed_data)
	except Exception as e:
		print(f"having trouble converting to dict: {e}")
		return old_embed_data
	return return_data


def sanatize_value( value: str ) -> str:
	"""This method cleans the value that is being sent"""
	value = value.replace("_", "").replace("`", "").replace("*", "").replace("$", "").replace(">", "").replace(" ", "").replace("off", "").replace("~", "").replace("#", "")
	return value


def sort_clean_list(input_list):
	"""Regular expression to find all numbers in each string"""
	# Function to extract numbers from a string and convert to float
	def extract_number(s):
		character_list: list = list(str(s))
		print(character_list)
		for character in character_list:
			if not str(character) in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."] or character in ["~"]:
				character_list.remove(character)
		price_string = "".join(character_list)
		cleaned_price_string = sanatize_value(price_string)
		return float(cleaned_price_string)


	# Extract numbers from each string and convert to float
	numbers = [extract_number(item) for item in input_list]
	# Remove None values (strings without numbers) and sort the list
	sorted_numbers = sorted(filter(lambda x: x is not None, numbers))

	return sorted_numbers[0]


class Reaction(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	
	def traverse_fields(self, embed_data: dict) -> str:
		# Search the url if the url is amazon
		embed_url = embed_data.get("url")
		if not embed_url == None:
			embed_url = embed_url.lower()
			if "amazon" in embed_url and "dp" in embed_url:
				search_value = {"type": "asin", "value": "".join(list(embed_url.split("dp/")[1])[:10])}

			else: search_value = None
		else: search_value = None

		# Now we do field traversing to find the other IDs we can use
		if not embed_data.get("fields") == None: 
			# First we traverse for pricing
			embed_pricing_list: list = [ ]
			for field in embed_data['fields']:
				if "price" in field['name'].lower() or "$" in field['value']:
					embed_pricing_list.append(field['value'])

			# Now we traverse for possible searches
			for field in embed_data['fields']:
				if search_value == None:
					if "upc" in field['name'].lower():
						search_value = {"type": "upc", "value": field['value'].lower()}

					elif "asin" in field['name'].lower():
						search_value = {"type": "asin", "value": field['value'].lower()}
						
		print(embed_pricing_list)
		if not len(embed_pricing_list) == 0:
			# Test the function
			price_value: float = sort_clean_list(embed_pricing_list)
		else: price_value = None

		print(search_value)
		if not search_value == None:
			value = sanatize_value(search_value['value'])
			search_value['value'] = value
		return price_value, search_value
		


	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		print(payload.emoji.name)
		if str(payload.guild_id) in self.bot.watchdog_guilds and payload.emoji.name in ['🔍', '🔎']:
			guild_data = self.bot.database.get_guild_data(str(payload.guild_id))
			# Now that we have a valid guild, let's see if the plan on the server is valid
			if guild_data['active_reaction_plan'] == True:

				channel = self.bot.get_channel(payload.channel_id)
				message = await channel.fetch_message(payload.message_id)

				message_link = f"https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id}"

				if len(message.embeds) != 0:

					embed_data: dict = clean_embed(message.embeds[0].to_dict())
					price, search_value = self.traverse_fields(embed_data)

					user = await self.bot.fetch_user(payload.user_id)
					queue_message = await self.bot.embed_sender.send_user_added_queue(user, message_link)


					if not search_value == None:
						if search_value['type'] == "asin":
							product_data = await amazon.get_product_data(search_value['value'])
							print(product_data)
						
						elif search_value['type'] == "upc":
							asin = await upc_resolver.get_product_data(search_value['value'])
							print(asin)
							try:
								search_value = asin['Amazon ASIN:']
							except:
								search_value = None
								product_data = None
								await queue_message.delete()
								await self.bot.embed_sender.send_user_error(user, "No Amazon listings found")

							if not search_value == None:
								product_data = await amazon.get_product_data(search_value)
						
						else:
							print("some other random search key")


						if not product_data == None:
							print(f"Sending user product data to {user.name}")
							print(product_data)
							await self.bot.send_user_embed(user, product_data, price)
			

			else:
				print(f"Server {payload.guild_id} Does not have an active plan")


def setup(bot):
	bot.add_cog(Reaction(bot))
