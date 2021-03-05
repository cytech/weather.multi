from ..conversions import *


# create feelslike from windchill or heatindex for wupws
def feels_like(t, ws=0, hi=0, wc=0):
    if t <= 10 and ws >= 8:
        feelslike = wc
    elif t >= 26:
        feelslike = hi
    else:
        feelslike = t
    return str(int(round(feelslike)))


class Weather():
    def __init__(self):
        pass

    # wu current api does not return sunrise/sunset so rely on yahoo
    # wu forecast api returns daily sunrise/sunset but why fetch just for that....
    def get_current_weather(response):
        data = response['observations'][0]
        # wupws current
        set_property('Current.Location', data['stationID'])
        set_property('Current.SolarRadiation', str(data['solarRadiation']))
        set_property('Current.Latitude', str(data['lat']))
        set_property('Current.Longitude', str(data['lon']))
        set_property('Current.UVIndex', str(data['uv']))
        set_property('Current.WindDegree', str(data['winddir']) + u'°')
        set_property('Current.WindDirection', xbmc.getLocalizedString(WIND_DIR(data['winddir'])))
        set_property('Current.Humidity', str(data['humidity']))
        set_property('Current.Temperature', str(data['metric']['temp']))
        if 'F' in TEMPUNIT:
            set_property('Current.Pressure',
                         str(round(data['metric']['pressure'] * 0.02953, 2)) + ' inHg')
            set_property('Current.Precipitation',
                         str(round(data['metric']['precipRate'] * 0.0393701, 2)) + ' in/hr')
            set_property('Current.HeatIndex',
                         convert_temp(data['metric']['heatIndex'], 'C') + TEMPUNIT)
            set_property('Current.WindChill',
                         convert_temp(data['metric']['windChill'], 'C') + TEMPUNIT)
        else:
            set_property('Current.Pressure', str(data['metric']['pressure']) + ' mb')
            set_property('Current.Precipitation', str(data['metric']['precipRate']) + ' mm/hr')
            set_property('Current.HeatIndex', str(data['metric']['heatIndex']) + TEMPUNIT)
            set_property('Current.WindChill', str(data['metric']['windChill']) + TEMPUNIT)
        set_property('Current.DewPoint', str(data['metric']['dewpt']))
        set_property('Current.Wind', str(data['metric']['windSpeed']))
        set_property('Current.WindGust', convert_speed(data['metric']['windGust'], 'kmh') + ' ' + SPEEDUNIT)
        set_property('Current.FeelsLike', feels_like(int(data['metric']['temp']),
                                                     data['metric']['windSpeed'],
                                                     data['metric']['heatIndex'],
                                                     data['metric']['windChill']) + TEMPUNIT)
        set_property('Current.LocalTime', convert_datetime(data['epoch'], 'timestamp', 'time', None))
        set_property('Current.LocalDate', convert_datetime(data['epoch'], 'timestamp', 'timedate', None))
        set_property('Current.IsFetched', 'true')
        set_property('Today.IsFetched', 'true')

    def get_daily_weather(response):
        # wunderground pws api only offers 5 day forecast, which does not include hourly
        data = response
        set_property('Forecast.IsFetched', 'true')
        set_property('Forecast.City', "")
        set_property('Forecast.State', "")
        set_property('Forecast.Country', "")
        set_property('Forecast.Updated', convert_datetime(data['expirationTimeUtc'][0], 'timestamp', 'timedate', 'long'))

        # daily properties
        set_property('Daily.IsFetched', 'true')
        for count, item in enumerate(data['dayOfWeek']):
            set_property('Daily.%i.LongDay' % (count + 1), item)
            set_property('Daily.%i.ShortDay' % (count + 1), item)
            set_property('Daily.%i.MoonPhase' % (count + 1), str(data['moonPhase']))
            set_property('Daily.%i.Moonrise' % (count + 1),
                         convert_datetime(data['moonriseTimeUtc'][0], 'timestamp', 'time', None))
            set_property('Daily.%i.Moonset' % (count + 1),
                         convert_datetime(data['moonsetTimeUtc'][0], 'timestamp', 'time', None))
            # precipitation as amount forecast
            # if 'F' in TEMPUNIT:
            #     set_property('Daily.%i.Precipitation' % (count + 1),
            #                  str(data['daypart'][0]['qpf'][2 * count]) + ' in')
            # else:
            #     set_property('Daily.%i.Precipitation' % (count + 1),
            #                  str(data['daypart'][0]['qpf'][2 * count]) + ' mm')
            set_property('Daily.%i.Sunrise' % (count + 1),
                         convert_datetime(data['sunriseTimeUtc'][0], 'timestamp', 'time', None))
            set_property('Daily.%i.Sunset' % (count + 1),
                         convert_datetime(data['sunsetTimeUtc'][0], 'timestamp', 'time', None))
            set_property('Daily.%i.LongDate' % (count + 1),
                         convert_datetime(data['validTimeUtc'][count], 'timestamp', 'monthday', 'long'))
            set_property('Daily.%i.ShortDate' % (count + 1),
                         convert_datetime(data['validTimeUtc'][count], 'timestamp', 'monthday', 'short'))
            # daypart
            # PLEASE NOTE: The daypart object (all keys[0]) as well as the temperatureMax field OUTSIDE
            # of the daypart object will appear as null in the API after 3:00pm Local Apparent Time.
            # this provider only uses iconCode and temperature in the forecast at this time
            # so after 3pm set iconCode to the night item and temperature to 'na'
            if data['daypart'][0]['iconCode'][2 * count] == 'na' or data['daypart'][0]['temperature'][
                2 * count] == 'na':
                weathercode = data['daypart'][0]['iconCode'][2 * count + 1]
                set_property('Daily.%i.HighTemperature' % (count + 1), str('na'))
            else:
                weathercode = data['daypart'][0]['iconCode'][2 * count]
                set_property('Daily.%i.HighTemperature' % (count + 1),
                             convert_temp(data['daypart'][0]['temperature'][2 * count], 'C') + TEMPUNIT)

            # precipitation as % probability
            set_property('Daily.%i.Precipitation' % (count + 1), str(data['daypart'][0]['precipChance']) + '%')
            set_property('Daily.%i.Humidity' % (count + 1),
                         str(data['daypart'][0]['relativeHumidity'][2 * count] or 0) + '%')
            set_property('Daily.%i.LowTemperature' % (count + 1),
                         convert_temp(data['daypart'][0]['temperature'][2 * count + 1], 'C') + TEMPUNIT)
            set_property('Daily.%i.WindDirection' % (count + 1),
                         str(data['daypart'][0]['windDirection'][2 * count] or 0))
            set_property('Daily.%i.ShortWindDirection' % (count + 1),
                         str(data['daypart'][0]['windDirectionCardinal'][2 * count] or 0))
            set_property('Daily.%i.WindDegree' % (count + 1),
                         str(data['daypart'][0]['windDirection'][2 * count] or 0))
            set_property('Daily.%i.WindSpeed' % (count + 1),
                         convert_speed(data['daypart'][0]['windSpeed'][2 * count], 'kmh') + SPEEDUNIT)
            set_property('Daily.%i.Outlook' % (count + 1), data['daypart'][0]['wxPhraseLong'][2 * count])
            set_property('Daily.%i.OutlookIcon' % (count + 1), WEATHER_ICON % weathercode)
            set_property('Daily.%i.FanartCode' % (count + 1), str(weathercode))
