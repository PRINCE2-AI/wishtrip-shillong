from datetime import date, timedelta

import httpx
import pytest

from app.weather import fetch_forecast_note


def test_returns_none_when_trip_is_far_in_the_future():
    start = date.today() + timedelta(days=60)
    end = start + timedelta(days=3)
    assert fetch_forecast_note(25.57, 91.88, start, end) is None


def test_returns_none_when_trip_is_entirely_in_the_past():
    end = date.today() - timedelta(days=5)
    start = end - timedelta(days=3)
    assert fetch_forecast_note(25.57, 91.88, start, end) is None


def test_parses_a_successful_forecast_response(monkeypatch):
    start = date.today() + timedelta(days=1)
    end = start + timedelta(days=2)

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"daily": {
                "precipitation_probability_max": [80, 20, 70],
                "weathercode": [61, 61, 3],
                "temperature_2m_max": [22, 24, 23],
            }}

    def fake_get(url, params, timeout):
        return FakeResponse()

    monkeypatch.setattr(httpx, "get", fake_get)
    note = fetch_forecast_note(25.57, 91.88, start, end)
    assert note is not None
    assert "rain likely on 2 of 3 days" in note
    assert "23°C" in note


def test_falls_back_to_none_on_network_failure(monkeypatch):
    start = date.today() + timedelta(days=1)
    end = start + timedelta(days=1)

    def fake_get(url, params, timeout):
        raise httpx.ConnectError("boom", request=httpx.Request("GET", url))

    monkeypatch.setattr(httpx, "get", fake_get)
    assert fetch_forecast_note(25.57, 91.88, start, end) is None
