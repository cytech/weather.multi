A provider for the Kodi 19 Multi Weather addon (https://gitlab.com/ronie/weather.multi),
for registered and active Weather Underground personal weather station users.

:+1: If you find this provider useful, feel free to buy me a beer: https://paypal.me/cytecheng

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
   
   3.) Enter your station ID
   
   If you would like to use the Wunderground API for the forecast instead of the default Yahoo forecast:
   
        - Enable Use Wunderground PWS API for Forecast data
   
   
   
The StationID collects the data from the PWS and displays in the current observation (top area) in Kodi Weather.

Caveats:

This currently only supports a single PWS.

The Wunderground Forecast API only returns daily forecast for 5 days. It does not have more than 5 days or hourly like the Yahoo Forecast.

The Wunderground current API does not return sunrise/sunset, so the provider uses the Yahoo data.

Only English and English(US) languages are defined.

