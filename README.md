Home Assistant sensor with meteo warnings in Poland.

[<img src="https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-dashboard.jpg" width="300" />](https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-dashboard.jpg)
[<img src="https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-states.jpg" width="300" />](https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-states.jpg)
[<img src="https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-attr.jpg" width="300" />](https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-attr.jpg)

### Data source

Data comes from meteo service of [IMGW-PIB - Instytut Meteorologii i Gospodarki Wodnej, Państwowy Instytut Badawczy](https://meteo.imgw.pl/dyn/), with fallowing endpoints:

- [x] [https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/osmet-teryt](https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/osmet-teryt)
- [ ] [https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/komet-teryt](https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/komet-teryt)
- [ ] [https://meteo.imgw.pl/api/meteo/messages/v1/warnhydro/latest/warn](https://meteo.imgw.pl/api/meteo/messages/v1/warnhydro/latest/warn)

## Instalation

Use [HACS](https://github.com/hacs/integration) for instalation, just add `https://github.com/duchu-net/meteo-warnings-poland` as custom repo.

### Config

Search and add in integration manager [Meteo Warnings Poland], selected your region for watching.  
[DEPRECATED] Confing by yaml are deprecated. Now integration supports config flow.  
For your region id check [regions codes](https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/custom_components/meteo_warnings_poland/const.py)

```yaml
sensor:
  # basic
  - platform: meteo_warnings_poland
    region_id: "2201" # required
    name: "Ostrzeżenia pogodowe" # optional

  # multiple sensors can be added
  - platform: meteo_warnings_poland
    region_id: "0601"
```

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
