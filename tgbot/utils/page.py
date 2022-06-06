async def get_offer(array, page: int = 1):
    offer_index = page - 1
    return array[offer_index]
