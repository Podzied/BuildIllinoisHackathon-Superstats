import asyncio, aiohttp
from bs4 import BeautifulSoup

def get_headers( ) -> dict:
    headers = {'authority': 'www.barcodespider.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'max-age=0', 'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    return headers

def parse_content( html_content: str ) -> str:
    """Using BS4 find the asin in the html"""
    try:

        soup_client: object = BeautifulSoup(html_content, "html.parser")
        info_table = soup_client.find("table", {"class": "table table-striped"})
        text_list: list = [line for line in info_table.text.split("\n") if not line == ""]
        result = {text_list[i]: text_list[i+1] for i in range(0, len(text_list), 2)}
        return result
    except Exception as e:
        print(e)

async def get_product_data( upc: str ) -> None:
    async with aiohttp.ClientSession() as session:
        # Load the asin to their product searcher
        async with session.get(f"https://www.barcodespider.com/{upc}", headers = get_headers()) as response:
            response_content = await response.text()
            if "not found" in response_content:
                return None
            asin = parse_content(response_content)
            return asin
        



