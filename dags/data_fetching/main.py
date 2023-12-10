from air_pollution_api import get_air_alerts_for_locations
from users_api import get_users_locations
from utils import create_alerts_tabele
from weather_api import get_weather_alerts_for_locations


def main():
    locations = get_users_locations()
    air_alerts = get_air_alerts_for_locations(locations)
    weather_alerts = get_weather_alerts_for_locations(locations)
    tabele = create_alerts_tabele(air_alerts, weather_alerts)
    return tabele


if __name__ == '__main__':
    tabele = main()
    print(*tabele, sep='\n')

