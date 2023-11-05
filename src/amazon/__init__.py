import aiohttp, asyncio, random, json


def get_headers( ) -> dict:
    headers = {
        'authority': 'api.sellerapp.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://amazon-asin.com',
        'referer': 'https://amazon-asin.com/',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-client': 'website',
    }
    return headers

def fix_concatenated_json(concatenated_json):
    fixed_json_list = []

    while concatenated_json:
        try:
            json_obj, index = json.JSONDecoder().raw_decode(concatenated_json)
            fixed_json_list.append(json_obj)
            concatenated_json = concatenated_json[index:].lstrip()
        except json.JSONDecodeError:
            break

    return fixed_json_list


async def get_product_data( asin: str ) -> None:
    product_data = { "asin": None, "title": None, "brand": None, "image_url": None, "manufacturer_suggested_price": None}
    async with aiohttp.ClientSession() as session:
        # Load the asin to their product searcher
        async with session.get("https://api.sellerapp.com/amazon/us/research/new/free_tool/asincheck", headers = get_headers(), params ={'product_id': asin}) as response:
            response_content = await response.text()
            json_data = fix_concatenated_json(response_content)
        
    await session.close()

    for endpoint_response in json_data:
        if "{'product_details'" in str(endpoint_response):

            product_data['asin'] = endpoint_response['data']['product_details']['asin']
            product_data['title'] = endpoint_response['data']['product_details']['title']
            product_data['brand'] = endpoint_response['data']['product_details']['brand']
            product_data['image_url'] = endpoint_response['data']['product_details']['image_url']

            product_data['manufacturer_suggested_price'] = endpoint_response['data']['product_details']['manufacturer_suggested_price']['amount']

            try:
                product_data['catagory_id'] = endpoint_response['data'] ['product_details']['sales_rank'][0]['product_category_id']
            except:
                product_data['catagory_id'] = "Unavaliable"
            try:

                product_data['sales_rank'] = endpoint_response['data']['product_details']['sales_rank'][0]['rank']
            except:
                product_data['sales_rank'] = "Unavaliable"

            # product_data['height'] = endpoint_response['data']['product_details']['package_dimensions']['height']['value']
            # product_data['width'] = endpoint_response['data']['product_details']['package_dimensions']['width']['value']
            # product_data['length'] = endpoint_response['data']['product_details']['package_dimensions']['length']['value']
            # product_data['weight'] = endpoint_response['data']['product_details']['package_dimensions']['weight']['value']

        elif "{'product_potential'" in str(endpoint_response):

            product_data['bsr'] = endpoint_response['data']['product_potential']['bsr']
            try:

                product_data['category'] = endpoint_response['data']['product_potential']['category']
            except:
                product_data['category'] = "Unavaliable"
            product_data['estimated_sales'] = endpoint_response['data']['product_potential']['estimated_sales_high']
            product_data['total_score'] = endpoint_response['data']['product_potential']['potential_stats']['total_score']
        
        elif "{'offerlistings'" in str(endpoint_response):

            product_data['offer_count'] = endpoint_response['data']['offerlistings']['offer_details']['total_offer_count']
            try:

                product_data['buybox_price'] = endpoint_response['data']['offerlistings']['offer_details']['buybox_prices'][0]['listing_price']['amount']
            except:
                product_data['buybox_price'] = None

    return product_data


