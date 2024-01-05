from typing import List
from constants import API_KEY_SHEETS, API_URL_SHEETS
from model import Location, User
import requests


def extract_users(response) -> List[User]:
    rows_no_header = response.json()["values"][1:]
    return [User(username=row[0],
                 location=Location(lon=float(row[1]), 
                                   lat=float(row[2])))
                   for row in rows_no_header]

def get_users():
    response = requests.get(API_URL_SHEETS, params={"key": API_KEY_SHEETS})
    if response.status_code != 200:
        print(f"Error on a call to {API_URL_SHEETS}. HTTP status code: {response.status_code}. Response: {response.json()}")
    records = extract_users(response)
    return records


def get_user_locations():
    return [user.location for user in get_users()]
