import pytest

from src.services.shufersal_stores_collector import collect


@pytest.mark.asyncio
async def test_shufersal_stores_collector(
    mock_get_stores_info_xml,
    mock_get_urls,
    mock_fs_storage,
    mock_load_data_content,
):
    await collect(
        "https://prices.something.com",
        "fileobjects",
        dict(catId=10),
        mock_fs_storage["fs_storage"],
        mock_get_urls,
        mock_get_stores_info_xml,
    )

    fs = mock_fs_storage["memory"]
    expected = {
        "Stores7290027600007-000-20260716-020": mock_load_data_content(
            "stores.xml"
        ),
    }
    assert expected == fs
