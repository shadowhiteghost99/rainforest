def extract_filename_from_url(url):
    try:
        clean_url = url.split("?")[0]
        filename_with_ext = clean_url.split("/")[-1]
        filename = filename_with_ext.split(".gz")[0]
        return filename if filename else None
    except (IndexError, AttributeError):
        return None


def stores_xml_urls_factory(html_parser, http_getter, url_join):
    def get_stores_xml_urls(base_url, path, params):
        response = http_getter(url_join(base_url, path), params)
        response.raise_for_status()
        parsed_html = html_parser(response.text)

        urls = []
        for link in parsed_html.select("tbody a"):
            url = link.get("href")
            if url:
                urls.append(url)
        return urls

    return get_stores_xml_urls


def stores_info_xml_factory(get_event_loop, http_getter, decompressor):
    async def get_stores_info_xml(url):
        event_loop = get_event_loop()

        response = await event_loop.run_in_executor(
            None, http_getter, url, dict(stream=True)
        )
        response.raise_for_status()

        filename = extract_filename_from_url(url)

        return (filename, decompressor(response.content))

    return get_stores_info_xml
