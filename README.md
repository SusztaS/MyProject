# Karateverseny sorsolás

## Hallgatói adatok

- Hallgató neve: Suszta Sándor
- Neptun-kód: wx72tx

## Feladat rövid leírása

A program a jelentkezési CSV-fájlban szereplő kumite- és kata-versenyzőket a `Tournament` oszlopban megadott kategóriák szerint csoportosítja. Egyetlen művelettel minden kategóriában véletlenszerűen elkészíti az első mérkőzés párosításait, majd az eredményt a grafikus felületen kategóriánként megjeleníti. A sorsolás külön CSV-fájlba menthető.

A program csak a kezdeti sorsolást végzi el. Nem kezeli a mérkőzések eredményeit és a továbbjutást.

## Fájlok és modulok

- `main.py`: a program indítása, a Tkinter grafikus felület, a CSV betöltését, a sorsolást és a mentést indító eseménykezelők.
- `ss_sorsolas.py`: saját modul, amely tartalmazza a versenyző osztályát, a CSV beolvasását, a kategóriánkénti sorsolást és az eredmény mentését.
- `Competitors.csv`: minta jelentkezési lista.

## Saját osztály

- `SSVersenyzo`: egy versenyző adatait tárolja, többek között a nevét, klubját és kategóriáját.

## Saját függvények

- `ss_csv_beolvasasa()`: ellenőrzi a CSV fejlécét, és létrehozza a versenyzőobjektumokat.
- `ss_sorsolas_keszitese()`: minden kategóriában megkeveri a versenyzőket, majd párokra bontja őket.
- `ss_eredmeny_csv_mentese()`: CSV-fájlba menti a kisorsolt párokat és a pár nélkül maradó versenyzőket.
- `ss_kimenet_frissitese()`: frissíti a grafikus felület eredménymezőjét.
- `ss_csv_betoltese()`: eseménykezelő, amely kiválasztja és betölti a jelentkezési CSV-fájlt.
- `ss_sorsolas_inditasa()`: eseménykezelő, amely minden kategóriában elkészíti a sorsolást.
- `ss_eredmeny_mentese()`: eseménykezelő, amely elindítja a sorsolás mentését.

## Használt modulok és függvények

- `csv.Sniffer().sniff()`: megpróbálja felismerni a CSV formátumát.
- `csv.reader()`: beolvassa és ellenőrzi a fejlécet.
- `csv.DictReader()`: a sorokat fejléc alapján, mezőnevekkel olvassa be.
- `csv.writer()`: elmenti a sorsolási eredményeket.
- `random.shuffle()`: véletlenszerű sorrendbe rendezi az adott kategória versenyzőit.
- `tkinter` és `tkinter.ttk`: létrehozza a grafikus ablakot és a vezérlőelemeket.
## Fontos működési szabály

Ha egy kategóriában páratlan a versenyzők száma, egy versenyző pár nélkül marad, és „Pár nélkül / erőnyerő” jelöléssel jelenik meg. Az alkalmazás minden versenyzőt pontosan egyszer vesz figyelembe az adott sorsolásban.
