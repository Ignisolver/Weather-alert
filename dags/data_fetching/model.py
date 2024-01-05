from dataclasses import dataclass
from typing import Dict


@dataclass
class WeatherAlert:
    is_rain_alert: bool
    is_wind_alert: bool


@dataclass
class Location:
    lon: float
    lat: float


@dataclass
class User:
    username: str
    location: Location


AirAlerts = Dict[Location, bool]
WeatherAlerts = Dict[Location, WeatherAlert]
