from . import async_handler


async def resolve_product( search_term: str ) -> dict:
    """This method resolves the product and gets amazon stats from search_term"""
    dataclient = await async_handler.get_page()
    dataclient.goto(f"https://sellercentral.amazon.com/rcpublic/productmatch?searchKey={search_term}&countryCode=US&locale=en-US")
    print(dataclient.content())

async def get_product_data( search_term: str ) -> dict:
    """This is the main method you call from other files"""
    product_resolver_data = await resolve_product( search_term )