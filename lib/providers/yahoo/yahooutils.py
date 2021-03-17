from lib import weather
from lib.utils import *
from . import yahoo

# yahoo news-weather api
# LCURL for location search by text (city, address, etc)
# FCURL for forecast based on woeids
LCURL = 'https://www.yahoo.com/news/_tdnews/api/resource/WeatherSearch;text=%s'
FCURL = 'https://www.yahoo.com/news/_tdnews/api/resource/WeatherService;woeids=%%5B%s%%5D'


def search_location(text, mode):
    url = LCURL % text
    data = weather.Multi.get_data(url)
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


def get_forecast(loc, locid):
    retry = 0
    data = ''
    url = FCURL % locid
    while (retry < 6) and (not weather.MyMonitor().abortRequested()):
        data = weather.Multi.get_data(url)
        if data:
            break
        else:
            weather.MyMonitor().waitForAbort(10)
            retry += 1
            log('weather download failed')
    log('yahoo forecast data: %s' % data)

    if not data:
        weather.Multi.clear_props()
        return
    yahoo.Weather.get_weather(data, loc)
    return data
