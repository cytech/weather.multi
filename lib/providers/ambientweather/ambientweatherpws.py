from lib.conversions import *


class Weather:
    def __init__(self):
        pass

    def get_current_weather(response):
        data = response
        # awpws current
        set_property('Current.Location', data['info']['name'])
        set_property('Current.SolarRadiation', str(data['lastData']['solarradiation']))
        set_property('Current.Latitude', str(data['info']['coords']['coords']['lat']))
        set_property('Current.Longitude', str(data['info']['coords']['coords']['lon']))
        set_property('Current.UVIndex', str(data['lastData']['uv']))
        set_property('Current.WindDegree', str(data['lastData']['winddir']) + u'°')
        set_property('Current.WindDirection', xbmc.getLocalizedString(WIND_DIR(data['lastData']['winddir'])))
        set_property('Current.Humidity', str(data['lastData']['humidity']))
        set_property('Current.Temperature', convert_temp(data['lastData']['tempf'], 'F', 'C'))
        if 'C' in TEMPUNIT: 
            pressure = str(round(data['lastData']['baromrelin'] * 33.863886667, 2)) + ' mb' if data['lastData']['baromrelin'] is not None else 'N/A'
            set_property('Current.Pressure', pressure)
            precipitation = str(round(data['lastData']['hourlyrainin'] * 25.4, 2)) + ' mm/hr' if data['lastData']['hourlyrainin'] is not None else 'N/A'
            set_property('Current.Precipitation', precipitation)
            set_property('Current.FeelsLike', str(data['lastData']['feelsLike']) + TEMPUNIT)
        else:
            set_property('Current.Pressure', str(data['lastData']['baromrelin']) + ' inHg' or 'N/A')
            set_property('Current.Precipitation', str(data['lastData']['hourlyrainin']) + ' in/hr' or 'N/A')
            set_property('Current.FeelsLike',
                         convert_temp(data['lastData']['feelsLike'], 'F', 'C') + TEMPUNIT)

        set_property('Current.DewPoint', convert_temp(data['lastData']['dewPoint'], 'F', 'C'))
        set_property('Current.Wind', convert_speed(data['lastData']['windspeedmph'], 'mph', 'kmh'))
        set_property('Current.WindGust', convert_speed(data['lastData']['windspeedmph'], 'mph', 'kmh') + ' ' + SPEEDUNIT)
        set_property('Current.LocalTime', convert_datetime(data['lastData']['dateutc'], 'timestampms', 'time', None))
        set_property('Current.LocalDate', convert_datetime(data['lastData']['dateutc'], 'timestampms', 'timedate', None))
        set_property('Today.Sunrise', convert_datetime(data['info']['sunrise'], 'timestamp', 'time', None))
        set_property('Today.Sunset', convert_datetime(data['info']['sunset'], 'timestamp', 'time', None))
        set_property('Current.IsFetched', 'true')
        cleardailyproperties()

# clear yahoo, wunderground  and weatherbit forecast when location change
def cleardailyproperties():
    i = 1
    while i < 17:  # yahoo = 11, weatherbit = 16
        clear_property('Daily.%i.ShortDay' % i)
        clear_property('Daily.%i.LongDay' % i)
        clear_property('Daily.%i.ShortDate' % i)
        clear_property('Daily.%i.LongDate' % i)
        clear_property('Daily.%i.HighTemperature' % i)
        clear_property('Daily.%i.LowTemperature' % i)
        clear_property('Daily.%i.Outlook' % i)
        clear_property('Daily.%i.OutlookIcon' % i)
        clear_property('Daily.%i.FanartCode' % i)
        clear_property('Daily.%i.Humidity' % i)
        clear_property('Daily.%i.Precipitation' % i)
        clear_property('Daily.%i.DewPoint' % i)
        clear_property('Daily.%i.WindDirection' % i)
        clear_property('Daily.%i.WindDegree' % i)
        clear_property('Daily.%i.Temperature' % i)
        clear_property('Daily.%i.FeelsLike' % i)
        clear_property('Daily.%i.HighFeelsLike' % i)
        clear_property('Daily.%i.LowFeelsLike' % i)
        clear_property('Daily.%i.Pressure' % i)
        clear_property('Daily.%i.SeaLevel' % i)
        clear_property('Daily.%i.Snow' % i)
        clear_property('Daily.%i.SnowDepth' % i)
        clear_property('Daily.%i.Visibility' % i)
        clear_property('Daily.%i.Pressure' % i)
        clear_property('Daily.%i.SeaLevel' % i)
        clear_property('Daily.%i.Snow' % i)
        clear_property('Daily.%i.SnowDepth' % i)
        clear_property('Daily.%i.Precipitation' % i)
        clear_property('Daily.%i.Precipitation' % i)
        clear_property('Daily.%i.Visibility' % i)
        clear_property('Daily.%i.WindSpeed' % i)
        clear_property('Daily.%i.WindGust' % i)
        clear_property('Daily.%i.Cloudiness' % i)
        clear_property('Daily.%i.CloudsLow' % i)
        clear_property('Daily.%i.CloudsMid' % i)
        clear_property('Daily.%i.CloudsHigh' % i)
        clear_property('Daily.%i.Probability' % i)
        clear_property('Daily.%i.UVIndex' % i)
        clear_property('Daily.%i.UVIndex' % i)
        clear_property('Daily.%i.Sunrise' % i)
        clear_property('Daily.%i.Sunset' % i)
        clear_property('Daily.%i.Moonrise' % i)
        clear_property('Daily.%i.Moonset' % i)
        clear_property('Daily.%i.MoonPhase' % i)
        clear_property('Daily.%i.Ozone' % i)
        i += 1
