from lib.conversions import *

MAPS = ADDON.getSettingBool('WMaps')
MAPID = ADDON.getSettingString('MAPAPI')
ZOOM = str(ADDON.getSettingInt('Zoom') + 2)


class Weather():
    def __init__(self):
        pass

    def get_weather(lat, lon, zoom, mapid):
        if xbmc.getCondVisibility('System.HasAddon(script.openweathermap.maps)'):
            xbmc.executebuiltin('RunAddon(script.openweathermap.maps,lat=%s&lon=%s&zoom=%s&api=%s&debug=%s)' % (lat, lon, zoom, mapid, DEBUG))
        else:
            set_property('Map.IsFetched', '')
            for count in range (1, 6):
                set_property('Map.%i.Layer' % count, '')
                set_property('Map.%i.Area' % count, '')
                set_property('Map.%i.Heading' % count, '')
                set_property('Map.%i.Legend' % count, '')
