# import web_pdb
# web_pdb.set_trace()
from .conversions import *
from .providers import yahoo
from .providers import weatherbit
from .providers import openweathermap
from .providers import wundergroundpws
from .providers import ambientweatherpws
from .suntime import Sun, SunTimeException

LCURL = 'https://www.yahoo.com/news/_tdnews/api/resource/WeatherSearch;text=%s'
FCURL = 'https://www.yahoo.com/news/_tdnews/api/resource/WeatherService;woeids=%%5B%s%%5D'
AURL = 'https://api.weatherbit.io/v2.0/%s'
# weatherunderground pws current conditions
WUPWSCURL = 'https://api.weather.com/v2/pws/observations/current?stationId=%s&format=json&units=m&apiKey=%s'
# weatherunderground pws 5 day forecast
WUPWSFURL = ('https://api.weather.com/v3/wx/forecast/daily/5day?geocode=%s,%s&units=m&language=en-US'
             '&format=json&apiKey=%s')
# weatherunderground pws search city api
WUPWSLCCURL = ('https://api.weather.com/v3/location/search?query=%s&locationType=city&language=en-US'
              '&format=json&apiKey=%s')
# weatherunderground pws search for pws near geocode api
WUPWSNEARURL = ('https://api.weather.com/v3/location/near?geocode=%s,%s&product=pws'
                '&format=json&apiKey=%s')
# ambientweather.net list devices api - used for both identifying devices and retrieving most recent data
# can also get stored data by specifying mac address, but that data can be from 5 - 30 minutes old
# 'https://api.ambientweather.net/v1/devices/MACADDRESS?applicationKey=%s&apiKey=%s'
AWPWSLCURL = 'https://api.ambientweather.net/v1/devices?applicationKey=%s&apiKey=%s'

WADD = ADDON.getSettingBool('WAdd')
APPID = ADDON.getSettingString('API')
WUPWSADD = ADDON.getSettingBool('WUpwsAdd')
WUPWSAPI = ADDON.getSettingString('WUpwsAPI')
AWPWSADD = ADDON.getSettingBool('AWpwsAdd')
AWPWSAPI = ADDON.getSettingString('AWpwsAPI')
AWPWSAPP = ADDON.getSettingString('AWpwsAPP')

MAPS = ADDON.getSettingBool('WMaps')
MAPID = ADDON.getSettingString('MAPAPI')
ZOOM = str(ADDON.getSettingInt('Zoom') + 2)


class MAIN():
    def __init__(self, *args, **kwargs):
        log('version %s started: %s' % (ADDONVERSION, sys.argv))
        self.MONITOR = MyMonitor()
        mode = kwargs['mode']
        log('startmode %s' % mode)
        if mode.startswith('loc'):
            self.search_location(mode)
        else:
            location, locationid, locationlat, locationlon = self.get_location(mode)
            if locationid != '-1':
                self.get_forecast(location, locationid, locationlat, locationlon)
            else:
                log('empty location id')
                self.clear_props()
            self.refresh_locations()
        log('finished')

    def search_location(self, mode):
        value = ADDON.getSettingString(mode)
        if WUPWSADD and AWPWSADD:
            keyboard = xbmc.Keyboard(value, ADDON.getLocalizedString(32319), False)
        elif WUPWSADD:
            keyboard = xbmc.Keyboard(value, ADDON.getLocalizedString(32313), False)
        elif AWPWSADD:
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
            locs = []
            log('searching for location: %s' % text)
            if text == 'awpws' and AWPWSAPI and AWPWSAPP:
                url = AWPWSLCURL % (AWPWSAPP, AWPWSAPI)
                data = self.get_data(url)
                log('awpws location data: %s' % data)
                if data:
                    locs = data
                    dialog = xbmcgui.Dialog()
                    if locs:
                        items = []
                        for item in locs:
                            listitem = (xbmcgui.ListItem(item['info']['name'], item['info']['coords']['location'] +
                                                         ' [' + str(item['info']['coords']['coords']['lat']) + '/' + str(item['info']['coords']['coords']['lon']) + ']'))
                            items.append(listitem)
                        selected = dialog.select(xbmc.getLocalizedString(396), items, useDetails=True)
                        if selected != -1:
                            ADDON.setSettingString(mode, 'awpws:' + locs[selected]['info']['name'])
                            ADDON.setSettingString(mode + 'id', locs[selected]['macAddress'])
                            ADDON.setSettingNumber(mode + 'lat', locs[selected]['info']['coords']['coords']['lat'])
                            ADDON.setSettingNumber(mode + 'lon', locs[selected]['info']['coords']['coords']['lon'])
                            log('selected location: %s' % str(locs[selected]))
                    else:
                        log('no awpws locations found')
                        dialog.ok(ADDONNAME, xbmc.getLocalizedString(284))
            elif text.startswith('wupws:') and WUPWSAPI:
                wupwslocs = []
                url = WUPWSLCCURL % (text.replace('wupws:', ''), WUPWSAPI)
                data = self.get_data(url)
                log('wupws location data: %s' % data)
                # find city
                if 'location' in data:
                    locs = data['location']
                    wupwl_keys = ("address", "city", "country", "latitude", "longitude", "placeId")
                    wupwl_dict = dict([(i, locs[i]) for i in locs if i in set(wupwl_keys)])
                    tempdict = {}
                    i = len(wupwl_dict['address'])

                    for itemcount in range(0, i):
                        for key, value in wupwl_dict.items():
                            tempdict.update({key: value[itemcount]})
                        wupwslocs.append(tempdict)
                        tempdict = {}

                dialog = xbmcgui.Dialog()
                log('wupwslocs %s' % locs)
                if wupwslocs:
                    items = []
                    for item in wupwslocs:
                        listitem = (xbmcgui.ListItem(item['address'], item['city'] + ' - ' + item['country']
                                                     + ' [' + str(item['latitude']) + '/' + str(
                            item['longitude']) + ']'))
                        items.append(listitem)
                    selected = dialog.select(xbmc.getLocalizedString(396), items, useDetails=True)
                    # find closest PWS's to selected city
                    if selected != -1:
                        url = WUPWSNEARURL % (wupwslocs[selected]['latitude'], wupwslocs[selected]['longitude'], WUPWSAPI)
                        data = self.get_data(url)
                        if 'location' in data:
                            locs = data['location']
                            wupwl_keys = ("stationName", "stationId", "latitude", "longitude", "distanceMi")
                            wupwl_dict = dict([(i, locs[i]) for i in locs if i in set(wupwl_keys)])
                            tempdict = {}
                            wupwslocs =[]
                            i = len(wupwl_dict['stationName'])

                            for itemcount in range(0, i):
                                for key, value in wupwl_dict.items():
                                    tempdict.update({key: value[itemcount]})
                                wupwslocs.append(tempdict)
                                tempdict = {}
                        dialog = xbmcgui.Dialog()
                        log('wupwslocs %s' % locs)
                        if wupwslocs:
                            items = []
                            for item in wupwslocs:
                                listitem = (xbmcgui.ListItem('Personal Weather Station - ' + item['stationId'],
                                                             str(item['distanceMi']) + ' Miles from selected city '))
                                items.append(listitem)
                            selected = dialog.select(xbmc.getLocalizedString(396), items, useDetails=True)
                        if selected != -1:
                            ADDON.setSettingString(mode, 'wupws:' + wupwslocs[selected]['stationId'])
                            ADDON.setSettingString(mode + 'id', wupwslocs[selected]['stationId'])
                            ADDON.setSettingNumber(mode + 'lat', wupwslocs[selected]['latitude'])
                            ADDON.setSettingNumber(mode + 'lon', wupwslocs[selected]['longitude'])
                            log('selected location: %s' % str(wupwslocs[selected]))
                        else:
                            log('no wupws station location found')
                            dialog.ok(ADDONNAME, xbmc.getLocalizedString(284))
                else:
                    log('no wupws city location found')
                    dialog.ok(ADDONNAME, xbmc.getLocalizedString(284))
            else:
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
                        ADDON.setSettingString(mode + 'id', str(locs[selected]['woeid']))
                        ADDON.setSettingNumber(mode + 'lat', locs[selected]['lat'])
                        ADDON.setSettingNumber(mode + 'lon', locs[selected]['lon'])
                        log('selected location: %s' % str(locs[selected]))
                else:
                    log('no yahoo locations found')
                    dialog.ok(ADDONNAME, xbmc.getLocalizedString(284))

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

        retry = 0
        data = ''
        datawu = ''
        dataaw = ''
        if loc.startswith('awpws:') and AWPWSAPI and AWPWSAPP:
            url = AWPWSLCURL % (AWPWSAPP, AWPWSAPI)
            while (retry < 6) and (not self.MONITOR.abortRequested()):
                awdata = self.get_data(url)
                if awdata:
                    for device in awdata:
                        if device['macAddress'] == locid:
                            dataaw = device
                            sun = Sun(lat, lon)
                            today_sr = sun.get_sunrise_time()
                            today_ss = sun.get_sunset_time()
                            dataaw['info']['sunrise'] = today_sr.timestamp()
                            dataaw['info']['sunset'] = today_ss.timestamp()

                    providers = '  AmbientWeatherPWS'
                    break
                else:
                    self.MONITOR.waitForAbort(10)
                    retry += 1
                    log('ambientweather download failed')
            log('ambientweather forecast data: %s' % dataaw)

            if not dataaw:
                self.clear_props()
                return
            ambientweatherpws.Weather.get_current_weather(dataaw)
            url = LCURL % dataaw['info']['coords']['address']
            woedata = self.get_data(url)
            locid = woedata[0]['woeid']
            url = FCURL % locid
            while (retry < 6) and (not self.MONITOR.abortRequested()):
                data = self.get_data(url)
                if data:
                    providers += ', Yahoo'
                    break
                else:
                    self.MONITOR.waitForAbort(10)
                    retry += 1
                    log('weather download failed')
            log('yahoo forecast data: %s' % data)
            set_property('Current.Condition', data['weathers'][0]['observation']['conditionDescription'])
        elif loc.startswith('wupws:') and WUPWSAPI:
            url = WUPWSCURL % (locid, WUPWSAPI)
            while (retry < 6) and (not self.MONITOR.abortRequested()):
                datawu = self.get_data(url)
                if datawu:
                    set_property('Location', datawu['observations'][0]['neighborhood'] + ', '
                                 + datawu['observations'][0]['stationID'])
                    providers = '  WUndergroundPWS'
                    retry = 0
                    lat = datawu['observations'][0]['lat']
                    lon = datawu['observations'][0]['lon']
                    url = WUPWSFURL % (lat, lon, WUPWSAPI)
                    while (retry < 6) and (not self.MONITOR.abortRequested()):
                        datawuf = self.get_data(url)
                        if datawuf:
                            datawu = {**datawu, **datawuf}
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
            log('wupws current/forecast data: %s' % datawu)

            if not datawu:
                self.clear_props()
                return
            set_property('Hourly.IsFetched', '')
            wundergroundpws.Weather.get_current_weather(datawu)
        else:
            url = FCURL % locid
            while (retry < 6) and (not self.MONITOR.abortRequested()):
                data = self.get_data(url)
                if data:
                    providers = '  Yahoo'
                    break
                else:
                    self.MONITOR.waitForAbort(10)
                    retry += 1
                    log('weather download failed')
            log('yahoo forecast data: %s' % data)

            if not data:
                self.clear_props()
                return
            yahoo.Weather.get_weather(data, loc, locid)

        add_weather = ''

        if MAPS and MAPID:
            providers = providers + ', Openweathermaps'
            openweathermap.Weather.get_weather(lat, lon, ZOOM, MAPID)

        if WADD and APPID:
            daily_string = 'forecast/daily?key=%s&lat=%s&lon=%s' % (APPID, lat, lon)
            url = AURL % daily_string
            add_weather = self.get_data(url)
            log('weatherbit data: %s' % add_weather)
            if not add_weather or (add_weather and 'error' in add_weather):
                add_weather = ''

        if add_weather and add_weather != '':
            weatherbit.Weather.get_weather(add_weather)
            providers = providers + ', Weatherbit.io'
            set_property('Hourly.IsFetched', 'true')
        elif datawu and WUPWSAPI and add_weather == '':
            wundergroundpws.Weather.get_daily_weather(datawu)
        elif dataaw and AWPWSAPI and AWPWSAPP and add_weather == '':
            yahoo.Weather.get_daily_weather(data)
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
