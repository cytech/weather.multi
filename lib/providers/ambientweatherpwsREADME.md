A provider for the Kodi 19 Multi Weather addon (https://gitlab.com/ronie/weather.multi),
for registered and active AmbientWeather.net personal weather station users.

:+1: If you find this provider useful, feel free to buy me a beer: https://paypal.me/cytecheng

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
   
   
The StationID collects the data from the PWS and displays in the current observation (top area) in Kodi Weather.

Caveats:

The AmbientWeather API does not provide forecast data. The displayed forecast will be provided by Yahoo.
To get extended forecast you may want to sign up for the Weatherbit.io api and enable it.
This will override the Yahoo forecast.

If you are running both the WeatherUnderground and AmbientWeather providers, only one can be enabled at a time.
Add location search will only work for the enabled provider.
To add locations for both providers, enable the one you want the location for then add location.
Then enable the other and add location.
