import asyncio
from src.services.fs_storage import fs_storage_factory
from src.utils.stores import (
    get_stores_xml_urls,
    get_stores_info_xml,
)


async def collect(base_url, path, params, store_storage, get_urls, get_stores_info):
    urls = get_urls(base_url, path=path, params=params)
    for url in urls:
        filename, data = await get_stores_info(url)
        store_storage.save(filename, data)


if __name__ == "__main__":
    asyncio.run(
        collect(
            "https://prices.shufersal.co.il",
            "FileObject/UpdateCategory",
            dict(catID=5, storeId=0),
            fs_storage_factory("./raw/stores"),
            get_stores_xml_urls,
            get_stores_info_xml,
        )
    )
