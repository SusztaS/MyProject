import csv
import random


class SSVersenyzo:
    def __init__(self, adatok):
        self.keresztnev = adatok["FirstName"].strip()
        self.vezeteknev = adatok["FamilyName"].strip()
        self.klub = adatok["ClubName"].strip()
        self.kategoria = adatok["Tournament"].strip()
        self.szuletesi_datum = adatok["DateOfBirth"].strip()
        self.nem = adatok["Gender"].strip()
        self.orvosi_vizsgalat = adatok["DateOfMedicalExamination"].strip()

    @property
    def nev(self):
        return f"{self.vezeteknev} {self.keresztnev}".strip()


def ss_csv_beolvasasa(fajl_utvonal):
    kotelezo_oszlopok = {
        "FirstName",
        "FamilyName",
        "ClubName",
        "Tournament",
        "DateOfBirth",
        "Gender",
        "DateOfMedicalExamination",
    }

    with open(fajl_utvonal, "r", encoding="utf-8-sig", newline="") as fajl:
        minta = fajl.read(4096)
        fajl.seek(0)

        try:
            formatum = csv.Sniffer().sniff(minta)
        except csv.Error:
            formatum = csv.excel

        fejlec_olvaso = csv.reader(fajl, dialect=formatum)
        fejlec = next(fejlec_olvaso, None)

        if not fejlec:
            raise ValueError("A CSV-fájl üres.")

        hianyzo_oszlopok = kotelezo_oszlopok.difference(fejlec)
        if hianyzo_oszlopok:
            hianyzo = ", ".join(sorted(hianyzo_oszlopok))
            raise ValueError(f"Hiányzó oszlopok a CSV-fájlban: {hianyzo}")

        fajl.seek(0)
        olvaso = csv.DictReader(fajl, dialect=formatum)
        versenyzok = []

        for sor in olvaso:
            if not any((ertek or "").strip() for ertek in sor.values() if ertek is not None):
                continue
            versenyzok.append(SSVersenyzo(sor))

    if not versenyzok:
        raise ValueError("A CSV-fájl nem tartalmaz versenyzőket.")

    return versenyzok


def ss_sorsolas_keszitese(versenyzok):
    kategoriak = {}

    for versenyzo in versenyzok:
        kategoriak.setdefault(versenyzo.kategoria, []).append(versenyzo)

    eredmenyek = []

    for kategoria in sorted(kategoriak, key=str.casefold):
        kategoriabeliek = kategoriak[kategoria][:]
        random.shuffle(kategoriabeliek)
        eronyero = kategoriabeliek.pop() if len(kategoriabeliek) % 2 else None
        parok = [
            (kategoriabeliek[index], kategoriabeliek[index + 1])
            for index in range(0, len(kategoriabeliek), 2)
        ]

        eredmenyek.append(
            {
                "kategoria": kategoria,
                "letszam": len(kategoriak[kategoria]),
                "parok": parok,
                "eronyero": eronyero,
            }
        )

    return eredmenyek


def ss_eredmeny_csv_mentese(fajl_utvonal, eredmenyek):
    with open(fajl_utvonal, "w", encoding="utf-8-sig", newline="") as fajl:
        iro = csv.writer(fajl)
        iro.writerow(
            [
                "Tournament",
                "MatchNumber",
                "Competitor1",
                "Club1",
                "Competitor2",
                "Club2",
                "Status",
            ]
        )

        for kategoriai_eredmeny in eredmenyek:
            kategoria = kategoriai_eredmeny["kategoria"]

            for sorszam, par in enumerate(kategoriai_eredmeny["parok"], start=1):
                versenyzo1, versenyzo2 = par
                iro.writerow(
                    [
                        kategoria,
                        sorszam,
                        versenyzo1.nev,
                        versenyzo1.klub,
                        versenyzo2.nev,
                        versenyzo2.klub,
                        "Kezdeti párosítás",
                    ]
                )

            eronyero = kategoriai_eredmeny["eronyero"]
            if eronyero is not None:
                iro.writerow(
                    [kategoria, "", eronyero.nev, eronyero.klub, "", "", "Pár nélkül / erőnyerő"]
                )
