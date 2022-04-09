from lib import weather
from lib.utils import *
from . import ambientweatherpws
from lib.suntime import Sun
from ..yahoo import yahooutils

# ambientweather.net list devices api - used for both identifying devices and retrieving most recent data
# can also get stored data by specifying mac address, but that data can be from 5 - 30 minutes old
# 'https://api.ambientweather.net/v1/devices/MACADDRESS?applicationKey=%s&apiKey=%s'

AWPWSLCURL = 'https://api.ambientweather.net/v1/devices?applicationKey=%s&apiKey=%s'

AWPWSADD = ADDON.getSettingBool('AWpwsAdd')
AWPWSAPI = ADDON.getSettingString('AWpwsAPI')
AWPWSAPP = ADDON.getSettingString('AWpwsAPP')

def search_location(app, api, mode):
    url = AWPWSLCURL % (app, api)
    data = weather.Multi.get_data(url)
    log('awpws location data: %s' % data)
    if data:
        locs = data
        dialog = xbmcgui.Dialog()
        if locs:
            items = []
            for item in locs:
                listitem = (xbmcgui.ListItem(item['info']['name'], item['info']['coords']['location'] +
                                             ' [' + str(item['info']['coords']['coords']['lat']) + '/' + str(
                    item['info']['coords']['coords']['lon']) + ']'))
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


def get_forecast(ylcurl, yfcurl, app, api, locid, lat, lon):
    retry = 0
    data = ''
    dataaw = ''
    url = AWPWSLCURL % (app, api)
    while (retry < 6) and (not weather.MyMonitor().abortRequested()):
        awdata = weather.Multi.get_data(url)
        if awdata:
            for device in awdata:
                if device['macAddress'] == locid:
                    dataaw = device
                    sun = Sun(lat, lon)
                    today_sr = sun.get_sunrise_time()
                    today_ss = sun.get_sunset_time()
                    dataaw['info']['sunrise'] = today_sr.timestamp()
                    dataaw['info']['sunset'] = today_ss.timestamp()
            break
        else:
            weather.MyMonitor().waitForAbort(10)
            retry += 1
            log('ambientweather download failed')
    log('ambientweather forecast data: %s' % dataaw)

    if not dataaw:
        weather.Multi.clear_props()
        return

    ambientweatherpws.Weather.get_current_weather(dataaw)
    # get forecast from yahoo
    url = ylcurl % dataaw['info']['coords']['address']
    woedata = weather.Multi.get_data(url)
    locid = woedata[0]['woeid']
    ycookie, ycrumb = yahooutils.get_ycreds()
    if not ycookie:
        log('no cookie')
    url = yfcurl.format(crumb=ycrumb, woeid=locid)

    while (retry < 6) and (not weather.MyMonitor().abortRequested()):
        data = weather.Multi.get_data(url, ycookie)
        if data:
            break
        else:
            weather.MyMonitor().waitForAbort(10)
            retry += 1
            log('weather download failed')
    log('yahoo forecast data: %s' % data)
    if not data:
        return dataaw, data
    set_property('Current.Condition', data['weathers'][0]['observation']['conditionDescription'])
    return dataaw, data
