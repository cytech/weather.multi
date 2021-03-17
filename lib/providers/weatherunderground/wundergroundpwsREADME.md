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
