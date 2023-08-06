import asyncio
import concurrent
import os
from PIL import Image

COMPRESSION_RETRIES = 5


def compress_original_format(file):
    """
    Compress the jpg file.
    """
    try:
        image = Image.open(file)
        image.save(file, quality=70, optimize=True)
    except ValueError:
        print(f"Compression not supported for file: {file}")
        return None
    return file


def change_picture_format(folder, file, target_format="webp"):
    """
    Change the pictures format to the one specified.
    """
    if folder is None or file is None or target_format is None:
        print("Failed to change picture format!")
        return None
    filename_parts = file.split("/")
    file_name, file_extension = os.path.splitext(filename_parts[-1])
    if file_extension != target_format:
        im = Image.open(file).convert("RGB")
        im.save(folder + "/" + file_name + "." + target_format, target_format)
    return file_name + "." + target_format


async def async_to_sync(function, *args):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, function, *args)
    return result
