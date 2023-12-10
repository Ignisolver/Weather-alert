from dataclasses import dataclass
from typing import Dict
from credentials import SHEETS_API_KEY

HIGH_WIND_SPEED_THRESHOLD = 30
USERS_LIMIT = 1000
SHEET_ID = "1CnOVLDW7gAaP-5TDoDRK-qMBjSqWKm1a4ffEmO2RinM"
SHEET_URL = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/Sheet1!A1:C{USERS_LIMIT}?key={SHEETS_API_KEY}"

@dataclass
class WeatherAlert:
    rain: bool
    wind: bool

@dataclass
class Location:
    lon: float
    lat: float

    def __hash__(self):
        return hash((self.lon, self.lat))


@dataclass
class UserData:
    username: str
    longitude: float
    latitude: float


AirAlerts = Dict[Location, bool]
WeatherAlerts = Dict[Location, WeatherAlert]
