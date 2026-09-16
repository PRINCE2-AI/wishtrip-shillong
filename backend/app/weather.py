"""Optional live weather layer.

Uses the free Open-Meteo forecast API (no key required) to give a short,
honest weather note when the trip start date falls within its 16-day
forecast window. Outside that window — most trips are planned further
ahead than that — or if the request fails for any reason, the planner
falls back to the static, month-based seasonal note. The itinerary is
never blocked on this call, and the response makes clear whether a note
is a live forecast or a general seasonal estimate.
"""

from datetime import date, timedelta

import httpx

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
FORECAST_HORIZON_DAYS = 15

WEATHER_CODE_LABELS = {
    0: "clear skies", 1: "mostly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "fog",
    51: "light drizzle", 53: "drizzle", 55: "heavy drizzle",
    61: "light rain", 63: "rain", 65: "heavy rain",
    71: "light snow", 73: "snow", 75: "heavy snow",
    80: "rain showers", 81: "rain showers", 82: "heavy rain showers",
    95: "thunderstorms", 96: "thunderstorms", 99: "thunderstorms",
}


def fetch_forecast_note(latitude: float, longitude: float, start_date: date, end_date: date) -> str | None:
    today = date.today()
    horizon = today + timedelta(days=FORECAST_HORIZON_DAYS)
    if start_date > horizon or end_date < today:
        return None  # trip is outside Open-Meteo's forecast window

    try:
        response = httpx.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": "precipitation_probability_max,weathercode,temperature_2m_max",
                "timezone": "Asia/Kolkata",
                "start_date": max(start_date, today).isoformat(),
                "end_date": min(end_date, horizon).isoformat(),
            },
            timeout=5.0,
        )
        response.raise_for_status()
        daily = response.json()["daily"]
        rain_probs = daily["precipitation_probability_max"]
        codes = daily["weathercode"]
        highs = daily["temperature_2m_max"]
    except (httpx.HTTPError, KeyError, ValueError, TypeError):
        return None

    if not rain_probs or not codes or not highs:
        return None

    rainy_days = sum(1 for probability in rain_probs if probability >= 50)
    avg_high = round(sum(highs) / len(highs))
    dominant_code = max(set(codes), key=codes.count)
    condition = WEATHER_CODE_LABELS.get(dominant_code, "mixed conditions")

    if rainy_days == 0:
        rain_line = f"low rain chance, mostly {condition}"
    elif rainy_days == len(rain_probs):
        rain_line = f"rain likely most days ({condition})"
    else:
        rain_line = f"rain likely on {rainy_days} of {len(rain_probs)} days, {condition} otherwise"

    return f"Live forecast for your dates: {rain_line}, highs around {avg_high}°C."
