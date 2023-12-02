Home Assistant sensor with meteo alerts in Poland.  
Version 0.0.4 contain 46 sensors, divided by warning level, phenomenon and activity.  
  
[<img src="https://github.com/duchu-net/meteo-warnings-poland/blob/0.0.4/docs/0.0.4-dashboard.jpg" width="300" />](https://github.com/duchu-net/meteo-warnings-poland/blob/0.0.4/docs/0.0.4-dashboard.jpg)
  

### Data source

Data comes from meteo service of [IMGW-PIB - Instytut Meteorologii i Gospodarki Wodnej, Państwowy Instytut Badawczy](https://meteo.imgw.pl/dyn/), with fallowing endpoints:

- [x] [https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/osmet-teryt](https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/osmet-teryt)
- [ ] [https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/komet-teryt](https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/komet-teryt)
- [ ] [https://meteo.imgw.pl/api/meteo/messages/v1/warnhydro/latest/warn](https://meteo.imgw.pl/api/meteo/messages/v1/warnhydro/latest/warn)

## Instalation
> [!WARNING]  
> Just in case: if you have an earlier version, please remove all devices before updating 0.0.4!  
  
Use [HACS](https://github.com/hacs/integration) for instalation, just add `https://github.com/duchu-net/meteo-warnings-poland` as custom repo.

### Config

Search and add in integration manager [Meteo Warnings Poland], selected your region for watching (rest is optional) - check your region on [dynamic map](https://meteo.imgw.pl/dyn/).   
[<img src="https://github.com/duchu-net/meteo-warnings-poland/blob/0.0.4/docs/0.0.4-config.jpg" width="300" />](https://github.com/duchu-net/meteo-warnings-poland/blob/0.0.4/docs/0.0.4-config.jpg)  
  
### Alternatives and complements

- [Burze.dzis.net sensor](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net) - lightning tracking service, data source: burze.dzis.net > blitzortung.org (Germany)
- [MeteoAlarm](https://www.home-assistant.io/integrations/meteoalarm/) - service aggregating weather warnings in Europe, data source: Federal Institute for Geology, Geophysics, Climatology and Meteorology (Austria)

### Todo

- [x] multi-sensor coordinator
- [x] warnings in progress
- [x] forecast warnings
- [ ] language support
- [ ] [MeteoalarmCard](https://github.com/MrBartusek/MeteoalarmCard/tree/master) integration

### Links

- [Building a Home Assistant Custom Component](https://aarongodfrey.dev/home%20automation/building_a_home_assistant_custom_component_part_1/)
