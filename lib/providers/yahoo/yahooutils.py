from lib import weather
from lib.utils import *
from . import yahoo

# yahoo news-weather api
# LCURL for location search by text (city, address, etc)
# FCURL for forecast based on woeids
CURL = 'https://www.yahoo.com/'
YURL = 'https://www.yahoo.com/news/weather/'
LCURL = 'https://www.yahoo.com/news/_tdnews/api/resource/WeatherSearch;text=%s'
FCURL = 'https://www.yahoo.com/news/_tdnews/api/resource/WeatherService;crumb={crumb};woeids=%5B{woeid}%5D'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml'}


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
    ycookie, ycrumb = get_ycreds()
    if not ycookie:
        log('no cookie')
    url = FCURL.format(crumb=ycrumb, woeid=locid)

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
        weather.Multi.clear_props()
        return
    yahoo.Weather.get_weather(data, loc)
    return data


def get_ycreds():
    ysess = requests.Session()
    ycookie = ADDON.getSettingString('ycookie')
    ycrumb = ADDON.getSettingString('ycrumb')
    ystamp = ADDON.getSettingString('ystamp')
    log('cookie from settings: %s' % ycookie)
    log('crumb from settings: %s' % ycrumb)
    log('stamp from settings: %s' % ystamp)
    if ystamp == '' or (int(time.time()) - int(ystamp) > 31536000): # cookie expires after 1 year
        try:
            retry = 0
            while (retry < 6) and (not weather.MyMonitor().abortRequested()):
                response = ysess.get(CURL, headers=HEADERS, timeout=10)
                if response.status_code == 200:
                    break
                else:
                    weather.MyMonitor().waitForAbort(10)
                    retry += 1
                    log('getting yahoo website failed')
            if 'consent' in response.url:  # EU users are asked for cookie consent
                token = re.search('csrfToken" value="(.*?)"', response.text, flags=re.DOTALL).group(1)
                sessionid = re.search('sessionId" value="(.*?)"', response.text, flags=re.DOTALL).group(1)
                redirect = re.search('originalDoneUrl" value="(.*?)"', response.text, flags=re.DOTALL).group(1)
                DATA = {'csrfToken': token, 'sessionId': sessionid, 'originalDoneUrl': redirect, 'namespace': 'yahoo',
                        'reject': 'reject'}
                response = ysess.post(response.url, headers=HEADERS, data=DATA)
            try:
                ycookie = response.cookies['A3']
            except:
                ycookie = response.cookies['A1']
            response = ysess.get(YURL, headers=HEADERS, cookies=dict(A3=ycookie), timeout=10)
            match = re.search('WeatherStore":{"crumb":"(.*?)","weathers', response.text, re.IGNORECASE)
            if not match:
                match = re.search("win.YAHOO.context.crumb = '(.*?)'", response.text, re.IGNORECASE)
            if not match:
                match = re.search('window.YAHOO.context.*?"crumb": "(.*?)"', response.text, flags=re.DOTALL)
            ycrumb = codecs.decode(match.group(1), 'unicode-escape')
            ystamp = time.time()
            ADDON.setSettingString('ycookie', ycookie)
            ADDON.setSettingString('ycrumb', ycrumb)
            ADDON.setSettingString('ystamp', str(int(ystamp)))
            log('save cookie to settings: %s' % ycookie)
            log('save crumb to settings: %s' % ycrumb)
            log('save stamp to settings: %s' % str(int(ystamp)))
        except:
            log('exception while getting cookie')
            return '', ''
    return ycookie, ycrumb
    