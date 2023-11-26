from datetime import timedelta
from typing import Final
from homeassistant.const import Platform

CONF_NANE = "name"
CONF_REGION_ID = "region_id"

DOMAIN: Final = "meteo_warnings_poland"
ATTRIBUTION = "Information provided by IMGW."
DEFAULT_NAME: Final = "Ostrzeżenia"
MIN_UPDATE_INTERVAL: Final = timedelta(minutes=10)
DEFAULT_UPDATE_INTERVAL: Final = timedelta(minutes=15)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]

WARNING_TYPES = {
    # "-2": ["none", "mdi:check-circle", "Ostrzeżenie - Brak ostrzeżeń"],
    # "-1": [
    #     "info",
    #     "mdi:waves",
    #     "Ostrzeżenie przed suszą hydrologiczną",
    #     "Ostrzeżenie przed suszą hydrologiczną aktywne",
    #     "Ostrzeżenie hydrologiczne",
    # ],
    # "0": ["none", "mdi:check-circle", "Ostrzeżenie - brak ostrzeżeń"],
    "1": [
        "medium",
        "mdi:numeric-1-box",
        "Ostrzeżenie 1 stopnia",
        "Ostrzeżenie 1 aktywne",
        "Stopień 1",
    ],
    "2": [
        "severity",
        "mdi:numeric-2-box",
        "Ostrzeżenie 2 stopnia",
        "Ostrzeżenie 2 stopnia aktywne",
        "Stopień 2",
    ],
    "3": [
        "extreme",
        "mdi:numeric-3-box",
        "Ostrzeżenie 3 stopnia",
        "Ostrzeżenie 3 stopnia aktywne",
        "Stopień 3",
    ],
}
WARNING_CODES = {
    "OB": ["Oblodzenie", "Icing"],
    "IS": ["Intensywne opady śniegu", "Heavy snow"],
    "SH": ["SUSZA HYDROLOGICZNA", "-"],
    "W_PSO": ["WEZBRANIE Z PRZEKROCZENIEM STANOW OSTRZEGAWCZYCH", "-"],
}

REGIONS = {
    "0201": "bolesławiecki",
    "0202": "dzierżoniowski",
    "0203": "głogowski",
    "0204": "górowski",
    "0205": "jaworski",
    "0206": "jeleniogórski",
    "0207": "kamiennogórski",
    "0208": "kłodzki",
    "0209": "legnicki",
    "0210": "lubański",
    "0211": "lubiński",
    "0212": "lwówecki",
    "0213": "milicki",
    "0214": "oleśnicki",
    "0215": "oławski",
    "0216": "polkowicki",
    "0217": "strzeliński",
    "0218": "średzki",
    "0219": "świdnicki",
    "0220": "trzebnicki",
    "0221": "wałbrzyski",
    "0222": "wołowski",
    "0223": "wrocławski",
    "0224": "ząbkowicki",
    "0225": "zgorzelecki",
    "0226": "złotoryjski",
    "0261": "Jelenia Góra",
    "0262": "Legnica",
    "0264": "Wrocław",
    "0265": "Wałbrzych",
    "0401": "aleksandrowski",
    "0402": "brodnicki",
    "0403": "bydgoski",
    "0404": "chełmiński",
    "0405": "golubsko-dobrzyński",
    "0406": "grudziądzki",
    "0407": "inowrocławski",
    "0408": "lipnowski",
    "0409": "mogileński",
    "0410": "nakielski",
    "0411": "radziejowski",
    "0412": "rypiński",
    "0413": "sępoleński",
    "0414": "świecki",
    "0415": "toruński",
    "0416": "tucholski",
    "0417": "wąbrzeski",
    "0418": "włocławski",
    "0419": "żniński",
    "0461": "Bydgoszcz",
    "0462": "Grudziądz",
    "0463": "Toruń",
    "0464": "Włocławek",
    "0601": "bialski",
    "0602": "biłgorajski",
    "0603": "chełmski",
    "0604": "hrubieszowski",
    "0605": "janowski",
    "0606": "krasnostawski",
    "0607": "kraśnicki",
    "0608": "lubartowski",
    "0609": "lubelski",
    "0610": "łęczyński",
    "0611": "łukowski",
    "0612": "opolski",
    "0613": "parczewski",
    "0614": "puławski",
    "0615": "radzyński",
    "0616": "rycki",
    "0617": "świdnicki",
    "0618": "tomaszowski",
    "0619": "włodawski",
    "0620": "zamojski",
    "0661": "Biała Podlaska",
    "0662": "Chełm",
    "0663": "Lublin",
    "0664": "Zamość",
    "0801": "gorzowski",
    "0802": "krośnieński",
    "0803": "międzyrzecki",
    "0804": "nowosolski",
    "0805": "słubicki",
    "0806": "strzelecko-drezdenecki",
    "0807": "sulęciński",
    "0808": "świebodziński",
    "0809": "zielonogórski",
    "0810": "żagański",
    "0811": "żarski",
    "0812": "wschowski",
    "0861": "Gorzów Wielkopolski",
    "0862": "Zielona Góra",
    "1001": "bełchatowski",
    "1002": "kutnowski",
    "1003": "łaski",
    "1004": "łęczycki",
    "1005": "łowicki",
    "1006": "łódzki wschodni",
    "1007": "opoczyński",
    "1008": "pabianicki",
    "1009": "pajęczański",
    "1010": "piotrkowski",
    "1011": "poddębicki",
    "1012": "radomszczański",
    "1013": "rawski",
    "1014": "sieradzki",
    "1015": "skierniewicki",
    "1016": "tomaszowski",
    "1017": "wieluński",
    "1018": "wieruszowski",
    "1019": "zduńskowolski",
    "1020": "zgierski",
    "1021": "brzeziński",
    "1061": "Łódź",
    "1062": "Piotrków Trybunalski",
    "1063": "Skierniewice",
    "1201": "bocheński",
    "1202": "brzeski",
    "1203": "chrzanowski",
    "1204": "dąbrowski",
    "1205": "gorlicki",
    "1206": "krakowski",
    "1207": "limanowski",
    "1208": "miechowski",
    "1209": "myślenicki",
    "1210": "nowosądecki",
    "1211": "nowotarski",
    "1212": "olkuski",
    "1213": "oświęcimski",
    "1214": "proszowicki",
    "1215": "suski",
    "1216": "tarnowski",
    "1217": "tatrzański",
    "1218": "wadowicki",
    "1219": "wielicki",
    "1261": "Kraków",
    "1262": "Nowy Sącz",
    "1263": "Tarnów",
    "1401": "białobrzeski",
    "1402": "ciechanowski",
    "1403": "garwoliński",
    "1404": "gostyniński",
    "1405": "grodziski",
    "1406": "grójecki",
    "1407": "kozienicki",
    "1408": "legionowski",
    "1409": "lipski",
    "1410": "łosicki",
    "1411": "makowski",
    "1412": "miński",
    "1413": "mławski",
    "1414": "nowodworski",
    "1415": "ostrołęcki",
    "1416": "ostrowski",
    "1417": "otwocki",
    "1418": "piaseczyński",
    "1419": "płocki",
    "1420": "płoński",
    "1421": "pruszkowski",
    "1422": "przasnyski",
    "1423": "przysuski",
    "1424": "pułtuski",
    "1425": "radomski",
    "1426": "siedlecki",
    "1427": "sierpecki",
    "1428": "sochaczewski",
    "1429": "sokołowski",
    "1430": "szydłowiecki",
    "1432": "warszawski zachodni",
    "1433": "węgrowski",
    "1434": "wołomiński",
    "1435": "wyszkowski",
    "1436": "zwoleński",
    "1437": "żuromiński",
    "1438": "żyrardowski",
    "1461": "Ostrołęka",
    "1462": "Płock",
    "1463": "Radom",
    "1464": "Siedlce",
    "1465": "Warszawa",
    "1601": "brzeski",
    "1602": "głubczycki",
    "1603": "kędzierzyńsko-kozielski",
    "1604": "kluczborski",
    "1605": "krapkowicki",
    "1606": "namysłowski",
    "1607": "nyski",
    "1608": "oleski",
    "1609": "opolski",
    "1610": "prudnicki",
    "1611": "strzelecki",
    "1661": "Opole",
    "1801": "bieszczadzki",
    "1802": "brzozowski",
    "1803": "dębicki",
    "1804": "jarosławski",
    "1805": "jasielski",
    "1806": "kolbuszowski",
    "1807": "krośnieński",
    "1808": "leżajski",
    "1809": "lubaczowski",
    "1810": "łańcucki",
    "1811": "mielecki",
    "1812": "niżański",
    "1813": "przemyski",
    "1814": "przeworski",
    "1815": "ropczycko-sędziszowski",
    "1816": "rzeszowski",
    "1817": "sanocki",
    "1818": "stalowowolski",
    "1819": "strzyżowski",
    "1820": "tarnobrzeski",
    "1821": "leski",
    "1861": "Krosno",
    "1862": "Przemyśl",
    "1863": "Rzeszów",
    "1864": "Tarnobrzeg",
    "2001": "augustowski",
    "2002": "białostocki",
    "2003": "bielski",
    "2004": "grajewski",
    "2005": "hajnowski",
    "2006": "kolneński",
    "2007": "łomżyński",
    "2008": "moniecki",
    "2009": "sejneński",
    "2010": "siemiatycki",
    "2011": "sokólski",
    "2012": "suwalski",
    "2013": "wysokomazowiecki",
    "2014": "zambrowski",
    "2061": "Białystok",
    "2062": "Łomża",
    "2063": "Suwałki",
    "2201": "bytowski",
    "2202": "chojnicki",
    "2203": "człuchowski",
    "2204": "gdański",
    "2205": "kartuski",
    "2206": "kościerski",
    "2207": "kwidzyński",
    "2208": "lęborski",
    "2209": "malborski",
    "2210": "nowodworski",
    "2211": "pucki",
    "2212": "słupski",
    "2213": "starogardzki",
    "2214": "tczewski",
    "2215": "wejherowski",
    "2216": "sztumski",
    "2261": "Gdańsk",
    "2262": "Gdynia",
    "2263": "Słupsk",
    "2264": "Sopot",
    "2401": "będziński",
    "2402": "bielski",
    "2403": "cieszyński",
    "2404": "częstochowski",
    "2405": "gliwicki",
    "2406": "kłobucki",
    "2407": "lubliniecki",
    "2408": "mikołowski",
    "2409": "myszkowski",
    "2410": "pszczyński",
    "2411": "raciborski",
    "2412": "rybnicki",
    "2413": "tarnogórski",
    "2414": "bieruńsko-lędziński",
    "2415": "wodzisławski",
    "2416": "zawierciański",
    "2417": "żywiecki",
    "2461": "Bielsko-Biała",
    "2462": "Bytom",
    "2463": "Chorzów",
    "2464": "Częstochowa",
    "2465": "Dąbrowa Górnicza",
    "2466": "Gliwice",
    "2467": "Jastrzębie-Zdrój",
    "2468": "Jaworzno",
    "2469": "Katowice",
    "2470": "Mysłowice",
    "2471": "Piekary Śląskie",
    "2472": "Ruda Śląska",
    "2473": "Rybnik",
    "2474": "Siemianowice Śląskie",
    "2475": "Sosnowiec",
    "2476": "Świętochłowice",
    "2477": "Tychy",
    "2478": "Zabrze",
    "2479": "Żory",
    "2601": "buski",
    "2602": "jędrzejowski",
    "2603": "kazimierski",
    "2604": "kielecki",
    "2605": "konecki",
    "2606": "opatowski",
    "2607": "ostrowiecki",
    "2608": "pińczowski",
    "2609": "sandomierski",
    "2610": "skarżyski",
    "2611": "starachowicki",
    "2612": "staszowski",
    "2613": "włoszczowski",
    "2661": "Kielce",
    "2801": "bartoszycki",
    "2802": "braniewski",
    "2803": "działdowski",
    "2804": "elbląski",
    "2805": "ełcki",
    "2806": "giżycki",
    "2807": "iławski",
    "2808": "kętrzyński",
    "2809": "lidzbarski",
    "2810": "mrągowski",
    "2811": "nidzicki",
    "2812": "nowomiejski",
    "2813": "olecki",
    "2814": "olsztyński",
    "2815": "ostródzki",
    "2816": "piski",
    "2817": "szczycieński",
    "2818": "gołdapski",
    "2819": "węgorzewski",
    "2861": "Elbląg",
    "2862": "Olsztyn",
    "3001": "chodzieski",
    "3002": "czarnkowsko-trzcianecki",
    "3003": "gnieźnieński",
    "3004": "gostyński",
    "3005": "grodziski",
    "3006": "jarociński",
    "3007": "kaliski",
    "3008": "kępiński",
    "3009": "kolski",
    "3010": "koniński",
    "3011": "kościański",
    "3012": "krotoszyński",
    "3013": "leszczyński",
    "3014": "międzychodzki",
    "3015": "nowotomyski",
    "3016": "obornicki",
    "3017": "ostrowski",
    "3018": "ostrzeszowski",
    "3019": "pilski",
    "3020": "pleszewski",
    "3021": "poznański",
    "3022": "rawicki",
    "3023": "słupecki",
    "3024": "szamotulski",
    "3025": "średzki",
    "3026": "śremski",
    "3027": "turecki",
    "3028": "wągrowiecki",
    "3029": "wolsztyński",
    "3030": "wrzesiński",
    "3031": "złotowski",
    "3061": "Kalisz",
    "3062": "Konin",
    "3063": "Leszno",
    "3064": "Poznań",
    "3201": "białogardzki",
    "3202": "choszczeński",
    "3203": "drawski",
    "3204": "goleniowski",
    "3205": "gryficki",
    "3206": "gryfiński",
    "3207": "kamieński",
    "3208": "kołobrzeski",
    "3209": "koszaliński",
    "3210": "myśliborski",
    "3211": "policki",
    "3212": "pyrzycki",
    "3213": "sławieński",
    "3214": "stargardzki",
    "3215": "szczecinecki",
    "3216": "świdwiński",
    "3217": "wałecki",
    "3218": "łobeski",
    "3261": "Koszalin",
    "3262": "Szczecin",
    "3263": "Świnoujście",
}
