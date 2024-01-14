from data_fetching.constants import AIR_ALARM, WEATHER_ALARM
from data_fetching.utils import print_alerts, get_alerts, write_df_to_s3, read_from_s3
from sheets_api import get_user_locations


def main():
    locations = get_user_locations()
    air_alerts = get_alerts(locations, AIR_ALARM)
    weather_alerts = get_alerts(locations, WEATHER_ALARM)
    print_alerts(weather_alerts, air_alerts)


def real_test():
    locations = get_user_locations()
    write_df_to_s3(locations, filename="locations.csv")

    locations2 = read_from_s3(filename="locations.csv")
    weather_alerts = get_alerts(locations2, WEATHER_ALARM)
    write_df_to_s3(weather_alerts, filename="weather_alerts.csv")

    locations3 = read_from_s3(filename="locations.csv")
    air_alerts = get_alerts(locations3, AIR_ALARM)
    write_df_to_s3(air_alerts, filename="air_alerts.csv")

    weather_alerts2 = read_from_s3(filename="weather_alerts.csv")
    air_alerts2 = read_from_s3(filename="air_alerts.csv")
    print_alerts(weather_alerts2, air_alerts2)


if __name__ == '__main__':
    # main()
    real_test()