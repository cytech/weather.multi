# import web_pdb
# web_pdb.set_trace()
from .conversions import *
from .providers.yahoo import yahoo, yahooutils
from .providers.weatherbit import weatherbit
from .providers.openweathermap import openweathermap
from .providers.weatherunderground import wundergroundpws, wupwsutils
from .providers.ambientweather import awpwsutils

class Multi:
    def __init__(self, *args, **kwargs):
        log('version %s started: %s' % (ADDONVERSION, sys.argv))
        self.MONITOR = MyMonitor()
        mode = kwargs['mode']
        log('startmode %s' % mode)
        if mode.startswith('loc'):
            self.search_location(mode)
        else:
            location, locationid, locationlat, locationlon = self.get_location(mode)
            log('location: %s' % (location))
            log('location id: %s' % (locationid))
            # if locationid > 0:
            # default value is string of "-1" when not configured.
            # original ronie weather-multi has changed this to an integer
            if locationid != '-1':
                ycookie, ycrumb = yahooutils.get_ycreds()
                if not ycookie:
                    log('no cookie')
                else:
                    self.get_forecast(location, locationid, locationlat, locationlon, ycookie, ycrumb)
            else:
                log('empty location id')
                self.clear_props()
            self.refresh_locations()
        log('finished')

    def search_location(self, mode):
        value = ADDON.getSettingString(mode)
        if wupwsutils.WUPWSADD and awpwsutils.AWPWSADD:
            keyboard = xbmc.Keyboard(value, ADDON.getLocalizedString(32319), False)
        elif wupwsutils.WUPWSADD:
            keyboard = xbmc.Keyboard(value, ADDON.getLocalizedString(32313), False)
        elif awpwsutils.AWPWSADD:
            keyboard = xbmc.Keyboard(value, ADDON.getLocalizedString(32317), False)
        else:
            keyboard = xbmc.Keyboard(value, xbmc.getLocalizedString(14024), False)
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            text = keyboard.getText()
            # not documented, for debugging
            if text == '_DELETE_':
                dialog = xbmcgui.Dialog()
                ADDON.setSettingString(mode, '')
                ADDON.setSettingString(mode + 'id', '-1')
                ADDON.setSettingNumber(mode + 'lat', 0)
                ADDON.setSettingNumber(mode + 'lon', 0)
                dialog.ok(ADDONNAME, ADDON.getLocalizedString(32320))
                return
            log('searching for location: %s' % text)
            if text == 'awpws' and awpwsutils.AWPWSAPI and awpwsutils.AWPWSAPP:
                awpwsutils.search_location(awpwsutils.AWPWSAPP, awpwsutils.AWPWSAPI, mode)
            elif text.startswith('wupws:') and wupwsutils.WUPWSAPI:
                wupwsutils.search_location(text, wupwsutils.WUPWSAPI, mode)
            else:
                yahooutils.search_location(text, mode)

    def get_location(self, mode):
        location = ADDON.getSettingString('loc%s' % mode)
        locationid = ADDON.getSettingString('loc%sid' % mode)
        locationlat = ADDON.getSettingNumber('loc%slat' % mode)
        locationlon = ADDON.getSettingNumber('loc%slon' % mode)
        if (locationid == -1) and (mode != '1'):
            log('trying location 1 instead')
            location = ADDON.getSettingString('loc1')
            locationid = ADDON.getSettingString('loc1id')
            locationlat = ADDON.getSettingNumber('loc1lat')
            locationlon = ADDON.getSettingNumber('loc1lon')
        return location, locationid, locationlat, locationlon

    @staticmethod
    def get_data(url, cookie=''):
        HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml'}
        try:
            if cookie:
                response = requests.get(url, headers=HEADERS, cookies=dict(A3=cookie), timeout=10)
            else:
                response = requests.get(url, headers=HEADERS, timeout=10)
            return response.json()
        except:
            return

    def get_forecast(self, loc, locid, lat, lon, ycookie='', ycrumb=''):
        set_property('WeatherProviderLogo', xbmcvfs.translatePath(os.path.join(CWD, 'resources', 'banner.png')))
        log('weather location: %s' % locid)

        # yahoo, wupws, awpws data
        data = datawu = dataaw = ''

        if loc.startswith('awpws:') and awpwsutils.AWPWSAPI and awpwsutils.AWPWSAPP:
            dataaw, data = awpwsutils.get_forecast(yahooutils.LCURL, yahooutils.FCURL, awpwsutils.AWPWSAPP,
                                                   awpwsutils.AWPWSAPI, locid, lat, lon)
            providers = '  AmbientWeatherPWS, Yahoo'
        elif loc.startswith('wupws:') and wupwsutils.WUPWSAPI:
            datawu = wupwsutils.get_forecast(locid, wupwsutils.WUPWSAPI)
            providers = '  WUndergroundPWS'
        else:
            data = yahooutils.get_forecast(loc, locid)
            providers = '  Yahoo'

        add_weather = ''

        if openweathermap.MAPS and openweathermap.MAPID:
            providers = providers + ', Openweathermaps'
            openweathermap.Weather.get_weather(lat, lon, openweathermap.ZOOM, openweathermap.MAPID)

        if weatherbit.WADD and weatherbit.APPID:
            daily_string = 'forecast/daily?lat=%s&lon=%s&key=%s' % (lat, lon, weatherbit.APPID)
            url = weatherbit.AURL % daily_string
            add_weather = self.get_data(url)
            log('weatherbit data: %s' % add_weather)
            if not add_weather or (add_weather and 'error' in add_weather):
                add_weather = ''

        if add_weather and add_weather != '':
            weatherbit.Weather.get_weather(add_weather)
            providers = providers + ', Weatherbit.io'
            set_property('Hourly.IsFetched', 'true')
        elif datawu and wupwsutils.WUPWSAPI and add_weather == '':
            wundergroundpws.Weather.get_daily_weather(datawu)
        elif dataaw and awpwsutils.AWPWSAPI and awpwsutils.AWPWSAPP and add_weather == '':
            yahoo.Weather.get_daily_weather(data)
        else:
            yahoo.Weather.get_daily_weather(data)
        set_property('WeatherProvider', providers)

    @staticmethod
    def clear_props():
        set_property('Current.Condition', 'N/A')
        set_property('Current.Temperature', '0')
        set_property('Current.Wind', '0')
        set_property('Current.WindDirection', 'N/A')
        set_property('Current.Humidity', '0')
        set_property('Current.FeelsLike', '0')
        set_property('Current.UVIndex', '0')
        set_property('Current.DewPoint', '0')
        set_property('Current.OutlookIcon', 'na.png')
        set_property('Current.FanartCode', 'na')
        for count in range(0, MAXDAYS + 1):
            set_property('Day%i.Title' % count, 'N/A')
            set_property('Day%i.HighTemp' % count, '0')
            set_property('Day%i.LowTemp' % count, '0')
            set_property('Day%i.Outlook' % count, 'N/A')
            set_property('Day%i.OutlookIcon' % count, 'na.png')
            set_property('Day%i.FanartCode' % count, 'na')

    def refresh_locations(self):
        locations = 0
        for count in range(1, 6):
            loc_name = ADDON.getSettingString('loc%s' % count)
            if loc_name:
                locations += 1
            set_property('Location%s' % count, loc_name)
        set_property('Locations', str(locations))
        log('available locations: %s' % str(locations))


class MyMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)
