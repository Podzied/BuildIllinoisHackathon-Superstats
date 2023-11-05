from nextcord.ext import commands
import asyncio, ast

import amazon
from utility import upc_resolver

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
	value = value.replace("_", "").replace("`", "").replace("*", "").replace("$", "").replace(">", "").replace(" ", "")
	return value



class OnMessage(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):		
		if str(message.channel.id) in self.bot.watchdog_channels:

			channel_data: dict = self.bot.database.get_channel_data(str(message.channel.id))

			if channel_data['type'] == "embed":
				if not len(message.embeds) == 0:

					embed_data: dict = clean_embed(message.embeds[0].to_dict())

					pricing_field: str = channel_data['pricing_field']
					search_field_one: str = channel_data['search_field_one']
					

					for field in embed_data['fields']: 
						if pricing_field in str(field['name']).lower():
							pricing_value = field['value']
							break
						else: pricing_value = None

					if not search_field_one in ["title", "url"]:
						for field in embed_data['fields']:
							if search_field_one in str(field['name']).lower():
								search_value = sanatize_value(field['value'])
								
								break
							else: search_value = None
					else:
						if search_field_one == "title":
							search_value = " ".join(embed_data['title'].split(" ")[:5])

						elif search_field_one == "url":
							embeded_url = embed_data['url'].lower()
							if "amazon" in embeded_url and "dp" in embeded_url:
								search_value = "".join(list(embeded_url.split("dp/")[1])[:10])
							else:
								search_value = None
					
					if "upc" in search_field_one:
						#asin = await upc_resolver.get_product_data(search_value)
						asin = None

						if not asin == None:
							search_value = asin['Amazon ASIN']

					elif "title" in search_field_one:
						self.bot.keyword_resolver(search_value)
					
					# After getting the pricing and the search, run it through selleramp stats
					if not pricing_value == None and not search_value == None:
						pricing_value: float = float(sanatize_value(pricing_value))
						product_data = await profitguru.get_product_data(search_value)

						if not product_data == None:
							await self.bot.send_channel_embed(message, product_data) 




def setup(bot):
	bot.add_cog(OnMessage(bot))
