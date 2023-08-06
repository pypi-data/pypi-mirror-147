import responses
import pytest

import rsapi
import rsapi.osrs as osrs


TEST_DATA = """\
614720,1630,42468190
1069240,72,981863
1219728,69,685327
1648633,67,555122
1416123,72,917428
1193221,75,1287711
450445,75,1243635
534387,90,5485172
987904,70,763221
103704,98,12161696
424358,81,2364145
1380561,60,273777
558810,80,2003096
415322,75,1288530
911812,60,284085
1230186,60,273908
710885,60,276216
1072436,60,283377
1091844,53,139005
915756,65,478485
170938,94,8270789
585235,54,162021
239063,80,2015743
684118,60,273838
-1,-1
-1,-1
-1,-1
244252,115
76892,22
81601,41
195474,39
460217,13
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
63004,66
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
486130,105
-1,-1
-1,-1"""


@pytest.fixture
def mock_hiscores():
    with responses.RequestsMock() as rsps:
        mock_url = f"{rsapi.API_URL}/{rsapi.osrs.HISCORES_PATH}"
        rsps.add(responses.GET, mock_url, body=TEST_DATA, status=200)
        yield rsps


def test_hiscores(mock_hiscores):
    scores = osrs.hiscores("jakop")
    assert scores["Overall"]["level"] == 1630, "Overall score mismatch"
    assert scores["Overall"]["exp"] == 42468190, "Overall exp mismatch"
    assert scores["Overall"]["rank"] == 614720, "Overall rank mismatch"


def test_player_not_found():
    with responses.RequestsMock() as rsps:
        mock_url = f"{rsapi.API_URL}/{rsapi.osrs.HISCORES_PATH}"
        rsps.add(responses.GET, mock_url, body="NOT FOOND", status=404)
        with pytest.raises(rsapi.PlayerNotFound):
            osrs.hiscores("jakop")


def test_items():
    items = osrs.items("Ana in a barrel")
    assert len(items) == 1, "Expected to find Ana"


def test_item_not_found():
    with pytest.raises(rsapi.ItemError):
        osrs.items("Ana not in a barrel")
