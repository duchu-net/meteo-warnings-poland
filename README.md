Home Assistant sensor with meteo warnings in Poland.

[<img src="https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-dashboard.jpg" width="300" />](https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-dashboard.jpg)
[<img src="https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-states.jpg" width="300" />](https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-states.jpg)
[<img src="https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-attr.jpg" width="300" />](https://raw.githubusercontent.com/duchu-net/meteo-warnings-poland/main/mwp-attr.jpg)

### Data source

Data comes from [meteo IMGW](https://meteo.imgw.pl/dyn/), with fallowing endpoints:

- [x] [https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/osmet-teryt](https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/osmet-teryt)
- [ ] todo [https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/komet-teryt](https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/komet-teryt)
- [ ] todo [https://meteo.imgw.pl/api/meteo/messages/v1/warnhydro/latest/warn](https://meteo.imgw.pl/api/meteo/messages/v1/warnhydro/latest/warn)

### Config

For your region id check [regions codes](./custom_components/meteo_warnings_poland/const.py)

```yaml
sensor:
  - platform: meteo_warnings_poland
    region_id: "2201"
    name: "Ostrzeżenia pogodowe"
  - platform: meteo_warnings_poland
    region_id: "0601"
    name: "Ostrzeżenia pogodowe"
```

### Links

- [Building a Home Assistant Custom Component](https://aarongodfrey.dev/home%20automation/building_a_home_assistant_custom_component_part_1/)
