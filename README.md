Fork of the weather.multi addon for Kodi 20 by ronie https://gitlab.com/ronie/weather.multi

This fork adds providers for:  
Weather Underground PWS users  
AmbientWeather.net PWS users  
:+1: If you find this provider useful, feel free to buy me a beer: https://paypal.me/cytecheng  


Note: Only the en_gb translation file is correct for this addon. All other translations will show missing information in the addon configuration.  
Feel free to update the other translations using en_gb as the base...


WEATHERUNDERGROUND
------------------

A provider for the Kodi 19 Multi Weather addon (https://gitlab.com/ronie/weather.multi),
for registered and active Weather Underground personal weather station users.

To use this provider, you need to enter your personal weather station API key in the addon settings.

To get a free API key:
1) You must have a personal weather station registered and uploading data to Weather Underground
    
    a) Join weather Underground
    
    b) Sign In
    
    c) My Profile -> My Weather Stations
    
    d) Add a New PWS
2) get API key at  https://www.wunderground.com/member/api-keys
   
First have the Kodi 19 Multi Weather addon installed and configured. then:

3) In Kodi - System - Addons - My add-ons - Weather - Multi Weather - Configure - Additional:
   
   1.) Enable "Use Wunderground PWS API for current PWS data"
   
   2.) Enter your wundergroundpws API key

4) Once enabled, add location by entering "wupws:CITY" in search location field (example - wupws:atlanta).    
   This will return a list of cities worldwide. Select the city in the list.  
   You will then receive a list of Wunderground personal weather stations near the selected city.  
   Select the PWS that you would like to monitor.
   
The StationID collects the data from the PWS and displays in the current observation (top area) in Kodi Weather.

Caveats:


The Wunderground Forecast API only returns daily forecast for 5 days. It does not have more than 5 days or hourly like the Yahoo Forecast.  
To get extended forecast you may want to sign up for the Weatherbit.io api and enable it.
This will override the Wunderground forecast.  



AMBIENTWEATHER.NET
------------------

A provider for the Kodi 19 Multi Weather addon (https://gitlab.com/ronie/weather.multi),
for registered and active AmbientWeather.net personal weather station users.


To use this provider, you need to enter your Ambientweather.net API key and Application key in the addon settings.

To get a free API key:
1) You must have a personal weather station registered and uploading data to AmbientWeather.net

2) Login to your ambientweather.net account
   
3) get API key at  https://ambientweather.net/account

3) get Application key at  https://ambientweather.net/account
   
First have the Kodi 19 Multi Weather addon installed and configured. then:

4) In Kodi - System - Addons - My add-ons - Weather - Multi Weather - Configure - Additional:
   
   1.) Enable "Use AmbientWeather PWS API for current PWS data"
   
   2.) Enter your AmbientWeather API key

   3.) Enter your AmbientWeather Application key

5) Once enabled, add location by entering "awpws" in search location field.  
   This will return a list of your registered AmbientWeather.net stations to select from.   
   
The StationID collects the data from the PWS and displays in the current observation (top area) in Kodi Weather.

Caveats:

The AmbientWeather API does not provide forecast data. The displayed forecast will be provided by Yahoo.  
The current condition description (i.e. "Breezy") is also supplied by Yahoo.  
The sunrise and sunset times are supplied thru the SunTime python library (https://github.com/SatAgro/suntime).  
To get extended forecast you may want to sign up for the Weatherbit.io api and enable it.
This will override the Yahoo forecast.  
The Ambient location search only allows return of your registered Ambient weather stations.  
The API currently does not allow access to other Ambient users station data.


********************************
INFO FOR SKINNERS

All values returned by the addon will include their units.  
Skinners won't have to bother with it.

---------------------------
DEFAULT KODI WEATHER LABELS
---------------------------


CURRENT (Yahoo)
-------
Current.Location  
Current.Condition  
Current.Temperature  
Current.Wind  
Current.WindDirection  
Current.Humidity  
Current.FeelsLike  
Current.DewPoint  
Current.UVIndex  
Current.ConditionIcon      (eg. '28.png')  
Current.FanartCode  

CURRENT (WundergroundPWS)
-------
Current.DewPoint  
Current.FeelsLike  
Current.HeatIndex  
Current.Humidity  
Current.Latitude    (station latitude)  
Current.Longitude    (station longitude)  
Current.LocalDate  
Current.LocalTime  
Current.Location  
Current.Precipitation  
Current.Pressure  
Current.SolarRadiation  
Current.Temperature  
Current.UVIndex  
Current.Wind  
Current.WindChill  
Current.WindDegree  
Current.WindDirection  
Current.WindGust  

CURRENT (AmbientWeather)
-------
Current.DewPoint  
Current.FeelsLike  
Current.Humidity  
Current.Latitude    (station latitude)  
Current.Longitude    (station longitude)  
Current.LocalDate  
Current.LocalTime  
Current.Location  
Current.Precipitation  
Current.Pressure  
Current.SolarRadiation  
Current.Temperature  
Current.UVIndex  
Current.Wind  
Current.WindDegree  
Current.WindDirection  
Current.WindGust  


DAY [0-6] (Yahoo)
---------
Day%i.Title  
Day%i.HighTemp  
Day%i.LowTemp  
Day%i.Outlook  
Day%i.OutlookIcon  
Day%i.FanartCode  


WEATHERPROVIDER
----------------
WeatherProvider  
WeatherProviderLogo  




-----------------------
EXTENDED WEATHER LABELS
-----------------------


FORECAST (Yahoo)
--------
Forecast.IsFetched  
Forecast.City  
Forecast.Country  
Forecast.Latitude  
Forecast.Longitude  
Forecast.Updated           (date and time the forecast was retrieved by yahoo)  


FORECAST (WundergroundPWS)
--------
Forecast.IsFetched  
Forecast.City  
Forecast.State  
Forecast.Country  
Forecast.Updated           (date and time the forecast was retrieved by yahoo)  


CURRENT (Yahoo)
-------
Current.IsFetched  
Current.Visibility         (visible distance)  
Current.Pressure           (air pressure)  
Current.SeaLevel           (pressure at sealevel)  
Current.Precipitation      (probability)  
Current.Cloudiness         (cloud coverage)  


TODAY (Yahoo)
-----
Today.IsFetched  
Today.Sunrise  
Today.Sunset  
Today.MoonPhase  


HOURLY [1-24] (Yahoo)
-------------
Hourly.IsFetched  
Hourly.%i.Time             (eg. '12:00')  
Hourly.%i.LongDate  
Hourly.%i.ShortDate  
Hourly.%i.Outlook          (eg. 'Very heavy rain')  
Hourly.%i.OutlookIcon  
Hourly.%i.FanartCode  
Hourly.%i.Temperature  
Hourly.%i.FeelsLike  
Hourly.%i.Humidity  
Hourly.%i.Precipitation    (probability of precipitation)  
Hourly.%i.WindSpeed  
Hourly.%i.WindDirection    (eg. 'SSW')  
Hourly.%i.WindDegree       (eg. '220°')  
Hourly.%i.DewPoint  



DAILY [1-10] (Yahoo)
------------
Daily.IsFetched  
Daily.%i.LongDay           (eg. 'Monday')  
Daily.%i.ShortDay          (eg. 'Mon')  
Daily.%i.LongDate          (eg. '1 January')  
Daily.%i.ShortDate         (eg. '1 Jan')  
Daily.%i.Outlook           (eg. 'Mostly Cloudy')  
Daily.%i.OutlookIcon  
Daily.%i.FanartCode  
Daily.%i.Humidity  
Daily.%i.DewPoint  
Daily.%i.Precipitation     (probability of precipitation)  
Daily.%i.HighTemperature   (highest temperature that will be reached today)  
Daily.%i.LowTemperature    (lowest temperature that will be reached today)  


DAILY [1-5] (WundergroundPWS)
------------
Daily.%i.FanartCode  
Daily.%i.HighTemperature   (highest temperature that will be reached today)  
Daily.%i.Humidity  
Daily.%i.LongDate          (eg. '1 January')  
Daily.%i.LongDay           (eg. 'Monday')  
Daily.%i.LowTemperature    (lowest temperature that will be reached today)  
Daily.%i.MoonPhase  
Daily.%i.MoonRise  
Daily.%i.MoonSet  
Daily.%i.Outlook           (eg. 'Mostly Cloudy')  
Daily.%i.OutlookIcon  
Daily.%i.Precipitation     (probability of precipitation)  
Daily.%i.ShortDate         (eg. '1 Jan')  
Daily.%i.ShortDay          (eg. 'Mon')  
Daily.%i.ShortWindDirection  
Daily.%i.SunRise  
Daily.%i.SunSet  
Daily.%i.WindDegree  
Daily.%i.WindDirection  
Daily.%i.WindSpeed  
Daily.IsFetched  

DAILY [1-16] (Weatherbit)
------------
Daily.IsFetched  
Daily.%i.LongDay           (eg. 'Monday')  
Daily.%i.ShortDay          (eg. 'Mon')  
Daily.%i.LongDate          (eg. '1 January')  
Daily.%i.ShortDate         (eg. '1 Jan')  
Daily.%i.Outlook           (eg. 'Very heavy rain')  
Daily.%i.OutlookIcon  
Daily.%i.FanartCode  
Daily.%i.WindSpeed  
Daily.%i.WindDirection     (eg. 'SSW')  
Daily.%i.WindDegree        (eg. '220°')  
Daily.%i.Humidity  
Daily.%i.DewPoint  
Daily.%i.WindGust  
Daily.%i.HighTemperature   (highest temperature that will be reached today)  
Daily.%i.LowTemperature    (lowest temperature that will be reached today)  
Daily.%i.Temperature       (average temperature)  
Daily.%i.HighFeelsLike  
Daily.%i.LowFeelsLike  
Daily.%i.FeelsLike         (same as HighFeelsLike)  
Daily.%i.Pressure  
Daily.%i.SeaLevel  
Daily.%i.Cloudiness  
Daily.%i.CloudsLow         (cloud coverage at 0-3km hight)  
Daily.%i.CloudsMid         (cloud coverage at 3-5km hight)  
Daily.%i.CloudsHigh        (cloud coverage at >5km hight)  
Daily.%i.Snow              (amount of snow)  
Daily.%i.SnowDepth         (depth of snow on the ground)  
Daily.%i.Precipitation     (total amount of rain and snow)  
Daily.%i.Probability       (probability of precipitation)  
Daily.%i.UVIndex  
Daily.%i.Visibility  
Daily.%i.Sunrise  
Daily.%i.Sunset  
Daily.%i.Moonrise  
Daily.%i.Moonset  
Daily.%i.MoonPhase         (moon phase fraction)  
Daily.%i.Ozone             (average ozone level)  


MAP [1-5] (Openweathermap)
---------
Map.IsFetched  
Map.%i.Area  
Map.%i.Layer  
Map.%i.Heading  
Map.%i.Legend  
