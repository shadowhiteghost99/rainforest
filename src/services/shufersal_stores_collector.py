import asyncio
from src.services.fs_storage import fs_storage_factory
from src.utils.stores import (
    get_stores_xml_urls,
    get_stores_info_xml,
)


async def main(base_url, path, params, store_storage):
    urls = get_stores_xml_urls(base_url, path=path, params=params)
    for url in urls:
        filename, data = await get_stores_info_xml(url)
        store_storage.save(filename, data)


if __name__ == "__main__":
    base_url = "https://prices.shufersal.co.il"
    path = "FileObject/UpdateCategory"
    params = dict(catID=5, storeId=0)
    store_storage = fs_storage_factory("./raw/stores")
    asyncio.run(main(base_url, path, params, store_storage))
