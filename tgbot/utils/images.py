import asyncio
from io import BytesIO

import aiohttp
from PIL import Image
from cairosvg import svg2png


async def get_photo_bytes(url: str):
    """Получаем фотографию в формате bytes."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    if dict(response.headers)['Content-Type'] == 'image/svg+xml':
                        svg = await response.read()
                        photo = svg2png(bytestring=svg)
                    else:
                        photo = await response.read()
                    return photo
        except Exception as e:
            print(e)


async def merge_photos(photos: tuple):
    """Делаем из двух фото одно"""
    image1 = Image.open(BytesIO(photos[0]))
    image2 = Image.open(BytesIO(photos[1]))

    image1_size = image1.size
    image2_size = image2.size

    new_image = Image.new('RGB', (2 * image1_size[0] + 5, image1_size[1]))

    white = Image.new('RGB', (15, image1_size[1]), color='#FFFFFF')
    white_size = white.size

    new_image.paste(image1, (0, 0))
    new_image.paste(white, (image1_size[0], 0))
    new_image.paste(image2, (image1_size[0] + white_size[0], 0))
    # new_image.show()

    return new_image


async def make_photo(offers: list):
    for offer in offers:
        tasks_photo_bytes = []
        for image in offer['image'][:2]:
            if type(image) == dict:
                tasks_photo_bytes.append(asyncio.create_task(get_photo_bytes(image['#text'])))
                # image_objects.append(await get_photo_bytes(image['#text']))
            else:
                # image_objects.append(await get_photo_bytes(image))
                tasks_photo_bytes.append(asyncio.create_task(get_photo_bytes(image)))
        photo_bytes = await asyncio.gather(*tasks_photo_bytes)
        # merged_photo = await merge_photos(image_objects)
        merged_photo = []
        # for photo in photo_bytes:
        merged_photo.append(asyncio.create_task(merge_photos(photo_bytes)))
        photos = await asyncio.gather(*merged_photo)
        offer['photo'] = photos
    return offers


async def resize_photo(url: str) -> BytesIO:
    """Изменяем размер фотографии."""
    bytes_photo = await get_photo_bytes(url)
    img = Image.open(BytesIO(bytes_photo))
    img_resize = img.resize((600, 600))
    buf = BytesIO()
    img_resize.save(buf, format='PNG')
    byte_img = buf.getvalue()
    photo = BytesIO(byte_img)
    return photo
