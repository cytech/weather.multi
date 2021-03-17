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
