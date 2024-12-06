import json
from datetime import date
from unittest.mock import Mock

import pytest

from title_belt_nhl.models.nhl_team_schedule_response import Game
from title_belt_nhl.schedule import Match, Schedule

MOCK_DATA_PATH = "./title_belt_nhl/tests/test_files/mock_league_schedule.json"
MOCK_DATA_PATH_BIG = "./title_belt_nhl/tests/test_files/mock_league_schedule_big.json"


@pytest.fixture()
def league_schedule():
    # Open the file and load the JSON data
    with open(MOCK_DATA_PATH, "r") as file:
        data = json.load(file)
        return [Game.from_dict(game) for game in data]


@pytest.fixture()
def league_schedule_big():
    # Open the file and load the JSON data
    with open(MOCK_DATA_PATH_BIG, "r") as file:
        data = json.load(file)
        return [Game.from_dict(game) for game in data]


class TestSchedule:
    def test_current_title_belt_holder(self, league_schedule):
        league_schedule.sort(key=lambda x: x.gameDate)
        cur_belt_holder = Schedule.find_current_belt_holder(league_schedule, "CHI")
        assert cur_belt_holder == "PIT"

    def test_find_match(self, monkeypatch, league_schedule):
        m = Mock()
        m.return_value = league_schedule
        monkeypatch.setattr("title_belt_nhl.schedule.getFullSchedule", m)
        monkeypatch.setattr("title_belt_nhl.schedule.INITIAL_BELT_HOLDER", "CHI")

        schedule = Schedule("VAN", from_date=date(2023, 9, 29))
        assert schedule.belt_holder == "PIT"
        assert len(schedule.matches) == 6

        match = schedule.find_match(schedule.belt_holder, date(2023, 9, 29))
        expected = Match("DAL", "PIT", date_obj=date(2023, 9, 30))
        assert str(match) == str(expected)
        assert match.date_obj == expected.date_obj

    def test_find_nearest_path_str(self, monkeypatch, league_schedule):
        m = Mock()
        m.return_value = league_schedule
        monkeypatch.setattr("title_belt_nhl.schedule.getFullSchedule", m)

        monkeypatch.setattr("title_belt_nhl.schedule.INITIAL_BELT_HOLDER", "CHI")

        schedule = Schedule("VAN", from_date=date(2023, 9, 29))
        assert schedule.belt_holder == "PIT"

        path_matches = schedule.find_nearest_path_v2()

        for i, m in enumerate(path_matches):
            print(f"{path_matches[i].date_obj} {path_matches[i]}")
        assert len(path_matches) == 2

        m1 = Match("DAL", "PIT", date_obj=date(2023, 9, 30))
        m2 = Match("VAN", "DAL", date_obj=date(2023, 10, 1))
        expected = [m1, m2]
        for i, m in enumerate(expected):
            assert str(path_matches[i]) == str(m)
            assert path_matches[i].date_obj == m.date_obj

    def test_find_nearest_path_games(self, monkeypatch, league_schedule):
        m = Mock()
        m.return_value = league_schedule
        monkeypatch.setattr("title_belt_nhl.schedule.getFullSchedule", m)

        monkeypatch.setattr("title_belt_nhl.schedule.INITIAL_BELT_HOLDER", "CHI")

        schedule = Schedule("VAN", from_date=date(2023, 9, 29))
        assert schedule.belt_holder == "PIT"
        assert len(schedule.matches) == 6

        path_matches = schedule.find_nearest_path_games()
        assert len(path_matches) == 2

        m1 = Match("DAL", "PIT", date_obj=date(2023, 9, 30))
        m2 = Match("VAN", "DAL", date_obj=date(2023, 10, 1))
        expected = [m1, m2]
        found = [False, False]
        for d, match_list in enumerate(path_matches):
            for m in match_list:
                if str(expected[d]) == str(m) and expected[d].date_obj == m.date_obj:
                    found[d] = True
                    assert m.on_shortest_path

        assert all(found)

    def test_find_nearest_path_str_big(self, monkeypatch, league_schedule_big):
        m = Mock()
        m.return_value = league_schedule_big
        monkeypatch.setattr("title_belt_nhl.schedule.getFullSchedule", m)
        monkeypatch.setattr("title_belt_nhl.schedule.INITIAL_BELT_HOLDER", "FLA")

        schedule = Schedule("CAR", from_date=date(2024, 10, 3))
        assert schedule.belt_holder == "FLA"

        path_matches = schedule.find_nearest_path_v2()

        for i, m in enumerate(path_matches):
            print(f"{path_matches[i].date_obj} {path_matches[i]}")
        assert len(path_matches) == 5

        m1 = Match("FLA", "BOS", date_obj=date(2024, 10, 8))
        m2 = Match("OTT", "FLA", date_obj=date(2024, 10, 10))
        m3 = Match("BUF", "FLA", date_obj=date(2024, 10, 12))
        m4 = Match("PIT", "BUF", date_obj=date(2024, 10, 16))
        m5 = Match("PIT", "CAR", date_obj=date(2024, 10, 18))
        expected = [m1, m2, m3, m4, m5]
        for i, m in enumerate(expected):
            assert str(path_matches[i]) == str(m)
            assert path_matches[i].date_obj == m.date_obj

    def test_find_nearest_path_games_big(self, monkeypatch, league_schedule_big):
        m = Mock()
        m.return_value = league_schedule_big
        monkeypatch.setattr("title_belt_nhl.schedule.getFullSchedule", m)

        monkeypatch.setattr("title_belt_nhl.schedule.INITIAL_BELT_HOLDER", "FLA")

        schedule = Schedule("CAR", from_date=date(2024, 10, 3))
        assert schedule.belt_holder == "FLA"
        assert len(schedule.matches) == 169

        path_matches = schedule.find_nearest_path_games()
        assert len(path_matches) == 5

        m1 = Match("FLA", "BOS", date_obj=date(2024, 10, 8))
        m2 = Match("OTT", "FLA", date_obj=date(2024, 10, 10))
        m3 = Match("BUF", "FLA", date_obj=date(2024, 10, 12))
        m4 = Match("PIT", "BUF", date_obj=date(2024, 10, 16))
        m5 = Match("PIT", "CAR", date_obj=date(2024, 10, 18))
        expected = [m1, m2, m3, m4, m5]
        found = [False, False, False, False, False]
        for d, match_list in enumerate(path_matches):
            for m in match_list:
                if str(expected[d]) == str(m) and expected[d].date_obj == m.date_obj:
                    found[d] = True
                    assert m.on_shortest_path

        assert all(found)

    def test_find_nearest_path_v2(self, monkeypatch, league_schedule_big):
        m = Mock()
        m.return_value = league_schedule_big
        monkeypatch.setattr("title_belt_nhl.schedule.getFullSchedule", m)

        monkeypatch.setattr("title_belt_nhl.schedule.INITIAL_BELT_HOLDER", "FLA")

        schedule = Schedule("MIN", from_date=date(2024, 10, 3))
        assert schedule.belt_holder == "FLA"

        path_matches = schedule.find_nearest_path_v2()

        for i, m in enumerate(path_matches):
            print(f"{path_matches[i].date_obj} {path_matches[i]}")
        assert len(path_matches) == 6

        m1 = Match("FLA", "BOS", belt_holder="FLA", date_obj=date(2024, 10, 8))
        m2 = Match("OTT", "FLA", belt_holder="FLA", date_obj=date(2024, 10, 10))
        m3 = Match("BUF", "FLA", belt_holder="FLA", date_obj=date(2024, 10, 12))
        m4 = Match("PIT", "BUF", belt_holder="BUF", date_obj=date(2024, 10, 16))
        m5 = Match("CBJ", "BUF", belt_holder="BUF", date_obj=date(2024, 10, 17))
        m6 = Match("CBJ", "MIN", belt_holder="CBJ", date_obj=date(2024, 10, 19))
        expected = [m1, m2, m3, m4, m5, m6]
        for i, m in enumerate(expected):
            assert str(path_matches[i]) == str(m)
            assert path_matches[i].date_obj == m.date_obj
            assert path_matches[i].belt_holder == m.belt_holder

    def test_find_nearest_path_v2_no_match(self, monkeypatch, league_schedule_big):
        m = Mock()
        m.return_value = league_schedule_big
        monkeypatch.setattr("title_belt_nhl.schedule.getFullSchedule", m)

        monkeypatch.setattr("title_belt_nhl.schedule.INITIAL_BELT_HOLDER", "FLA")

        schedule = Schedule("EDM", from_date=date(2024, 10, 28))
        assert schedule.belt_holder == "FLA"

        path_matches = schedule.find_nearest_path_v2()

        assert path_matches is None

    def test_find_nearest_path_v2_end_of_season(self, monkeypatch, league_schedule_big):
        m = Mock()
        m.return_value = league_schedule_big
        monkeypatch.setattr("title_belt_nhl.schedule.getFullSchedule", m)

        monkeypatch.setattr("title_belt_nhl.schedule.INITIAL_BELT_HOLDER", "FLA")

        schedule = Schedule("UTA", from_date=date(2025, 8, 15))
        assert schedule.belt_holder == "FLA"

        path_matches = schedule.find_nearest_path_v2()

        assert path_matches is None
