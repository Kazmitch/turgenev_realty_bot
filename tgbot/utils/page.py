async def get_page(array, page: int = 1):
    offer_index = page - 1
    return array[offer_index]
