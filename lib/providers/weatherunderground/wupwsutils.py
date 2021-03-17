from lib import weather
from lib.utils import *
from . import wundergroundpws

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

WUPWSADD = ADDON.getSettingBool('WUpwsAdd')
WUPWSAPI = ADDON.getSettingString('WUpwsAPI')


def search_location(text, api, mode):
    wupwslocs = []
    url = WUPWSLCCURL % (text.replace('wupws:', ''), api)
    data = weather.Multi.get_data(url)
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
            url = WUPWSNEARURL % (wupwslocs[selected]['latitude'], wupwslocs[selected]['longitude'], api)
            data = weather.Multi.get_data(url)
            if 'location' in data:
                locs = data['location']
                wupwl_keys = ("stationName", "stationId", "latitude", "longitude", "distanceMi")
                wupwl_dict = dict([(i, locs[i]) for i in locs if i in set(wupwl_keys)])
                tempdict = {}
                wupwslocs = []
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


def get_forecast(locid, api):
    url = WUPWSCURL % (locid, api)
    retry = 0
    while (retry < 6) and (not weather.MyMonitor().abortRequested()):
        datawu = weather.Multi.get_data(url)
        if datawu:
            set_property('Location', datawu['observations'][0]['neighborhood'] + ', '
                         + datawu['observations'][0]['stationID'])
            retry = 0
            lat = datawu['observations'][0]['lat']
            lon = datawu['observations'][0]['lon']
            url = WUPWSFURL % (lat, lon, api)
            while (retry < 6) and (not weather.MyMonitor().abortRequested()):
                datawuf = weather.Multi.get_data(url)
                if datawuf:
                    datawu = {**datawu, **datawuf}
                    break
                else:
                    weather.MyMonitor().waitForAbort(10)
                    retry += 1
                    log('wupwsforecast download failed')
            break
        else:
            weather.MyMonitor().waitForAbort(10)
            retry += 1
            log('wupwscurrent download failed')
    log('wupws current/forecast data: %s' % datawu)

    if not datawu:
        weather.Multi.clear_props()
        return
    set_property('Hourly.IsFetched', '')
    wundergroundpws.Weather.get_current_weather(datawu)
    return datawu
