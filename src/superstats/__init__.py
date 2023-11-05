from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio, datetime, random, json
from typing import List


page_thread_holder: List[object] = [ ]

pending_tasks: list = [ ]

completed_tasks: list = [ ]


with open("proxies.txt", "r") as file:
    proxies = [ proxy.replace("\n", "") for proxy in file.readlines() if not proxy.replace("\n", "") == None]

proxy = random.choice(proxies).split(":")


def get_search_url( task: dict ) -> str:
    if task['stage'] == 1:
        return f"https://sellercentral.amazon.com/rcpublic/productmatch?searchKey={task['_id']}&countryCode=US&locale=en-US"
    elif task['stage'] == 2:
        return f"https://sellercentral.amazon.com/rcpublic/getadditionalpronductinfo?countryCode=US&asin={task['asin']}&fnsku=&searchType=GENERAL&locale=en-US"


def get_asin( products: list ) -> str:
    asin = products[0]['asin']
    return asin


def get_products( task_content: list ) -> list:
    try:task_content = json.loads(task_content)
    except: return []
    
    found_products = task_content['data']['otherProducts']
    if found_products['totalProductCount'] == 0:
        return []
    
    products_holder: list = [ ]
    # Iterate through all the products from the endpoint
    for product in found_products['products']:
        products_holder.append(
            {
                "asin": product['asin'],
                "image": product['imageUrl'],
                "catagory": product['gl'].replace("gl_", ""),
                "title": product['title'],
                "reviews": {
                    "count": product['customerReviewsCount'],
                    "rating": product['customerReviewsRatingfullStarCount']
                },
                "offers": product['offerCount'],
                "sales_rank": product.get("salesRank")
            }
        )
    return products_holder

def get_pricing( task_content: dict ) -> dict:
    try:task_content = json.loads(task_content)
    except: return None

    if task_content['succeed'] == True:
        return task_content['data']['price']['amount']
    else:
        return None



async def run_data_extraction( ) -> None:
    """Method to initalize all of the async objects"""
    async with async_playwright() as playwright:
        global webkit, browser, context, page
        webkit = playwright.webkit
        print("[+] Lauching browser [+]")
        global browser, context
        browser = await webkit.launch(headless=True)
        context = await browser.new_context()

        page_one = await browser.new_page()
        page_two = await browser.new_page()

        page_thread_holder.append(
            {
                "number": "one",
                "value": page_one
            }
        )
        page_thread_holder.append(
            {
                "number": "two",
                "value": page_two
            }
        )

        x = random.choice(page_thread_holder)['value']
        await x.goto("https://sellercentral.amazon.com/hz/fba/profitabilitycalculator/index?lang=en_US")
        await asyncio.sleep(2)

    
        while True:
            if not len(pending_tasks) == 0:
                
                task = pending_tasks.pop(0)
                thread = random.choice(page_thread_holder)
                thread_obj = thread['value']
                
                if task['stage'] != 3:
                    # Call the method to get what url to extract data from
                    task_search_url: str = get_search_url(task)
                    await thread_obj.goto(task_search_url)
                    check_page_content = await thread_obj.content()
                    check_page_content = BeautifulSoup(check_page_content.encode("utf-8"), "html.parser").text
                    
                    if task['stage'] == 1:
                        
                        products: list = get_products( check_page_content )
                        if not len(products) == 0:
                            asin = get_asin(products)
                            task['products'] = products
                            task['asin'] = asin

                            task['stage']+=1
                            print(f"Task has been set to stage 2")
                            pending_tasks.append(task)

                        else:
                            task['products'] = None
                            task['asin'] = None
                            task['pricing'] = None

                            print(f"Task has been set to complete because of no found products")
                            completed_tasks.append(task)
                    
                    elif task['stage'] == 2:
                        print("[+] Stage 2 Complete Now moving to completed [+]")
                        pricing = get_pricing(check_page_content)
                        task['pricing'] = pricing
                        completed_tasks.append(task)


            await asyncio.sleep(0.3)


async def task_gather_runner():
    await asyncio.gather(
        run_data_extraction()
    )
