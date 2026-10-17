import csv
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from ss_sorsolas import (
    ss_csv_beolvasasa,
    ss_eredmeny_csv_mentese,
    ss_sorsolas_keszitese,
)


root = tk.Tk()
root.title("Karateverseny sorsolás")
root.geometry("1000x700")
root.minsize(760, 500)

versenyzok = []
eredmenyek = []
betoltott_fajl = None
projekt_mappa = Path(__file__).resolve().parent
statusz = tk.StringVar(value="Töltsd be a jelentkezési CSV-fájlt.")

fejlec = ttk.Frame(root, padding=(12, 12, 12, 6))
fejlec.pack(fill="x")

ttk.Label(fejlec, text="Karateverseny sorsolás", font=("Segoe UI", 16, "bold")).pack(anchor="w")
ttk.Label(
    fejlec,
    text="Kumite- és kata-kategóriák kezdeti párosítása CSV alapján",
).pack(anchor="w", pady=(3, 0))

vezerles = ttk.Frame(root, padding=(12, 6))
vezerles.pack(fill="x")

kimenet_frame = ttk.Frame(root, padding=(12, 6, 12, 12))
kimenet_frame.pack(fill="both", expand=True)

kimenet = tk.Text(kimenet_frame, wrap="word", font=("Consolas", 10), state="disabled")
gorgeto = ttk.Scrollbar(kimenet_frame, orient="vertical", command=kimenet.yview)
kimenet.configure(yscrollcommand=gorgeto.set)
kimenet.pack(side="left", fill="both", expand=True)
gorgeto.pack(side="right", fill="y")

statusz_sor = ttk.Label(root, textvariable=statusz, relief="sunken", anchor="w", padding=6)
statusz_sor.pack(fill="x", side="bottom")


def ss_kimenet_frissitese(szoveg):
    kimenet.configure(state="normal")
    kimenet.delete("1.0", "end")
    kimenet.insert("1.0", szoveg)
    kimenet.configure(state="disabled")


def ss_csv_betoltese():
    global versenyzok, betoltott_fajl, eredmenyek

    fajl_utvonal = filedialog.askopenfilename(
        title="Jelentkezési CSV kiválasztása",
        initialdir=projekt_mappa,
        filetypes=[("CSV fájlok", "*.csv"), ("Minden fájl", "*.*")],
    )

    if not fajl_utvonal:
        return

    try:
        uj_versenyzok = ss_csv_beolvasasa(fajl_utvonal)
    except (OSError, UnicodeError, csv.Error, ValueError) as hiba:
        messagebox.showerror("CSV betöltési hiba", str(hiba))
        return

    versenyzok = uj_versenyzok
    betoltott_fajl = Path(fajl_utvonal)
    eredmenyek = []
    kategoriak_szama = len({versenyzo.kategoria for versenyzo in versenyzok})
    statusz.set(
        f"Betöltve: {betoltott_fajl.name} | Versenyzők: {len(versenyzok)} | Kategóriák: {kategoriak_szama}"
    )
    ss_kimenet_frissitese(
        f"Sikeres betöltés: {betoltott_fajl.name}\n"
        f"Versenyzők száma: {len(versenyzok)}\n"
        f"Kategóriák száma: {kategoriak_szama}\n\n"
        "Kattints a Sorsolás gombra az összes kategória egyidejű kisorsolásához."
    )
    sorsolas_gomb.configure(state="normal")
    mentes_gomb.configure(state="disabled")


def ss_sorsolas_inditasa():
    global eredmenyek

    if not versenyzok:
        messagebox.showwarning("Nincs adat", "Először tölts be egy CSV-fájlt.")
        return

    eredmenyek = ss_sorsolas_keszitese(versenyzok)
    sorok = [
        "KARATEVERSENY – KEZDETI SORSOLÁS",
        f"Forrásfájl: {betoltott_fajl.name if betoltott_fajl else 'ismeretlen'}",
        f"Versenyzők száma: {len(versenyzok)}",
        f"Kategóriák száma: {len(eredmenyek)}",
        "",
    ]

    osszes_par = 0
    osszes_eronyero = 0

    for kategoriai_eredmeny in eredmenyek:
        sorok.append(kategoriai_eredmeny["kategoria"])
        sorok.append("-" * min(max(len(kategoriai_eredmeny["kategoria"]), 12), 70))
        sorok.append(f"Kategória létszáma: {kategoriai_eredmeny['letszam']}")

        if not kategoriai_eredmeny["parok"]:
            sorok.append("Nincs kialakítható mérkőzéspár ebben a kategóriában.")

        for sorszam, par in enumerate(kategoriai_eredmeny["parok"], start=1):
            versenyzo1, versenyzo2 = par
            sorok.append(
                f"{sorszam}. mérkőzés: {versenyzo1.nev} ({versenyzo1.klub})"
                f"  –  {versenyzo2.nev} ({versenyzo2.klub})"
            )
            osszes_par += 1

        eronyero = kategoriai_eredmeny["eronyero"]
        if eronyero is not None:
            sorok.append(f"Pár nélkül / erőnyerő: {eronyero.nev} ({eronyero.klub})")
            osszes_eronyero += 1

        sorok.append("")

    sorok.extend(
        [
            "ÖSSZESÍTÉS",
            f"Kialakított párok száma: {osszes_par}",
            f"Pár nélkül maradó versenyzők száma: {osszes_eronyero}",
            "",
            "Ez a kezdeti sorsolás; a program nem kezeli a mérkőzések eredményeit vagy a továbbjutást.",
        ]
    )

    ss_kimenet_frissitese("\n".join(sorok))
    statusz.set(
        f"Sorsolás elkészült | Kategóriák: {len(eredmenyek)} | Párok: {osszes_par} | Erőnyerők: {osszes_eronyero}"
    )
    mentes_gomb.configure(state="normal")


def ss_eredmeny_mentese():
    if not eredmenyek:
        messagebox.showwarning("Nincs sorsolás", "Először készítsd el a sorsolást.")
        return

    fajl_utvonal = filedialog.asksaveasfilename(
        title="Sorsolás mentése",
        initialdir=projekt_mappa,
        initialfile="karate_sorsolas.csv",
        defaultextension=".csv",
        filetypes=[("CSV fájlok", "*.csv")],
    )

    if not fajl_utvonal:
        return

    try:
        ss_eredmeny_csv_mentese(fajl_utvonal, eredmenyek)
    except (OSError, UnicodeError, csv.Error, ValueError) as hiba:
        messagebox.showerror("Mentési hiba", str(hiba))
        return

    statusz.set(f"Sorsolás elmentve: {Path(fajl_utvonal).name}")
    messagebox.showinfo("Sikeres mentés", f"A sorsolás mentése sikerült:\n{fajl_utvonal}")


ttk.Button(vezerles, text="CSV betöltése", command=ss_csv_betoltese).pack(side="left", padx=(0, 8))
sorsolas_gomb = ttk.Button(
    vezerles,
    text="Összes kategória kisorsolása",
    command=ss_sorsolas_inditasa,
    state="disabled",
)
sorsolas_gomb.pack(side="left", padx=(0, 8))
mentes_gomb = ttk.Button(
    vezerles,
    text="Sorsolás mentése CSV-be",
    command=ss_eredmeny_mentese,
    state="disabled",
)
mentes_gomb.pack(side="left")

if __name__ == "__main__":
    root.mainloop()
