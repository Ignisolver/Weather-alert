from typing import List

from requests import Response

from constans import SHEET_URL, Location, UserData
from utils import send_request


def get_values_from_response(response: Response):
    json_ = response.json()
    values = json_["values"]
    return values


def create_tabele_row(row):
    tabele_row = UserData(username=row[0],
                          longitude=float(row[1]),
                          latitude=float(row[2]))
    return tabele_row


def extract_rows_and_headers(values):
    header = values[0]
    rows = values[1:]
    return header, rows


def get_tabele_from_values(values: List[str]) -> List[UserData]:
    header, rows = extract_rows_and_headers(values)
    tabele = []
    for row in rows:
        tabele_row = create_tabele_row(row)
        tabele.append(tabele_row)
    return tabele


def get_users_locations_from_tabele(tabele: List[UserData]) -> List[Location]:
    locations = []
    for user_data in tabele:
        location = Location(user_data.longitude, user_data.latitude)
        locations.append(location)
    return locations


def get_users_locations():
    resp = send_request(SHEET_URL)
    values = get_values_from_response(resp)
    tabele = get_tabele_from_values(values)
    locations = get_users_locations_from_tabele(tabele)
    return locations
