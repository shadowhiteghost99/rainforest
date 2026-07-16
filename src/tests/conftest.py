import pytest
from unittest.mock import MagicMock, Mock

from src.utils.stores import (
    get_stores_xml_urls,
    get_stores_info_xml,
)


@pytest.fixture
def mock_successful_stores_http_getter():
    http_getter = MagicMock()
    return http_getter


@pytest.fixture
def mock_fs_storage():
    fs_storage = Mock()
    fs = dict()

    def fake_save(filename, content):
        fs[filename] = content

    fs_storage.save.side_effect = fake_save
    return dict(fs_storage=fs_storage, memory=fs)


XML_DATA = """<?xml version="1.0" encoding="UTF-8"?>
<Chain>
    <ChainID>7290027600007</ChainID>
    <ChainName>שופרסל</ChainName>
    <LastUpdateDate>2026-07-16</LastUpdateDate>
    <LastUpdateTime>02:01:05</LastUpdateTime>
    <SubChains>
        <SubChain>
            <SubChainID>1</SubChainID>
            <SubChainName>שופרסל שלי</SubChainName>
            <Stores>
                <Store>
                    <StoreID>756</StoreID>
                    <BikoretNo>7</BikoretNo>
                    <StoreType>1</StoreType>
                    <StoreName>שלי באר יעקב</StoreName>
                    <Address>17 יצחק שמיר</Address>
                    <City>2530</City>
                    <ZIPCode>7030336</ZIPCode>
                </Store>
                <Store>
                    <StoreID>374</StoreID>
                    <BikoretNo>7</BikoretNo>
                    <StoreType>1</StoreType>
                    <StoreName>שלי הרצליה- הבנים</StoreName>
                    <Address>הבנים 46</Address>
                    <City>6400</City>
                    <ZIPCode>4637948</ZIPCode>
                </Store>
                <Store>
                    <StoreID>371</StoreID>
                    <BikoretNo>7</BikoretNo>
                    <StoreType>1</StoreType>
                    <StoreName>שלי ברניצקי</StoreName>
                    <Address>נתן ברניצקי 13</Address>
                    <City>8300</City>
                    <ZIPCode>7523901</ZIPCode>
                </Store>
            </Stores>
        </SubChain>
    </SubChains>
</Chain>
"""


@pytest.fixture
def mock_get_stores_info_xml():
    mock_response = MagicMock()
    mock_response.text = XML_DATA
    mock_response.content = XML_DATA.encode("utf-8")
    mock_response.status_code = 200

    bad_response = MagicMock()
    bad_response.status_code = 400
    bad_response.raise_for_status = MagicMock(
        side_effect=Exception("400 Client Error: Not Found")
    )

    def get_handler(url, *args, **kwargs):
        if (
            url
            == "https://pricesprodpublic.blob.core.windows.net/stores/Stores7290027600007-000-20260716-020.gz?sv=2014-02-14&sr=b&sig=2%2FTm8nUHz924SjOIgix8q6Ab8VAZGPsfeXJ%2FIm8Y68c%3D&se=2026-07-16T20%3A15%3A27Z&sp=r"
        ):
            return mock_response
        return bad_response

    mock_get = MagicMock()
    mock_get.side_effect = get_handler

    async def get_stores_info(url, **kwargs):
        kwargs["http_getter"] = mock_get
        kwargs["gzip_decompressor"] = lambda x: x
        return await get_stores_info_xml(url, **kwargs)

    return get_stores_info


HTML_DATA = """<table class="webgrid" data-swhgajax="true" data-swhgcontainer="gridContainer" data-swhgcallback="">
<thead>
    <tr class="webgrid-header">
        <th scope="col">
הורדה            </th>
        <th scope="col">
<a data-swhglnk="true" href="/FileObject/UpdateCategory?catID=5&amp;storeId=0&amp;sort=Time&amp;sortdir=ASC">זמן עידכון</a>            </th>
        <th scope="col">
<a data-swhglnk="true" href="/FileObject/UpdateCategory?catID=5&amp;storeId=0&amp;sort=Size&amp;sortdir=ASC">גודל</a>            </th>
        <th scope="col">
<a data-swhglnk="true" href="/FileObject/UpdateCategory?catID=5&amp;storeId=0&amp;sort=Type&amp;sortdir=ASC">סוג קובץ</a>            </th>
        <th scope="col">
<a data-swhglnk="true" href="/FileObject/UpdateCategory?catID=5&amp;storeId=0&amp;sort=Category&amp;sortdir=ASC">קטגוריה</a>            </th>
        <th scope="col">
<a data-swhglnk="true" href="/FileObject/UpdateCategory?catID=5&amp;storeId=0&amp;sort=Branch&amp;sortdir=ASC">סניף</a>            </th>
        <th scope="col">
<a data-swhglnk="true" href="/FileObject/UpdateCategory?catID=5&amp;storeId=0&amp;sort=Name&amp;sortdir=ASC">שם</a>            </th>
        <th scope="col">
        </th>
    </tr>
</thead>
<tbody>
    <tr class="webgrid-row-style">
        <td><a href="https://pricesprodpublic.blob.core.windows.net/stores/Stores7290027600007-000-20260716-020.gz?sv=2014-02-14&amp;sr=b&amp;sig=2%2FTm8nUHz924SjOIgix8q6Ab8VAZGPsfeXJ%2FIm8Y68c%3D&amp;se=2026-07-16T20%3A15%3A27Z&amp;sp=r" target="_blank">לחץ להורדה</a></td>
        <td>7/16/2026 12:20:00 AM</td>
        <td>12.42 KB</td>
        <td>GZ</td>
        <td>stores</td>
        <td>All</td>
        <td>Stores7290027600007-000-20260716-020</td>
        <td>1</td>
    </tr>
</tbody>
</table>
"""


@pytest.fixture
def mock_get_urls():
    mock_response = MagicMock()
    mock_response.text = HTML_DATA
    mock_response.content = HTML_DATA.encode("utf-8")
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock(return_value=None)

    bad_response = MagicMock()
    bad_response.status_code = 400
    bad_response.raise_for_status = MagicMock(
        side_effect=Exception("400 Client Error: Not Found")
    )

    def get_handler(url, *args, **kwargs):
        if (
            url == "https://prices.something.com/fileobjects"
            and len(args) == 1
            and args[0].get("catId") == 10
        ):
            return mock_response
        return bad_response

    mock_get = MagicMock()
    mock_get.side_effect = get_handler

    def get_urls(base_url, **kwargs):
        kwargs["http_getter"] = mock_get
        return get_stores_xml_urls(base_url, **kwargs)

    return get_urls
