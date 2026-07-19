import asyncio

from src.services.fs_storage import fs_storage_factory
from src.utils.defaults import (
    default_get_event_loop,
    default_gzip_decompressor,
    default_html_parser,
    default_http_getter,
    default_url_join,
)
from src.utils.stores import (
    stores_info_xml_factory,
    stores_xml_urls_factory,
)


async def collect(
    base_url, path, params, store_storage, get_urls, get_stores_info
):
    urls = get_urls(base_url, path, params)
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(get_stores_info(url)) for url in urls]
    for task in tasks:
        filename, data = task.result()
        if not filename:
            continue
        store_storage.save(filename, data)


if __name__ == "__main__":
    asyncio.run(
        collect(
            "https://prices.shufersal.co.il",
            "FileObject/UpdateCategory",
            dict(catID=5, storeId=0),
            fs_storage_factory("./raw/stores"),
            stores_xml_urls_factory(
                default_html_parser,
                default_http_getter,
                default_url_join,
            ),
            stores_info_xml_factory(
                default_get_event_loop,
                default_http_getter,
                default_gzip_decompressor,
            ),
        )
    )
