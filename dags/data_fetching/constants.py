import os

API_KEY_OPENWEATHERMAP = os.environ.get("API_KEY_OPENWEATHERMAP")
API_KEY_SHEETS = os.environ.get("API_KEY_SHEETS")

SHEETS_USERS_LIMIT = 1000
SHEET_ID = "1CnOVLDW7gAaP-5TDoDRK-qMBjSqWKm1a4ffEmO2RinM"
API_URL_SHEETS = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/Sheet1!A1:C{SHEETS_USERS_LIMIT}"

API_URL_WEATHER = "https://api.openweathermap.org/data/2.5/forecast"
API_URL_POLLUTION = "http://api.openweathermap.org/data/2.5/air_pollution/forecast"
