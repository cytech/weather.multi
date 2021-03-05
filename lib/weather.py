from .conversions import *
from .providers import yahoo
from .providers import weatherbit
from .providers import openweathermap
from .providers import wundergroundpws

LCURL = 'https://www.yahoo.com/news/_tdnews/api/resource/WeatherSearch;text=%s'
FCURL = 'https://www.yahoo.com/news/_tdnews/api/resource/WeatherService;woeids=%%5B%s%%5D'
AURL = 'https://api.weatherbit.io/v2.0/%s'
# weatherunderground pws current conditions
WUPWSCURL = 'https://api.weather.com/v2/pws/observations/current?stationId=%s&format=json&units=m&apiKey=%s'
# weatherunderground pws 5 day forecast
WUPWSFURL = ('https://api.weather.com/v3/wx/forecast/daily/5day?geocode=%s,%s&units=m&language=en-US'
             '&format=json&apiKey=%s')

WADD = ADDON.getSettingBool('WAdd')
APPID = ADDON.getSettingString('API')
WUPWSADD = ADDON.getSettingBool('WUpwsAdd')
WUPWSAPI = ADDON.getSettingString('WUpwsAPI')
WUPWSSTATIONID = ADDON.getSettingString('WUpwsStationID')
WUPWSFADD = ADDON.getSettingBool('WUpwsFAdd')

MAPS = ADDON.getSettingBool('WMaps')
MAPID = ADDON.getSettingString('MAPAPI')
ZOOM = str(ADDON.getSettingInt('Zoom') + 2)


class MAIN():
    def __init__(self, *args, **kwargs):
        log('version %s started: %s' % (ADDONVERSION, sys.argv))
        self.MONITOR = MyMonitor()
        mode = kwargs['mode']
        if mode.startswith('loc'):
            self.search_location(mode)
        else:
            location, locationid, locationlat, locationlon = self.get_location(mode)
            if locationid > 0:
                self.get_forecast(location, locationid, locationlat, locationlon)
            else:
                log('empty location id')
                self.clear_props()
            self.refresh_locations()
        log('finished')

    def search_location(self, mode):
        value = ADDON.getSettingString(mode)
        keyboard = xbmc.Keyboard(value, xbmc.getLocalizedString(14024), False)
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            text = keyboard.getText()
            locs = []
            log('searching for location: %s' % text)
            url = LCURL % text
            data = self.get_data(url)
            log('location data: %s' % data)
            if data:
                locs = data
            dialog = xbmcgui.Dialog()
            if locs:
                items = []
                for item in locs:
                    listitem = (xbmcgui.ListItem(item['qualifiedName'], item['city'] + ' - ' + item['country']
                                                 + ' [' + str(item['lat']) + '/' + str(item['lon']) + ']'))
                    items.append(listitem)
                selected = dialog.select(xbmc.getLocalizedString(396), items, useDetails=True)
                if selected != -1:
                    ADDON.setSettingString(mode, locs[selected]['qualifiedName'])
                    ADDON.setSettingInt(mode + 'id', locs[selected]['woeid'])
                    ADDON.setSettingNumber(mode + 'lat', locs[selected]['lat'])
                    ADDON.setSettingNumber(mode + 'lon', locs[selected]['lon'])
                    log('selected location: %s' % str(locs[selected]))
            else:
                log('no locations found')
                dialog.ok(ADDONNAME, xbmc.getLocalizedString(284))

    def get_location(self, mode):
        location = ADDON.getSettingString('loc%s' % mode)
        locationid = ADDON.getSettingInt('loc%sid' % mode)
        locationlat = ADDON.getSettingNumber('loc%slat' % mode)
        locationlon = ADDON.getSettingNumber('loc%slon' % mode)
        if (locationid == -1) and (mode != '1'):
            log('trying location 1 instead')
            location = ADDON.getSettingString('loc1')
            locationid = ADDON.getSettingInt('loc1id')
            locationlat = ADDON.getSettingNumber('loc1lat')
            locationlon = ADDON.getSettingNumber('loc1lon')
        return location, locationid, locationlat, locationlon

    def get_data(self, url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            return response.json()
        except:
            return

    def get_forecast(self, loc, locid, lat, lon):
        set_property('WeatherProviderLogo', xbmcvfs.translatePath(os.path.join(CWD, 'resources', 'banner.png')))
        log('weather location: %s' % locid)
        providers = 'provided by Yahoo'
        if MAPS and MAPID:
            providers = providers + ', Openweathermaps'
            openweathermap.Weather.get_weather(lat, lon, ZOOM, MAPID)
        retry = 0
        url = FCURL % locid
        while (retry < 6) and (not self.MONITOR.abortRequested()):
            data = self.get_data(url)
            if data:
                break
            else:
                self.MONITOR.waitForAbort(10)
                retry += 1
                log('weather download failed')
        log('yahoo forecast data: %s' % data)
        datawu = ''
        datawuf = ''
        if WUPWSADD and WUPWSAPI and WUPWSSTATIONID:
            retry = 0
            url = WUPWSCURL % (WUPWSSTATIONID, WUPWSAPI)
            while (retry < 6) and (not self.MONITOR.abortRequested()):
                datawu = self.get_data(url)
                if datawu:
                    set_property('Location', datawu['observations'][0]['neighborhood'] + ', '
                                 + datawu['observations'][0]['stationID'])

                    if WUPWSFADD:
                        retry = 0
                        lat = datawu['observations'][0]['lat']
                        lon = datawu['observations'][0]['lon']
                        url = WUPWSFURL % (lat, lon, WUPWSAPI)
                        while (retry < 6) and (not self.MONITOR.abortRequested()):
                            datawuf = self.get_data(url)
                            if datawuf:
                                break
                            else:
                                self.MONITOR.waitForAbort(10)
                                retry += 1
                                log('wupwsforecast download failed')
                    break
                else:
                    self.MONITOR.waitForAbort(10)
                    retry += 1
                    log('wupwscurrent download failed')
        if not data:
            self.clear_props()
            return
        add_weather = ''
        if WADD and APPID:
            daily_string = 'forecast/daily?key=%s&lat=%s&lon=%s' % (APPID, lat, lon)
            url = AURL % daily_string
            add_weather = self.get_data(url)
            log('weatherbit data: %s' % add_weather)
            if not add_weather or (add_weather and 'error' in add_weather):
                add_weather = ''
        yahoo.Weather.get_weather(data, loc, locid)
        # if wupws is enabled, overwrite yahoo current props
        if datawu:
            wundergroundpws.Weather.get_current_weather(datawu)
            providers = providers + ', WeatherUnderground PWS'

        if add_weather and add_weather != '':
            weatherbit.Weather.get_weather(add_weather)
            providers = providers + ', Weatherbit.io'
        # if wupws forecast is enabled, overwrite yahoo daily props
        elif WUPWSFADD and datawuf:
            for count in range(0, MAXDAYS + 1):
                set_property('Day%i.Title' % count, 'N/A')
                set_property('Day%i.HighTemp' % count, '0')
                set_property('Day%i.LowTemp' % count, '0')
                set_property('Day%i.Outlook' % count, 'N/A')
                set_property('Day%i.OutlookIcon' % count, 'na.png')
                set_property('Day%i.FanartCode' % count, 'na')
            set_property('Hourly.IsFetched', '')
            wundergroundpws.Weather.get_daily_weather(datawuf)
            providers = 'WeatherUnderground'
        else:
            yahoo.Weather.get_daily_weather(data)
        set_property('WeatherProvider', providers)

    def clear_props(self):
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
