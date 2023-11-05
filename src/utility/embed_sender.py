import nextcord

def calculate_roi( price, total_fees ) -> float:
    pass

async def send_channel_embed(message: object, information: dict) -> None:
    print("s")
    
    # embed = nextcord.Embed(title=f"Found Amazon Stats for: {information['asin']}", color=0xF33006, url=f"https://amazon.com/dp/{information['asin']}")
    # embed.add_field(name="Sales Per Month", value=str(information['sales_per_month']))
    # embed.add_field(name="Sales Rank (90d)", value=str(information['90_day_rank']['3']))
    # embed.add_field(name="BSR Drop", value=str(information['90_day_rank']['bsr_drops']))
    # embed.add_field(name="Private Label", value=str(information['private_label']), inline=False)
    # embed.add_field(name="IP Issues", value=str(information['ip_issues']), inline=False)
    # embed.set_footer(icon_url="https://media.discordapp.net/attachments/1084360785431646218/1137276593585279086/SuperStats.jpg", text="Powered By SuperStats™️")
    # await message.reply(embed=embed)


def calculate_roi(buy_price, sale_price):
    if buy_price <= 0:
        buy_price = 0.01
        
    
    roi = ((sale_price - buy_price) / buy_price) * 100
    return round(roi)



# async def send_user_embed( user: object, information: dict ) -> None:



#     embed = nextcord.Embed(title=f"Found Amazon Stats for: {information['asin']}", color=0xF33006, url=f"https://amazon.com/dp/{information['asin']}")
#     embed.add_field(name="Sales Per Month", value=str(information['sales_per_month']))
#     embed.add_field(name="Sales Rank (90d)", value=str(information['90_day_rank']['3']))
#     embed.add_field(name="BSR Drop", value=str(information['90_day_rank']['bsr_drops']))
#     embed.add_field(name="Private Label", value=str(information['private_label']), inline=False)
#     embed.add_field(name="IP Issues", value=str(information['ip_issues']), inline=False)

#     # if not price == None and not information['total_fees'] == None:
#     #     roi_percentage = 

#     embed.set_footer(icon_url="https://media.discordapp.net/attachments/1084360785431646218/1137276593585279086/SuperStats.jpg", text="Powered By SuperStats™️")
#     await user.send(embed=embed)


async def send_user_embed( user: object, information: dict, price: str ) -> None:

    if not information.get("asin") == None:
        embed = nextcord.Embed(title=f"{information['title']}", color=0xF33006, url=f"https://amazon.com/dp/{information['asin']}")


        embed.add_field(name="\n**Selling Statistics**", value=str(""), inline=False)
        if not information.get("estimated_sales") == None:
            embed.add_field(name="Est. Sales Per Month", value=str(information.get("estimated_sales", "Unavaliable")),inline=False)
            embed.add_field(name="Sales Rank", value=str(information['sales_rank']), inline=False)

        embed.add_field(name="BSR Rank", value=str(information.get("bsr", "Unavaliable")), inline=False)

        embed.add_field(name="\n\n**Product Information**", value=str(""), inline=False)
        embed.add_field(name="Brand", value=str(information['brand']))
        embed.add_field(name="Category ID", value=str(information['catagory_id']))
        try:
            embed.add_field(name="Category", value=str(information['category']))
        except:
            embed.add_field(name="Category", value=str("Unavaliable"))
        try:
            embed.add_field(name="Manufacturer Price", value=str(information['manufacturer_suggested_price']))
        except:
            embed.add_field(name="Manufacturer Price", value=str("Unavaliable"))

        if not information.get("buybox_price") == None: 
            embed.add_field(name="BuyBox Price", value=str(round(float(information['buybox_price']), 2)))
            embed.add_field(name="Total Offers", value=str(information['offer_count']))

        if not information.get("buybox_price") == None or not information.get("manufacturer_suggested_price") == None:
            if not information.get("buybox_price") == None:
                return_on_investment = calculate_roi(price, information['buybox_price'])
            elif not information.get("manufacturer_suggested_price") == None:
                return_on_investment = calculate_roi(price, information['manufacturer_suggested_price'])

            embed.add_field(name="\n\n**Profitability Statistics**", value=str(""), inline=False)
            embed.add_field(name="ROI", value=str(return_on_investment)+"%")


        embed.set_thumbnail(url=information['image_url'])
        embed.set_footer(icon_url="https://media.discordapp.net/attachments/1084360785431646218/1137276593585279086/SuperStats.jpg", text="Powered By SuperStats™️")
        await user.send(embed=embed)

# {'height': 9.199999809265137, 'width': 9.600000381469727, 'length': 27.5, 'weight': 6.649141788482666}


async def send_user_added_queue( user: object, message_link: dict ) -> None:

    embed = nextcord.Embed(title=f"Loading Amazon Stats...", color=0xF33006, description=f"[Message Link]({message_link})")
    embed.set_footer(icon_url="https://media.discordapp.net/attachments/1084360785431646218/1137276593585279086/SuperStats.jpg", text="Powered By SuperStats™️")
    message = await user.send(embed=embed)
    return message

async def send_user_error( user: object, error_message: dict ) -> None:
    await user.send(error_message)