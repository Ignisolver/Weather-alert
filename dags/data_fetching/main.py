from air_pollution_api import get_air_alerts
from sheets_api import get_user_locations
from utils import create_alerts_table
from weather_api import get_weather_alerts


def main():
    locations = get_user_locations()
    air_alerts = get_air_alerts(locations)
    weather_alerts = get_weather_alerts(locations)
    table = create_alerts_table(air_alerts, weather_alerts)
    print(*table, sep='\n')


if __name__ == '__main__':
    main()
