from src.services.shufersal_stores_collector import collect
import pytest


@pytest.mark.asyncio
async def test_shufersal_stores_collector(
    mock_get_stores_info_xml, mock_get_urls, mock_fs_storage
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
        "Stores7290027600007-000-20260716-020": b'<?xml version="1.0" encoding="UTF-8"?>\n<Chain>\n    <ChainID>7290027600007</ChainID>\n    <ChainName>\xd7\xa9\xd7\x95\xd7\xa4\xd7\xa8\xd7\xa1\xd7\x9c</ChainName>\n    <LastUpdateDate>2026-07-16</LastUpdateDate>\n    <LastUpdateTime>02:01:05</LastUpdateTime>\n    <SubChains>\n        <SubChain>\n            <SubChainID>1</SubChainID>\n            <SubChainName>\xd7\xa9\xd7\x95\xd7\xa4\xd7\xa8\xd7\xa1\xd7\x9c \xd7\xa9\xd7\x9c\xd7\x99</SubChainName>\n            <Stores>\n                <Store>\n                    <StoreID>756</StoreID>\n                    <BikoretNo>7</BikoretNo>\n                    <StoreType>1</StoreType>\n                    <StoreName>\xd7\xa9\xd7\x9c\xd7\x99 \xd7\x91\xd7\x90\xd7\xa8 \xd7\x99\xd7\xa2\xd7\xa7\xd7\x91</StoreName>\n                    <Address>17 \xd7\x99\xd7\xa6\xd7\x97\xd7\xa7 \xd7\xa9\xd7\x9e\xd7\x99\xd7\xa8</Address>\n                    <City>2530</City>\n                    <ZIPCode>7030336</ZIPCode>\n                </Store>\n                <Store>\n                    <StoreID>374</StoreID>\n                    <BikoretNo>7</BikoretNo>\n                    <StoreType>1</StoreType>\n                    <StoreName>\xd7\xa9\xd7\x9c\xd7\x99 \xd7\x94\xd7\xa8\xd7\xa6\xd7\x9c\xd7\x99\xd7\x94- \xd7\x94\xd7\x91\xd7\xa0\xd7\x99\xd7\x9d</StoreName>\n                    <Address>\xd7\x94\xd7\x91\xd7\xa0\xd7\x99\xd7\x9d 46</Address>\n                    <City>6400</City>\n                    <ZIPCode>4637948</ZIPCode>\n                </Store>\n                <Store>\n                    <StoreID>371</StoreID>\n                    <BikoretNo>7</BikoretNo>\n                    <StoreType>1</StoreType>\n                    <StoreName>\xd7\xa9\xd7\x9c\xd7\x99 \xd7\x91\xd7\xa8\xd7\xa0\xd7\x99\xd7\xa6\xd7\xa7\xd7\x99</StoreName>\n                    <Address>\xd7\xa0\xd7\xaa\xd7\x9f \xd7\x91\xd7\xa8\xd7\xa0\xd7\x99\xd7\xa6\xd7\xa7\xd7\x99 13</Address>\n                    <City>8300</City>\n                    <ZIPCode>7523901</ZIPCode>\n                </Store>\n            </Stores>\n        </SubChain>\n    </SubChains>\n</Chain>\n'
    }
    assert expected == fs
