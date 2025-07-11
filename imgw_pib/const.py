"""IMDB-PIB constants."""

from datetime import timedelta

from aiohttp import ClientTimeout
from yarl import URL

API_BASE_ENDPOINT = URL("https://danepubliczne.imgw.pl/api/data")
API_HYDROLOGICAL_ENDPOINT = API_BASE_ENDPOINT / "hydro"
API_HYDROLOGICAL_ENDPOINT_2 = API_BASE_ENDPOINT / "hydro2"
API_WEATHER_ENDPOINT = API_BASE_ENDPOINT / "synop"
API_WEATHER_WARNINGS_ENDPOINT = API_BASE_ENDPOINT / "warningsmeteo"
API_HYDROLOGICAL_DETAILS_ENDPOINT = URL(
    "https://hydro-back.imgw.pl/station/hydro/status"
)

HEADERS = {"Content-Type": "application/json"}
TIMEOUT = ClientTimeout(total=20)

DATA_VALIDITY_PERIOD = timedelta(hours=6)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

RIVER_NAMES = {
    "149180010": "Odra",
    "149180020": "Odra",
    "149180030": "Olza",
    "149180040": "Szotkówka",
    "149180050": "Piotrówka",
    "149180060": "Olza",
    "149180070": "Młynówka",
    "149180080": "Wisła",
    "149180100": "Wisła",
    "149180110": "Wisła",
    "149180120": "Brennica",
    "149180130": "Olza",
    "149180140": "Wisła",
    "149180160": "Wisła",
    "149180180": "Biała Wisełka",
    "149180200": "Wisła",
    "149180210": "Wisła",
    "149180220": "Pszczynka",
    "149180230": "Wapienica",
    "149180240": "Wisła",
    "149180250": "Iłownica",
    "149180300": "Odra",
    "149190010": "Biała",
    "149190020": "Bystra",
    "149190030": "Biała",
    "149190040": "Woda Ujsolska",
    "149190050": "Soła",
    "149190060": "Wisła",
    "149190070": "Żylica",
    "149190080": "Soła",
    "149190090": "Żabniczanka",
    "149190100": "Soła",
    "149190120": "Soła",
    "149190140": "Łękawka",
    "149190150": "Koszarawa",
    "149190160": "Wieprzówka",
    "149190170": "Skawa",
    "149190180": "Skawa",
    "149190200": "Stryszawka",
    "149190210": "Skawa",
    "149190220": "Skawica",
    "149190230": "Wisła",
    "149190260": "Skawa",
    "149190270": "Skawinka",
    "149190280": "Dunajec",
    "149190290": "Skawa",
    "149190300": "Kirowa Woda",
    "149190310": "Raba",
    "149190320": "Młyniska",
    "149190340": "Raba",
    "149190350": "Krzczonówka",
    "149190360": "Lepietnica",
    "149190370": "Lubieńka",
    "149190380": "Biały Dunajec",
    "149190390": "Wielki Rogoźnik",
    "149190480": "Paleczka",
    "149190490": "Bystrzanka",
    "149190500": "Wieprzówka",
    "149190510": "Cedron",
    "149200010": "Poroniec",
    "149200020": "Biały Dunajec",
    "149200030": "Dunajec",
    "149200040": "Raba",
    "149200050": "Dunajec",
    "149200060": "Raba",
    "149200080": "Mszanka",
    "149200090": "Raba",
    "149200100": "Białka",
    "149200110": "Białka",
    "149200120": "Niedziczanka",
    "149200130": "Stradomka",
    "149200140": "Dunajec",
    "149200150": "Ochotnica",
    "149200160": "Dunajec",
    "149200170": "Raba",
    "149200180": "Grajcarek",
    "149200190": "Dunajec",
    "149200200": "Łososina",
    "149200220": "Poprad",
    "149200230": "Dunajec",
    "149200240": "Dunajec",
    "149200250": "Kamienica",
    "149200260": "Łubinka",
    "149200270": "Kamienica",
    "149200280": "Dunajec",
    "149200290": "Poprad",
    "149200300": "Poprad",
    "149200310": "Biała",
    "149200320": "Biała",
    "149200330": "Biała",
    "149200520": "Królewski Potok",
    "149200530": "Krzyworzeka",
    "149200540": "Raba",
    "149209990": "Łososina",
    "149210010": "Ropa",
    "149210020": "Sękówka",
    "149210030": "Ropa",
    "149210040": "Wisłoka",
    "149210050": "Wisłoka",
    "149210060": "Ropa",
    "149210070": "Wisłoka",
    "149210080": "Jasiołka",
    "149210090": "Wisłoka",
    "149210100": "Jasiołka",
    "149210110": "Wisłok",
    "149210120": "Stobnica",
    "149210130": "Wisłok",
    "149210140": "Morwawa",
    "149210150": "Wisłok",
    "149210160": "Wisłok",
    "149210180": "Przysłopianka",
    "149210190": "Ropa",
    "149210200": "Zdynia",
    "149210210": "Wisłok",
    "149210450": "Wisłok",
    "149210460": "Odrzechowski",
    "149210470": "Lubatówka",
    "149210480": "Wisłok",
    "149220010": "Pielnica",
    "149220020": "Osława",
    "149220030": "San",
    "149220040": "San",
    "149220050": "Osława",
    "149220060": "San",
    "149220070": "Hoczewka",
    "149220080": "Solinka",
    "149220100": "Solinka",
    "149220110": "Wetlina",
    "149220130": "San",
    "149220140": "Czarna",
    "149220150": "San",
    "149220160": "Wiar",
    "149220170": "Strwiąż",
    "149220180": "Wołosaty",
    "149220190": "San",
    "149220200": "Wiar",
    "149220210": "Wisznia",
    "149229998": "Mleczka",
    "149229999": "Mleczka",
    "149230020": "Szkło",
    "150140010": "Nysa Łużycka",
    "150140020": "Nysa Łużycka",
    "150140030": "Miedzianka",
    "150140100": "Miedzianka",
    "150140140": "Lubota",
    "150150010": "Kwisa",
    "150150020": "Czarny Potok",
    "150150030": "Kamienna",
    "150150040": "Kamienica",
    "150150050": "Kamienna",
    "150150060": "Bóbr",
    "150150070": "Kamienna",
    "150150080": "Bóbr",
    "150150090": "Łomnica",
    "150150100": "Bóbr",
    "150150110": "Jedlica",
    "150150120": "Bóbr",
    "150150130": "Bóbr",
    "150150190": "Podgórna",
    "150150200": "Sośniak",
    "150150230": "Bóbr",
    "150159997": "Złotna",
    "150160010": "Bóbr",
    "150160020": "Pełcznica",
    "150160030": "Strzegomka",
    "150160040": "Klikawa",
    "150160060": "Bystrzyca",
    "150160070": "Bystrzyca",
    "150160080": "Ścinawka",
    "150160090": "Strzegomka",
    "150160100": "Ścinawka",
    "150160110": "Bystrzyca Dusznicka",
    "150160120": "Bystrzyca",
    "150160130": "Piława",
    "150160140": "Piława",
    "150160150": "Bystrzyca",
    "150160160": "Bystrzyca",
    "150160170": "Nysa Kłodzka",
    "150160180": "Nysa Kłodzka",
    "150160190": "Nysa Kłodzka",
    "150160200": "Biała Lądecka",
    "150160210": "Wilczka",
    "150160220": "Nysa Kłodzka",
    "150160230": "Biała Lądecka",
    "150160250": "Ślęza",
    "150160270": "Budzówka",
    "150160280": "Ślęza",
    "150160290": "Czarna Woda",
    "150160330": "Kamienny Potok",
    "150160340": "Włodzica",
    "150160350": "Bystrzyca Dusznicka",
    "150160360": "Duna Dolna",
    "150160370": "Duna Górna",
    "150160380": "Duna Górna",
    "150160390": "Goworówka",
    "150160400": "Nysa Kłodzka",
    "150160410": "Cieszyca",
    "150160420": "Goworówka",
    "150160430": "Bystrzyca",
    "150169999": "Bóbr",
    "150170010": "Oława",
    "150170030": "Oława",
    "150170040": "Odra",
    "150170050": "Biała Głuchołaska",
    "150170060": "Nysa Kłodzka",
    "150170070": "Biała Głuchołaska",
    "150170080": "Złoty Potok",
    "150170090": "Odra",
    "150170100": "Nysa Kłodzka",
    "150170110": "Prudnik",
    "150170120": "Ścinawa Niemodlińska",
    "150170130": "Odra",
    "150170140": "Nysa Kłodzka",
    "150170150": "Stobrawa",
    "150170160": "Opawa",
    "150170170": "Boczne koryto Opawy",
    "150170180": "Osobłoga",
    "150170200": "Bogacica",
    "150170210": "Budkowiczanka",
    "150170220": "Biała",
    "150170240": "Odra",
    "150170290": "Odra",
    "150170320": "Nysa Kłodzka",
    "150170330": "Nysa Kłodzka",
    "150170340": "Świdna",
    "150170350": "Widna",
    "150170360": "Osobłoga",
    "150180010": "Stradunia",
    "150180020": "Mała Panew",
    "150180030": "Odra",
    "150180040": "Psina",
    "150180050": "Mała Panew",
    "150180060": "Odra",
    "150180070": "Kłodnica",
    "150180080": "Bierawka",
    "150180090": "Sumina",
    "150180100": "Mała Panew",
    "150180110": "Ruda",
    "150180130": "Ruda",
    "150180140": "Nacyna",
    "150180150": "Kłodnica",
    "150180160": "Drama",
    "150180170": "Drama",
    "150180190": "Mała Panew",
    "150180210": "Liswarta",
    "150180220": "Kłodnica",
    "150180230": "Stoła",
    "150180250": "Kłodnica",
    "150180270": "Brynica",
    "150180280": "Ruda",
    "150180300": "Gostynia",
    "150180310": "Brynica",
    "150180320": "Kłodnica",
    "150180330": "Ruda",
    "150180340": "Stobrawa",
    "150190010": "Brynica",
    "150190050": "Mleczna",
    "150190060": "Gostynia",
    "150190070": "Brynica",
    "150190080": "Przemsza",
    "150190100": "Biała Przemsza",
    "150190120": "Przemsza",
    "150190130": "Przemsza",
    "150190140": "Wisła",
    "150190150": "Warta",
    "150190160": "Soła",
    "150190170": "Wisła",
    "150190180": "Przemsza",
    "150190190": "Przemsza",
    "150190200": "Warta",
    "150190210": "Mitręga",
    "150190220": "Warta",
    "150190240": "Warta",
    "150190250": "Biała Przemsza",
    "150190260": "Wisła",
    "150190270": "Biała Przemsza",
    "150190280": "Pilica",
    "150190310": "Rudawa",
    "150190330": "Prądnik",
    "150190340": "Wisła",
    "150190350": "Czarna",
    "150190360": "Wisła",
    "150190390": "Stradomka",
    "150190400": "Kucelinka",
    "150190410": "Warta",
    "150190430": "Kamieniczka",
    "150190440": "Warta",
    "150190450": "Boży Stok",
    "150190460": "Ordonka",
    "150190470": "Wiercica",
    "150190480": "Wilga",
    "150200010": "Nida",
    "150200020": "Wierna Rzeka",
    "150200030": "Nida",
    "150200040": "Czarna Nida",
    "150200050": "Mierzawa",
    "150200060": "Wisła",
    "150200070": "Szreniawa",
    "150200080": "Nida",
    "150200090": "Bobrza",
    "150200100": "Wisła",
    "150200120": "Czarna Nida",
    "150200140": "Uszwica",
    "150200150": "Wisła",
    "150200160": "Czarna Nida",
    "150200170": "Dunajec",
    "150200180": "Szreniawa",
    "150200190": "Nidzica",
    "150200200": "Nida",
    "150200210": "Lubrzanka",
    "150200220": "Wisła",
    "150210010": "Czarna",
    "150210020": "Wisła",
    "150210030": "Łagowica",
    "150210040": "Świślina",
    "150210050": "Wschodnia",
    "150210060": "Czarna",
    "150210070": "Breń",
    "150210080": "Świślina",
    "150210090": "Kamienna",
    "150210100": "Czarna",
    "150210110": "Grabinka",
    "150210120": "Wisłoka",
    "150210130": "Wisłoka",
    "150210140": "Brzeźnica",
    "150210150": "Wisła",
    "150210160": "Koprzywianka",
    "150210170": "Wisła",
    "150210180": "Wisła",
    "150210190": "Wisła",
    "150210200": "Łęg",
    "150210210": "San",
    "150210220": "Pokrzywianka",
    "150210410": "Łęg",
    "150220010": "Wisłok",
    "150220020": "Bukowa",
    "150220030": "San",
    "150220040": "Trzebośnica",
    "150220050": "Tanew",
    "150220060": "Mleczka",
    "150220070": "San",
    "150220080": "Wisłok",
    "150220090": "San",
    "150220100": "San",
    "150220110": "Łada",
    "150220120": "Pór",
    "150220130": "Lubaczówka",
    "150220140": "Szkło",
    "150220160": "Tanew",
    "150230010": "Wieprz",
    "150230020": "Wieprz",
    "150230030": "Łabuńka",
    "150230040": "Wieprz",
    "150230050": "Wolica",
    "150230070": "Huczwa",
    "150230080": "Wieprz",
    "150240010": "Bug",
    "150240020": "Bug",
    "151140010": "Nysa Łużycka",
    "151140020": "Lubsza",
    "151140030": "Skroda",
    "151140040": "Nysa Łużycka",
    "151140050": "Witka",
    "151140060": "Nysa Łużycka",
    "151140170": "Nysa Łużycka",
    "151140180": "Nysa Łużycka",
    "151140190": "Lubsza",
    "151140200": "Nysa Łużycka",
    "151150010": "Czerwona Woda",
    "151150020": "Witka",
    "151150030": "Czerna Mała",
    "151150040": "Bóbr",
    "151150050": "Bóbr",
    "151150060": "Kwisa",
    "151150070": "Czerna Wielka",
    "151150080": "Bóbr",
    "151150090": "Kwisa",
    "151150100": "Kwisa",
    "151150110": "Kwisa",
    "151150120": "Bóbr",
    "151150130": "Szprotawa",
    "151150140": "Bóbr",
    "151150150": "Odra",
    "151150160": "Skora",
    "151150170": "Kaczawa",
    "151150180": "Skora",
    "151160020": "Kaczawa",
    "151160030": "Jezioro Sławskie",
    "151160040": "Czarna Woda",
    "151160050": "Kaczawa",
    "151160060": "Odra",
    "151160070": "Nysa Szalona",
    "151160080": "Czarna Woda",
    "151160090": "Nysa Szalona",
    "151160100": "Kaczawa",
    "151160130": "Odra",
    "151160140": "Barycz",
    "151160150": "Odra",
    "151160160": "Polski Rów",
    "151160170": "Odra",
    "151160180": "Strzegomka",
    "151160190": "Bystrzyca",
    "151160200": "Orla",
    "151160220": "Sąsiecznica",
    "151160230": "Ślęza",
    "151160260": "Czernica",
    "151160300": "Barycz",
    "151170010": "Widawa",
    "151170030": "Odra",
    "151170040": "Barycz",
    "151170050": "Widawa",
    "151170060": "Polska Woda",
    "151170070": "Barycz",
    "151170080": "Kuroch",
    "151170090": "Widawa",
    "151170110": "Prosna",
    "151180010": "Ołobok",
    "151180020": "Prosna",
    "151180030": "Niesób",
    "151180040": "Prosna",
    "151180050": "Swędrnia",
    "151180060": "Łużyca",
    "151180070": "Prosna",
    "151180080": "Warta",
    "151180090": "Oleśnica",
    "151180100": "Warta",
    "151180110": "Warta",
    "151180120": "Warta",
    "151180130": "Warta",
    "151180140": "Widawka",
    "151180150": "Nieciecz",
    "151180160": "Ner",
    "151180170": "Widawka",
    "151180180": "Grabia",
    "151180190": "Prosna",
    "151180200": "Żeglina",
    "151180210": "Myja",
    "151180220": "Pichna",
    "151190010": "Liswarta",
    "151190020": "Widawka",
    "151190030": "Grabia",
    "151190060": "Warta",
    "151190070": "Moszczenica",
    "151190080": "Luciąża",
    "151190090": "Pilica",
    "151190100": "Pilica",
    "151190110": "Wolbórka",
    "151190120": "Czarna",
    "151190130": "Ner",
    "151200020": "Pilica",
    "151200040": "Drzewiczka",
    "151200080": "Drzewiczka",
    "151200090": "Pilica",
    "151200100": "Kamienna",
    "151200110": "Radomka",
    "151200120": "Pilica",
    "151210010": "Kamienna",
    "151210020": "Kamienna",
    "151210040": "Kamienna",
    "151210050": "Wisła",
    "151210060": "Radomka",
    "151210070": "Wilga",
    "151210080": "Iłżanka",
    "151210090": "Kamienna",
    "151210100": "Wilga",
    "151210110": "Okrzejka",
    "151210120": "Wisła",
    "151210130": "Wyżnica",
    "151210190": "Wisła",
    "151210220": "Wisła",
    "151220010": "Wieprz",
    "151220040": "Kurówka",
    "151220050": "Minina",
    "151220070": "Bystrzyca",
    "151220080": "Tyśmienica",
    "151220090": "Wieprz",
    "151220100": "Bystrzyca",
    "151220110": "Tyśmienica",
    "151220120": "Piwonia",
    "151220130": "Giełczewka",
    "151220150": "Bystrzyca",
    "151230010": "Wieprz",
    "151230020": "Muława",
    "151230030": "Włodawka",
    "151230040": "Bug",
    "151230050": "Uherka",
    "151230060": "Bug",
    "152140010": "Odra",
    "152140020": "Odra",
    "152140030": "Jezioro Morzycko",
    "152140050": "Odra",
    "152140060": "Odra",
    "152140070": "Warta",
    "152140080": "Ilanka",
    "152140090": "Odra",
    "152140100": "Myśla",
    "152140110": "Pliszka",
    "152140120": "Myśla",
    "152140130": "Odra",
    "152150010": "Warta",
    "152150020": "Bóbr",
    "152150040": "Warta",
    "152150050": "Odra",
    "152150060": "Jezioro Niesłysz",
    "152150080": "Warta",
    "152150090": "Noteć",
    "152150100": "Obra",
    "152150110": "Warta",
    "152150130": "Odra",
    "152150140": "Noteć",
    "152150150": "Jezioro Żabie",
    "152150180": "Mierzęcka Struga",
    "152150190": "Noteć",
    "152150200": "Warta",
    "152150220": "Obra",
    "152150230": "Miała",
    "152150240": "Drawa",
    "152160010": "Noteć",
    "152160050": "Warta",
    "152160060": "Mogilnica",
    "152160070": "Noteć",
    "152160080": "Sama",
    "152160090": "Kanał Mosiński",
    "152160100": "Warta",
    "152160110": "Wełna",
    "152160130": "Kanał Mosiński",
    "152160140": "Warta",
    "152160150": "Kopel",
    "152170010": "Warta",
    "152170030": "Główna",
    "152170040": "Wełna",
    "152170060": "Warta",
    "152170080": "Warta",
    "152170120": "Wrześnica",
    "152170130": "Warta",
    "152170140": "Jezioro Powidzkie",
    "152170150": "Czarna Struga",
    "152179994": "Lutynia",
    "152180010": "Noteć Zachodnia",
    "152180020": "Panna",
    "152180030": "Noteć",
    "152180050": "Warta",
    "152180060": "Powa",
    "152180090": "Noteć",
    "152180100": "Noteć",
    "152180110": "Kiełbaska Duża",
    "152180120": "Warta",
    "152180130": "Tążyna",
    "152180140": "Rgilewka",
    "152180150": "Ner",
    "152180160": "Kanał Ślesiński",
    "152180180": "Pichna",
    "152190030": "Wisła",
    "152190050": "Bzura",
    "152190100": "Mroga",
    "152190110": "Sierpienica",
    "152190120": "Wisła",
    "152190160": "Skrwa",
    "152199992": "Bzura",
    "152199997": "Ochnia",
    "152200010": "Rawka",
    "152200020": "Wkra",
    "152200030": "Wisła",
    "152200050": "Bzura",
    "152200070": "Łasica",
    "152200080": "Płonka",
    "152200090": "Utrata",
    "152200100": "Łydynia",
    "152200110": "Wisła",
    "152200120": "Wkra",
    "152200130": "Narew",
    "152200150": "Wisła",
    "152209994": "Sona",
    "152209996": "Wkra",
    "152209997": "Pisia Gągolina",
    "152210020": "Jeziorka",
    "152210030": "Orzyc",
    "152210040": "Wisła",
    "152210060": "Narew",
    "152210070": "Świder",
    "152210090": "Bug",
    "152210100": "Orz",
    "152210110": "Osownica",
    "152210120": "Liwiec",
    "152210130": "Brok",
    "152210140": "Kostrzyń",
    "152210150": "Bug",
    "152210170": "Wisła",
    "152210180": "Narew",
    "152219993": "Narew",
    "152219996": "Długa",
    "152220010": "Liwiec",
    "152220050": "Bug",
    "152220060": "Toczna",
    "152220070": "Nurzec",
    "152220080": "Narew",
    "152220100": "Nurzec",
    "152229999": "Bug",
    "152230010": "Nurzec",
    "152230020": "Krzna",
    "152230030": "Orlanka",
    "152230040": "Narew",
    "152230050": "Zielawa",
    "152230060": "Rudnia",
    "152230070": "Krzna",
    "152230080": "Bug",
    "152230090": "Narew",
    "152230100": "Narewka",
    "152230110": "Narew",
    "152230120": "Narew",
    "152230190": "Narewka",
    "152230200": "Bug",
    "153140010": "Bałtyk",
    "153140020": "Odra",
    "153140030": "Odra",
    "153140040": "Zalew Szczeciński",
    "153140050": "Odra",
    "153140060": "Cieśnina Dziwna",
    "153140070": "Bałtyk",
    "153140080": "Gowienica",
    "153140090": "Ina",
    "153140100": "Płonia",
    "153140110": "Płonia",
    "153140190": "Regalica",
    "153140200": "Jezioro Miedwie",
    "153150010": "Ina",
    "153150020": "Mała Ina",
    "153150030": "Sąpólna",
    "153150040": "Krąpiel",
    "153150050": "Rega",
    "153150060": "Jezioro Ińsko",
    "153150080": "Rega",
    "153150090": "Rega",
    "153150100": "Drawa",
    "153150120": "Drawa",
    "153150140": "Jezioro Lubie",
    "153150160": "Jezioro Ostrowite",
    "153150190": "Mołstowa",
    "153160020": "Parsęta",
    "153160030": "Drawa",
    "153160040": "Jezioro Drawsko",
    "153160050": "Jezioro Komorze",
    "153160060": "Jezioro Bytyń Wielki",
    "153160070": "Piława",
    "153160080": "Parsęta",
    "153160110": "Dobrzyca",
    "153160160": "Noteć",
    "153160170": "Noteć",
    "153160180": "Gwda",
    "153160190": "Piława",
    "153160200": "Gwda",
    "153160210": "Gwda",
    "153160250": "Czarna",
    "153160260": "Czernica",
    "153170010": "Noteć",
    "153170020": "Jezioro Sławianowskie",
    "153170040": "Łobżonka",
    "153170050": "Brda",
    "153170060": "Brda",
    "153170070": "Zbrzyca",
    "153170080": "Jezioro Charzykowskie",
    "153170090": "Jezioro Sępoleńskie",
    "153170100": "Noteć",
    "153170110": "Sępolna",
    "153170120": "Brda",
    "153170130": "Jezioro Wdzydze",
    "153170140": "Brda",
    "153179996": "Chocina",
    "153180010": "Wda",
    "153180020": "Wisła",
    "153180030": "Wierzyca",
    "153180040": "Prusina",
    "153180050": "Wda",
    "153180060": "Wda",
    "153180080": "Wisła",
    "153180090": "Wisła",
    "153180100": "Wisła",
    "153180110": "Wierzyca",
    "153180120": "Bałtyk",
    "153180130": "Liwa",
    "153180140": "Drwęca",
    "153180150": "Osa",
    "153190010": "Lutryna",
    "153190020": "Osa",
    "153190030": "Jezioro Dzierzgoń",
    "153190040": "Elbląg",
    "153190050": "Drwęca",
    "153190070": "Jezioro Bachotek",
    "153190080": "Jezioro Jeziorak",
    "153190090": "Drwęca",
    "153190100": "Iławka",
    "153190120": "Drwęca",
    "153190130": "Wel",
    "153190140": "Drwęca",
    "153190150": "Wel",
    "153190170": "Jezioro Drwęckie",
    "153190180": "Skarlanka",
    "153190190": "Skarlanka",
    "153200010": "Drwęca",
    "153200020": "Mławka",
    "153200030": "Pasłęka",
    "153200040": "Pasłęka",
    "153200050": "Szkotówka",
    "153200070": "Łyna",
    "153200090": "Jezioro Wadąg",
    "153200140": "Jezioro Dadaj",
    "153200160": "Sawica",
    "153210010": "Omulew",
    "153210020": "Orzyc",
    "153210040": "Rozoga",
    "153210050": "Krutynia",
    "153210070": "Omulew",
    "153210090": "Narew",
    "153210100": "Jezioro Nidzkie",
    "153210120": "Rozoga",
    "153210130": "Jezioro Śniardwy",
    "153210140": "Szkwa",
    "153210170": "Pisa",
    "153210180": "Ruż",
    "153210190": "Pisa",
    "153210200": "Jezioro Roś",
    "153210210": "Narew",
    "153210220": "Pisa",
    "153220010": "Narew",
    "153220050": "Jezioro Ełckie",
    "153220060": "Ełk",
    "153220070": "Narew",
    "153220080": "Ełk",
    "153220090": "Wissa",
    "153220100": "Biebrza",
    "153220110": "Lega",
    "153220120": "Jezioro Selmęt Wielki",
    "153220130": "Narew",
    "153220140": "Ełk",
    "153220150": "Lega",
    "153220160": "Ełk",
    "153220170": "Biebrza",
    "153220180": "Ślina",
    "153220190": "Jezioro Rajgrodzkie",
    "153220200": "Lega",
    "153220220": "Lega",
    "153220230": "Nereśl",
    "153220240": "Netta",
    "153220250": "Biebrza",
    "153220260": "Biebrza",
    "153220270": "Narew",
    "153220280": "Netta",
    "153220290": "Blizna",
    "153220310": "Kanał Kuwasy",
    "153230010": "Supraśl",
    "153230020": "Brzozówka",
    "153230040": "Jezioro Białe Augustowskie",
    "153230050": "Jezioro Studzieniczne",
    "153230060": "Biała",
    "153230070": "Biebrza",
    "153230080": "Czarna",
    "153230110": "Supraśl",
    "153230120": "Czarna Hańcza",
    "153230130": "Sidra",
    "153230140": "Sokołda",
    "153230160": "Supraśl",
    "153230170": "Supraśl",
    "154150010": "Rega",
    "154150030": "Bałtyk",
    "154150040": "Parsęta",
    "154150050": "Parsęta",
    "154150060": "Parsęta",
    "154150070": "Parsęta",
    "154150080": "Rega",
    "154160010": "Jezioro Jamno",
    "154160020": "Radew",
    "154160030": "Dzierżęcinka",
    "154160060": "Grabowa",
    "154160070": "Wieprza",
    "154160080": "Radew",
    "154160090": "Grabowa",
    "154160100": "Moszczeniczka",
    "154160110": "Bałtyk",
    "154160120": "Wieprza",
    "154160130": "Studnica",
    "154160140": "Słupia",
    "154160150": "Bałtyk",
    "154160160": "Wieprza",
    "154169997": "Wieprza",
    "154170010": "Słupia",
    "154170020": "Glaźna",
    "154170030": "Skotawa",
    "154170040": "Wieprza",
    "154170060": "Łupawa",
    "154170070": "Słupia",
    "154170080": "Łupawa",
    "154170090": "Jezioro Łebsko",
    "154170100": "Bałtyk",
    "154170110": "Łeba",
    "154170120": "Słupia",
    "154170130": "Pogorzelica",
    "154170140": "Jezioro Jasień Południe",
    "154170150": "Łupawa",
    "154170160": "Łeba",
    "154170180": "Wda",
    "154170190": "Jezioro Raduńskie Górne",
    "154170230": "Łupawa",
    "154170240": "Borucinka",
    "154170320": "Darżyńska Struga",
    "154170330": "Bałtyk",
    "154170340": "Słupia",
    "154179991": "Radunia",
    "154179998": "Łupawa",
    "154180010": "Wierzyca",
    "154180020": "Łeba",
    "154180030": "Reda",
    "154180040": "Jezioro Ostrzyckie",
    "154180050": "Piaśnica",
    "154180060": "Radunia",
    "154180070": "Bolszewka",
    "154180080": "Reda",
    "154180090": "Bałtyk",
    "154180100": "Bałtyk",
    "154180110": "Wierzyca",
    "154180120": "Bałtyk",
    "154180140": "Bałtyk",
    "154180150": "Wisła",
    "154180160": "Martwa Wisła",
    "154180170": "Motława",
    "154180180": "Bielawa",
    "154180190": "Wisła",
    "154180200": "Wisła",
    "154180210": "Wisła",
    "154180220": "Wisła",
    "154180230": "Radunia",
    "154180260": "Kanał Raduński",
    "154180270": "Radunia",
    "154180280": "Bałtyk",
    "154180290": "Reda",
    "154180300": "Wietcisa",
    "154190010": "Tuja",
    "154190020": "Szkarpawa",
    "154190030": "Zalew Wiślany",
    "154190040": "Nogat",
    "154190050": "Zalew Wiślany",
    "154190060": "Elbląg",
    "154190070": "Zalew Wiślany",
    "154190080": "Jezioro Druzno",
    "154190090": "Zalew Wiślany",
    "154190100": "Wąska",
    "154190110": "Bauda",
    "154190130": "Zalew Wiślany",
    "154190140": "Pasłęka",
    "154190150": "Pasłęka",
    "154190160": "Pasłęka",
    "154190170": "Pasłęka",
    "154190180": "Bałtyk",
    "154200010": "Wałsza",
    "154200020": "Drwęca Warmińska",
    "154200030": "Łyna",
    "154200040": "Elma",
    "154209999": "Pasłęka",
    "154210010": "Łyna",
    "154210020": "Guber",
    "154210030": "Sajna",
    "154210060": "Jezioro Mamry",
    "154210070": "Węgorapa",
    "154210080": "Węgorapa",
    "154210090": "Pisa",
    "154210100": "Węgorapa",
    "154210110": "Dejna",
    "154220010": "Gołdapa",
    "154220020": "Jezioro Litygajno",
    "154220030": "Ełk",
    "154220050": "Gołdapa",
    "154220070": "Jezioro Rospuda Filipowska",
    "154220080": "Jezioro Hańcza",
    "154220090": "Czarna Hańcza",
    "154220100": "Szeszupa",
    "154220110": "Gołdapa",
    "154230010": "Szeszupa",
    "154230020": "Jezioro Wigry",
    "154230030": "Czarna Hańcza",
    "154230040": "Marycha",
    "250161110": "Ścinawka",
}
ID_TO_TERYT_MAP = {
    "12295": "2061",  # Białystok
    "12600": "2461",  # Bielsko-Biała
    "12235": "2202",  # Chojnice
    "12550": "2464",  # Częstochowa
    "12160": "2861",  # Elbląg
    "12155": "2261",  # Gdańsk
    "12135": "2211",  # Hel
    "12500": "0261",  # Jelenia Góra
    "12435": "3061",  # Kalisz
    "12560": "2469",  # Katowice
    "12185": "2808",  # Kętrzyn
    "12570": "2661",  # Kielce
    "12520": "0208",  # Kłodzko
    "12345": "3009",  # Koło
    "12100": "3208",  # Kołobrzeg
    "12105": "3261",  # Koszalin
    "12488": "1407",  # Kozienice
    "12566": "1261",  # Kraków
    "12670": "1861",  # Krosno
    "12415": "0262",  # Legnica
    "12690": "1821",  # Lesko
    "12418": "3063",  # Leszno
    "12125": "2208",  # Lębork
    "12495": "0663",  # Lublin
    "12120": "2208",  # Łeba
    "12465": "1061",  # Łódź
    "12280": "2810",  # Mikołajki
    "12270": "1413",  # Mława
    "12660": "1262",  # Nowy Sącz
    "12530": "1661",  # Opole
    "12285": "1461",  # Ostrołęka
    "12230": "3019",  # Piła
    "12360": "1462",  # Płock
    "12330": "3064",  # Poznań
    "12695": "1862",  # Przemyśl
    "12540": "2411",  # Racibórz
    "12210": "3218",  # Resko
    "12580": "1863",  # Rzeszów
    "12585": "2609",  # Sandomierz
    "12385": "1464",  # Siedlce
    "12310": "0805",  # Słubice
    "12469": "1010",  # Sulejów
    "12195": "2063",  # Suwałki
    "12205": "3262",  # Szczecin
    "12215": "3215",  # Szczecinek
    "12200": "3263",  # Świnoujście
    "12575": "1263",  # Tarnów
    "12399": "0601",  # Terespol
    "12250": "0463",  # Toruń
    "12115": "2212",  # Ustka
    "12375": "1465",  # Warszawa
    "12455": "1017",  # Wieluń
    "12497": "0619",  # Włodawa
    "12424": "0264",  # Wrocław
    "12625": "1217",  # Zakopane
    "12595": "0664",  # Zamość
    "12400": "0862",  # Zielona Góra
}

WEATHER_ALERTS_MAP = {
    "intensywne opady deszczu": "heavy_rainfall",
    "silny wiatr": "strong_wind",
}
ALERT_LEVEL_MAP = {
    "1": "yellow",
    "2": "orange",
    "3": "red",
}
