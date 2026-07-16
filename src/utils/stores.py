from src.core.inject_default_kwargs import inject_default_kwarg
from src.utils.defaults import (
    default_html_parser,
    default_http_getter,
    default_gzip_decompressor,
)
import asyncio


def extract_filename_from_url(url):
    try:
        clean_url = url.split("?")[0]
        filename_with_ext = clean_url.split("/")[-1]
        filename = filename_with_ext.split(".gz")[0]
        return filename if filename else None
    except (IndexError, AttributeError):
        return None


@inject_default_kwarg("path", "")
@inject_default_kwarg("params", dict())
@inject_default_kwarg("html_parser", default_html_parser)
@inject_default_kwarg("http_getter", default_http_getter)
def get_stores_xml_urls(base_url, **kwargs):
    path = kwargs.get("path")
    params = kwargs.get("params")
    html_parser = kwargs.get("html_parser")
    http_getter = kwargs.get("http_getter")

    response = http_getter("/".join([base_url, path]), params)
    response.raise_for_status()
    parsed_html = html_parser(response.text)

    urls = []
    for link in parsed_html.select("tbody a"):
        url = link.get("href")
        if url:
            urls.append(url)
    return urls


@inject_default_kwarg("get_event_loop", asyncio.get_event_loop)
@inject_default_kwarg("http_getter", default_http_getter)
@inject_default_kwarg("gzip_decompressor", default_gzip_decompressor)
async def get_stores_info_xml(url, **kwargs):
    event_loop = kwargs.get("get_event_loop")()
    http_getter = kwargs.get("http_getter")
    decompressor = kwargs.get("gzip_decompressor")

    response = await event_loop.run_in_executor(
        None, http_getter, url, dict(stream=True)
    )
    response.raise_for_status()

    filename = extract_filename_from_url(url)

    return (filename, decompressor(response.content))
