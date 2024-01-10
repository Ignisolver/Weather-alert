from dags.data_fetching.constants import AIR_ALARM, WEATHER_ALARM
from dags.data_fetching.utils import print_alerts, get_alerts
from sheets_api import get_user_locations


def main():
    locations = get_user_locations()
    air_alerts = get_alerts(locations, AIR_ALARM)
    weather_alerts = get_alerts(locations, WEATHER_ALARM)
    print_alerts(weather_alerts, air_alerts)


if __name__ == '__main__':
    main()
