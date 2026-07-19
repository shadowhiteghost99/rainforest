from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

from src.utils.stores import (
    get_stores_info_xml,
    get_stores_xml_urls,
)


@pytest.fixture
def mock_fs_storage():
    fs_storage = Mock()
    fs = dict()

    def fake_save(filename, content):
        fs[filename] = content

    fs_storage.save.side_effect = fake_save
    return dict(fs_storage=fs_storage, memory=fs)


@pytest.fixture
def mock_get_stores_info_xml(mock_load_data_content):
    mock_response = MagicMock()
    xml_data = mock_load_data_content("stores.xml")
    mock_response.text = xml_data
    mock_response.content = xml_data
    mock_response.status_code = 200

    bad_response = MagicMock()
    bad_response.status_code = 400
    bad_response.raise_for_status = MagicMock(
        side_effect=Exception("400 Client Error: Not Found")
    )

    expected_url = (
        "https://pricesprodpublic.blob.core.windows.net/stores/"
        + "Stores7290027600007-000-20260716-020.gz?sv=2014-02-14&"
        + "sr=b&sig=2%2FTm8nUHz924SjOIgix8q6Ab8VAZGPsfeXJ%2FIm8Y68c%3D&"
        + "se=2026-07-16T20%3A15%3A27Z&sp=r"
    )

    def get_handler(url, *args, **kwargs):
        if url == expected_url:
            return mock_response
        return bad_response

    mock_get = MagicMock()
    mock_get.side_effect = get_handler

    async def get_stores_info(url, **kwargs):
        kwargs["http_getter"] = mock_get
        kwargs["gzip_decompressor"] = lambda x: x
        return await get_stores_info_xml(url, **kwargs)

    return get_stores_info


@pytest.fixture
def mock_get_urls(mock_load_data_content):
    mock_response = MagicMock()
    html_data = mock_load_data_content("stores.html")
    mock_response.text = html_data
    mock_response.content = html_data
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


@pytest.fixture(scope="session")
def mock_load_data_content():
    assets = {
        "stores.xml": "data/stores.xml",
        "stores.html": "data/stores.html",
    }

    def get_data_asset(name):
        if name not in assets:
            return None
        current_dir = Path(__file__).parent
        xml_path = current_dir / assets.get(name)
        return xml_path.read_text(encoding="utf-8")

    return get_data_asset
