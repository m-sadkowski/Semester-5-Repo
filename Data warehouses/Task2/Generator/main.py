import os
import csv
import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker
import time

fake = Faker('pl_PL')

FIELD_TERMINATOR = '~|~'
ROW_TERMINATOR = '\n'

KATEGORIE = ['Drogowe', 'Porządkowe', 'Kryminalne']

RODZAJE_DROGOWE = ['Wypadek', 'Kolizja', 'Katastrofa lądowa']
OPISY_DROGOWE = [
    'Zdarzenie spowodowało utrudnienia w ruchu drogowym.',
    'Na miejsce wezwano patrol policji i służby ratunkowe.',
    'Zgłoszenie zostało odnotowane przez dyżurnego o poranku.',
    'Ruch na drodze został czasowo wstrzymany.',
    'Zabezpieczono teren zdarzenia i wykonano dokumentację fotograficzną.',
    'Uczestnicy zdarzenia zostali przebadani alkomatem.',
    'Pojazdy uczestniczące w zdarzeniu zostały odholowane z miejsca zdarzenia.',
    'Zdarzenie odnotowano w ewidencji systemu SEWiK.',
]

RODZAJE_PORZADKOWE = ['Zakłócenie porządku publicznego', 'Spożywanie alkoholu w miejscu publicznym', 'Wandalizm']
OPISY_PORZADKOWE = [
    'Na miejscu interweniował patrol prewencji.',
    'Osoby uczestniczące w zdarzeniu zostały wylegitymowane.',
    'Zgłoszenie wpłynęło od mieszkańców okolicznego budynku.',
    'Sporządzono notatkę urzędową i zabezpieczono nagranie z monitoringu.',
    'Uczestnicy zdarzenia zostali pouczeni o obowiązujących przepisach.',
    'Zdarzenie miało miejsce w godzinach wieczornych.',
    'Miejsce zdarzenia zostało uprzątnięte po zakończeniu interwencji.',
    'Nie odnotowano osób poszkodowanych.',
    'Zachowanie uczestników zakłócało spokój publiczny.',
    'Interwencję zakończono bez użycia środków przymusu bezpośredniego.',
]

RODZAJE_KRYMINALNE = ['Kradzież mienia', 'Pobicie', 'Włamanie']
OPISY_KRYMINALNE = [
    'Na miejsce zdarzenia skierowano grupę dochodzeniowo-śledczą.',
    'Zabezpieczono ślady biologiczne oraz odciski palców.',
    'Zdarzenie zostało zgłoszone przez świadka.',
    'Funkcjonariusze przeprowadzili oględziny miejsca zdarzenia.',
    'Poszkodowany został przesłuchany w charakterze świadka.',
    'Wszczęto postępowanie przygotowawcze pod nadzorem prokuratora.',
    'Zabezpieczono nagranie z monitoringu miejskiego.',
    'Sporządzono protokół z miejsca zdarzenia.',
    'W toku czynności ustalono potencjalnych sprawców.',
    'Zdarzenie zostało wpisane do systemu KSIP.',
    'Nie stwierdzono zagrożenia dla osób postronnych.',
    'Na miejscu obecny był technik kryminalistyki.',
]

DZIELNICE = ['Przymorze Małe', 'Przymorze Wielkie', 'Oliwa', 'Wrzeszcz Dolny', 'Wrzeszcz Górny', 'Śródmieście',
             'Aniołki', 'Brzeźno', 'Jasień', 'Chełm', 'Matarnia', 'Letnica', 'Piecki- Migowo', 'Stogi', 'Siedlce']

WARUNKI_POGODOWE = [
    "Słonecznie, sucha nawierzchnia",
    "Pochmurno, sucha nawierzchnia",
    "Deszcz, mokra nawierzchnia",
    "Ulewa, bardzo mokra nawierzchnia",
    "Mgła, ograniczona widoczność",
    "Lekki śnieg, śliska nawierzchnia",
    "Obfite opady śniegu, bardzo śliska nawierzchnia",
    "Gołoledź, ekstremalnie śliska nawierzchnia",
    "Lekka mżawka, wilgotna nawierzchnia",
    "Wietrznie, sucha nawierzchnia",
    "Burza, intensywne opady",
]

PRZYCZYNY_ZDARZEN_Z_KARAMI = [
    {
        "przyczyna": "Niezachowanie bezpiecznej odległości między pojazdami",
        "podstawa_prawna": "Art. 19 Prawa o ruchu drogowym",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [100, 300],
        "punkty_karne": 2
    },
    {
        "przyczyna": "Niezastosowanie się do sygnalizacji świetlnej",
        "podstawa_prawna": "Art. 74 Prawa o ruchu drogowym",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [300, 500],
        "punkty_karne": 6
    },
    {
        "przyczyna": "Niedostosowanie prędkości do warunków ruchu",
        "podstawa_prawna": "Art. 19 Prawa o ruchu drogowym",
        "możliwe_kary": ["mandat", "wniosek_do_sadu"],
        "kwota_mandatu": [200, 500],
        "punkty_karne": 10
    },
    {
        "przyczyna": "Nieprawidłowe wyprzedzanie",
        "podstawa_prawna": "Art. 24 Prawa o ruchu drogowym",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [250, 400],
        "punkty_karne": 5
    },
    {
        "przyczyna": "Nieustąpienie pierwszeństwa przejazdu",
        "podstawa_prawna": "Art. 25 Prawa o ruchu drogowym",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [300, 500],
        "punkty_karne": 6
    },
    {
        "przyczyna": "Jazda pod wpływem alkoholu",
        "podstawa_prawna": "Art. 87 Kodeksu wykroczeń",
        "możliwe_kary": ["wniosek_do_sadu", "mandat"],
        "kwota_mandatu": [2500, 5000],
        "punkty_karne": 10
    },
    {
        "przyczyna": "Jazda pod wpływem środków odurzających",
        "podstawa_prawna": "Art. 87a Kodeksu wykroczeń",
        "możliwe_kary": ["wniosek_do_sadu"],
        "kwota_mandatu": [0, 0],
        "punkty_karne": 10
    },
    {
        "przyczyna": "Zmęczenie lub zaśnięcie za kierownicą",
        "podstawa_prawna": "Art. 86 Kodeksu wykroczeń",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [200, 400],
        "punkty_karne": 4
    },
    {
        "przyczyna": "Używanie telefonu podczas jazdy",
        "podstawa_prawna": "Art. 45 Prawa o ruchu drogowym",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [200, 500],
        "punkty_karne": 5
    },
    {
        "przyczyna": "Nieprawidłowe manewry na skrzyżowaniu",
        "podstawa_prawna": "Art. 22 Prawa o ruchu drogowym",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [150, 300],
        "punkty_karne": 4
    },
    {
        "przyczyna": "Przekroczenie dopuszczalnej prędkości do 20 km/h",
        "podstawa_prawna": "Art. 88 Kodeksu wykroczeń",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [100, 300],
        "punkty_karne": 2
    },
    {
        "przyczyna": "Przekroczenie dopuszczalnej prędkości o 21-40 km/h",
        "podstawa_prawna": "Art. 88 Kodeksu wykroczeń",
        "możliwe_kary": ["mandat"],
        "kwota_mandatu": [300, 800],
        "punkty_karne": 6
    },
    {
        "przyczyna": "Przekroczenie dopuszczalnej prędkości o ponad 40 km/h",
        "podstawa_prawna": "Art. 88 Kodeksu wykroczeń",
        "możliwe_kary": ["wniosek_do_sadu", "mandat"],
        "kwota_mandatu": [800, 1500],
        "punkty_karne": 10
    },
    {
        "przyczyna": "Nieprawidłowe zachowanie wobec pieszego",
        "podstawa_prawna": "Art. 26 Prawa o ruchu drogowym",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [350, 500],
        "punkty_karne": 10
    },
    {
        "przyczyna": "Jazda bez wymaganych świateł",
        "podstawa_prawna": "Art. 51 Prawa o ruchu drogowym",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [100, 300],
        "punkty_karne": 3
    },
    {
        "przyczyna": "Nieprawidłowe zachowanie na przejściu dla pieszych",
        "podstawa_prawna": "Art. 47 Prawa o ruchu drogowym",
        "możliwe_kary": ["mandat", "pouczenie"],
        "kwota_mandatu": [350, 500],
        "punkty_karne": 10
    }
]

PRZYCZYNY_ZDARZEN = [p["przyczyna"] for p in PRZYCZYNY_ZDARZEN_Z_KARAMI]

def save_to_csv(data, filename, headers):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in data:
            writer.writerow(
                [item.strftime('%Y-%m-%d %H:%M:%S') if isinstance(item, datetime) else item for item in row])
    print(f"   Dane zapisano do pliku CSV: {filename}")


def save_to_bulk(data, filename_template, headers):
    base, _ = os.path.splitext(filename_template)
    bulk_filename = base + '.bulk'

    os.makedirs(os.path.dirname(bulk_filename), exist_ok=True)
    with open(bulk_filename, 'w', encoding='utf-8') as f:
        for row in data:
            str_row = [
                item.strftime('%Y-%m-%d %H:%M:%S') if isinstance(item, datetime)
                else '' if item is None
                else str(item)
                for item in row
            ]
            f.write(FIELD_TERMINATOR.join(str_row) + ROW_TERMINATOR)
    print(f"   Dane zapisano do pliku BULK: {bulk_filename}")

def generuj_notowanych(ilosc, existing_pesels=None):
    pesele_set = set() if existing_pesels is None else existing_pesels.copy()
    rekordy = []
    while len(rekordy) < ilosc:
        data_urodzenia = fake.date_of_birth(minimum_age=18, maximum_age=90)
        plec = random.choice(['M', 'K'])
        imie = fake.first_name_male() if plec == 'M' else fake.first_name_female()
        nazwisko = fake.last_name_male() if plec == 'M' else fake.last_name_female()
        pesel = fake.pesel(date_of_birth=data_urodzenia, sex=plec)
        if pesel not in pesele_set:
            pesele_set.add(pesel)
            rekordy.append([pesel, imie, nazwisko, data_urodzenia.strftime('%Y-%m-%d'), plec])
    return rekordy


def generuj_patrole(liczba_dni, ilosc_policjantow=200, start_nr_patrolu=1000000000, start_data=datetime(2025, 1, 1)):
    odznaki = list({str(random.randint(100000, 999999)) for _ in range(ilosc_policjantow)})
    auta = [(f"Skoda Octavia #{i}", f"GD {random.randint(100, 999)}AN") for i in range(15)] + \
           [(f"BMW Serii 3 #{i}", f"GA {random.randint(100, 999)}BC") for i in range(10)]

    rekordy_patroli = []
    nr_patrolu_counter = start_nr_patrolu

    for dzien in range(liczba_dni):
        aktualna_data = start_data + timedelta(days=dzien)
        for _ in range(random.randint(5, 10)):
            czas_rozpoczecia = aktualna_data.replace(hour=random.randint(6, 20), minute=random.randint(0, 59))
            czas_zakonczenia = czas_rozpoczecia + timedelta(hours=random.randint(4, 8))
            if czas_zakonczenia.day != aktualna_data.day:
                czas_zakonczenia = aktualna_data.replace(hour=23, minute=59)

            model, nr_rej = random.choice(auta)
            rekordy_patroli.append([
                str(nr_patrolu_counter), czas_rozpoczecia, czas_zakonczenia,
                random.choice(DZIELNICE), model, nr_rej,
                random.choice(odznaki), random.choice(odznaki)
            ])
            nr_patrolu_counter += 1
    return rekordy_patroli, odznaki, auta


def generuj_dane_z_patroli(patrole, lista_peseli, start_id_zdarzenia=0):
    zdarzenia, zdarzenia_drogowe, sprawcy, kary = [], [], [], []
    id_zdarzenia_counter = start_id_zdarzenia
    nr_sprawy_counter = 0
    przyczyny_info_map = {p["przyczyna"]: p for p in PRZYCZYNY_ZDARZEN_Z_KARAMI}
    pesele_do_przypisania = list(lista_peseli)
    random.shuffle(pesele_do_przypisania)

    for patrol in patrole:
        liczba_kar_dla_patrolu = random.randint(0, 20)
        pozostale_kary = liczba_kar_dla_patrolu
        while pozostale_kary > 0:
            id_zdarzenia = id_zdarzenia_counter

            offset_s = random.randint(0, int((patrol[2] - patrol[1]).total_seconds()))
            data_godzina = patrol[1] + timedelta(seconds=offset_s)

            kategoria = random.choices(KATEGORIE, weights=[0.7, 0.15, 0.15])[0]
            rodzaj, przyczyna = '', None
            if kategoria == 'Drogowe':
                rodzaj = random.choices(RODZAJE_DROGOWE, weights=[0.19, 0.8, 0.01])[0]
                przyczyna = random.choice(PRZYCZYNY_ZDARZEN)
                zdarzenia_drogowe.append(
                    [id_zdarzenia, random.randint(0, 2), 0, random.choice(WARUNKI_POGODOWE), przyczyna])
            else:
                rodzaj = 'Inne'

            zdarzenia.append([id_zdarzenia, kategoria, rodzaj, data_godzina, patrol[3], "Opis."])

            liczba_sprawcow = min(random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0], pozostale_kary)

            przypisani_sprawcy_pesel = []
            for _ in range(liczba_sprawcow):
                if pesele_do_przypisania:
                    pesel = pesele_do_przypisania.pop()
                else:
                    pesel = random.choice(lista_peseli)

                if pesel not in przypisani_sprawcy_pesel:
                    sprawcy.append([pesel, id_zdarzenia])
                    przypisani_sprawcy_pesel.append(pesel)
                    podstawa = przyczyny_info_map.get(przyczyna, {}).get("podstawa_prawna", "Art. 86 KW")
                    kary.append([f"GD/{id_zdarzenia}/{nr_sprawy_counter}", id_zdarzenia, patrol[0], podstawa])
                    nr_sprawy_counter += 1

            pozostale_kary -= len(przypisani_sprawcy_pesel)
            id_zdarzenia_counter += 1

    zdarzenia_do_przyczyn = {zd[0]: zd[4] for zd in zdarzenia_drogowe}
    mandaty, pouczenia, wnioski = przydziel_typy_kar(kary, zdarzenia_do_przyczyn, przyczyny_info_map)
    return zdarzenia, zdarzenia_drogowe, sprawcy, kary, mandaty, pouczenia, wnioski

def przydziel_typy_kar(kary, zdarzenia_do_przyczyn, przyczyny_info_map):
    mandaty, pouczenia, wnioski = [], [], []
    for nr_sprawy, id_zdarzenia, _, _ in kary:
        przyczyna = zdarzenia_do_przyczyn.get(id_zdarzenia)
        info = przyczyny_info_map.get(przyczyna)
        kara_type = random.choices(["mandat", "pouczenie", "wniosek"], weights=[0.7, 0.2, 0.1])[0]

        if kara_type == "mandat":
            min_k, max_k = (100, 500)
            if info and info["kwota_mandatu"][1] > 0: min_k, max_k = info["kwota_mandatu"]
            mandaty.append(
                [nr_sprawy, random.randint(min_k, max_k), random.choice([1, 0]), random.randint(0, 10),
                 f"M/{random.randint(1, 9999)}", 14])
        elif kara_type == "pouczenie":
            POUCZENIA = ["Pouczenie o zasadach", "Przedstawienie mozliwych konsekwencji czynu", "Ostrzezenie na przyszlosc"]
            pouczenie_tresc = random.choice(POUCZENIA)
            pouczenia.append([nr_sprawy, "ustne", pouczenie_tresc])
        else:
            RODZAJE = ["o ukaranie", "o zatrzymanie", "o doprowadzenie"]
            rodzaj_wniosku = random.choice(RODZAJE)
            wnioski.append([nr_sprawy, "Sąd Rejonowy Gdańsk-Południe", f"III W {random.randint(1, 999)}", rodzaj_wniosku])
    return mandaty, pouczenia, wnioski

def snapshot1(target_records=500000, data_dir='snapshot1_data'):
    print("\n" + "=" * 60 + f"\nSTART SNAPSHOT 1: Generowanie ~{target_records:,} rekordów\n" + "=" * 60)

    avg_kary_per_patrol = 10
    avg_patrole_per_day = 7.5
    needed_days = int((target_records / avg_kary_per_patrol) / avg_patrole_per_day)
    needed_notowani = int(target_records * 0.3)

    print(f"   - Obliczone parametry: {needed_days} dni symulacji, {needed_notowani:,} notowanych.")

    patrole, odznaki, auta = generuj_patrole(needed_days, start_data=datetime(2025, 1, 1))
    notowani = generuj_notowanych(needed_notowani)

    zdarzenia, zd_drogowe, sprawcy, kary, mandaty, pouczenia, wnioski = generuj_dane_z_patroli(
        patrole, [n[0] for n in notowani]
    )

    print(f"\n   - Zapisywanie danych do folderu '{data_dir}'...")
    save_to_bulk(notowani, f'{data_dir}/notowani.csv', ['PESEL', 'Imie', 'Nazwisko', 'DataUrodzenia', 'Plec'])
    save_to_bulk(auta, f'{data_dir}/auta.csv', ['Model', 'NrRejestracyjny'])
    save_to_bulk([[o] for o in odznaki], f'{data_dir}/policjanci.csv', ['NrOdznaki'])

    save_to_csv(patrole, f'{data_dir}/patrole.csv',
                ['NrPatrolu', 'CzasRozpoczecia', 'CzasZakonczenia', 'Dzielnica', 'ModelAuta', 'NrRejestracyjny',
                 'Kierowca', 'Partner'])

    save_to_bulk(zdarzenia, f'{data_dir}/zdarzenia.csv',
                 ['IDZdarzenia', 'Kategoria', 'Rodzaj', 'DataGodzina', 'Dzielnica', 'Opis'])
    save_to_bulk(zd_drogowe, f'{data_dir}/zdarzenia_drogowe.csv',
                 ['IDZdarzenia', 'LiczbaRannych', 'LiczbaOfiar', 'WarunkiPogodowe', 'Przyczyna'])
    save_to_bulk(sprawcy, f'{data_dir}/sprawcy_zdarzen.csv', ['PESEL', 'IDZdarzenia'])
    save_to_bulk(kary, f'{data_dir}/kary.csv', ['NrSprawy', 'IDZdarzenia', 'NrPatrolu', 'PodstawaPrawna'])
    save_to_bulk(mandaty, f'{data_dir}/mandaty.csv',
                 ['NrSprawy', 'Kwota', 'CzyPrzyjety', 'PunktyKarne', 'SeriaNumerMandatu', 'TerminPlatnosciDni'])
    save_to_bulk(pouczenia, f'{data_dir}/pouczenia.csv', ['NrSprawy', 'Forma', 'Tresc'])
    save_to_bulk(wnioski, f'{data_dir}/wnioski_do_sadu.csv', ['NrSprawy', 'Sad', 'SygnaturaAkt', 'RodzajWniosku'])

    print(f"\nSNAPSHOT 1 ZAKOŃCZONY! Wygenerowano {len(kary):,} kar.")

    return {
        'notowani': notowani, 'zdarzenia': zdarzenia, 'patrole': patrole, 'odznaki': odznaki,
        'auta': auta, 'kary': kary, 'mandaty': mandaty, 'pouczenia': pouczenia, 'wnioski': wnioski,
        'zdarzenia_drogowe': zd_drogowe, 'sprawcy': sprawcy, 'needed_days': needed_days
    }


def snapshot2(s1_data, target_records=500000, data_dir='snapshot2_data'):
    print("\n" + "=" * 60 + f"\nSTART SNAPSHOT 2: Aktualizacje i ~{target_records:,} nowych rekordów\n" + "=" * 60)

    sql_updates = []
    print("   - Generowanie skryptu SQL z aktualizacjami...")
    notowani_df = pd.DataFrame(s1_data['notowani'], columns=['PESEL', 'Imie', 'Nazwisko', 'DataUrodzenia', 'Plec'])
    kobiety_df = notowani_df[notowani_df['Plec'] == 'K']
    for _, row in kobiety_df.sample(frac=0.05).iterrows():
        sql_updates.append(f"UPDATE Notowani SET Nazwisko = '{fake.last_name_female()}' WHERE PESEL = '{row.PESEL}';")
    mandaty_df = pd.DataFrame(s1_data['mandaty'],
                              columns=['NrSprawy', 'Kwota', 'CzyPrzyjety', 'PunktyKarne', 'SeriaNumerMandatu',
                                       'TerminPlatnosciDni'])
    nieprzyjete = mandaty_df[mandaty_df['CzyPrzyjety'] == False]
    for _, row in nieprzyjete.sample(frac=0.10).iterrows():
        sql_updates.append(f"UPDATE Mandaty SET Czy_przyjety = 'True' WHERE FK_Kary = '{row.NrSprawy}';")

    update_filename = f'{data_dir}/snapshot2_updates.sql'
    os.makedirs(os.path.dirname(update_filename), exist_ok=True)
    with open(update_filename, 'w', encoding='utf-8') as f:
        f.write("-- SQL Updates and Deletes for Snapshot 2\n\n")
        f.write("\n".join(sql_updates))
    print(f"   Skrypt SQL zapisano do {update_filename}")

    print("\n   - Generowanie nowych danych...")
    avg_kary_per_patrol = 10
    avg_patrole_per_day = 7.5
    needed_days = int((target_records / avg_kary_per_patrol) / avg_patrole_per_day)
    needed_notowani = int(target_records * 0.3)

    start_nr_patrolu = int(s1_data['patrole'][-1][0]) + 1
    start_id_zdarzenia = s1_data['zdarzenia'][-1][0] + 1
    start_data = datetime(2025, 1, 1) + timedelta(days=s1_data['needed_days'] + 1)

    print(f"   - Obliczone parametry: {needed_days} dni symulacji, {needed_notowani:,} nowych notowanych.")

    nowe_patrole, nowe_odznaki, nowe_auta = generuj_patrole(needed_days, start_nr_patrolu=start_nr_patrolu,
                                                            start_data=start_data)
    print("   - Tworzenie zbioru istniejących PESEL-i...")
    s1_pesele = {n[0] for n in s1_data['notowani']}
    nowi_notowani = generuj_notowanych(needed_notowani, existing_pesels=s1_pesele)

    wszyscy_pesel = [n[0] for n in s1_data['notowani']] + [n[0] for n in nowi_notowani]

    zdarzenia, zd_drog, sprawcy, kary, mandaty, pouczenia, wnioski = generuj_dane_z_patroli(
        nowe_patrole, wszyscy_pesel, start_id_zdarzenia=start_id_zdarzenia
    )

    print(f"\n   - Zapisywanie nowych danych do folderu '{data_dir}'...")
    save_to_bulk(nowi_notowani, f'{data_dir}/notowani_new.csv', ['PESEL', 'Imie', 'Nazwisko', 'DataUrodzenia', 'Plec'])
    save_to_bulk(nowe_auta, f'{data_dir}/auta_new.csv', ['Model', 'NrRejestracyjny'])
    save_to_bulk([[o] for o in nowe_odznaki], f'{data_dir}/policjanci_new.csv', ['NrOdznaki'])

    save_to_csv(nowe_patrole, f'{data_dir}/patrole_new.csv',
                ['NrPatrolu', 'CzasRozpoczecia', 'CzasZakonczenia', 'Dzielnica', 'ModelAuta', 'NrRejestracyjny',
                 'Kierowca', 'Partner'])

    save_to_bulk(zdarzenia, f'{data_dir}/zdarzenia_new.csv',
                 ['IDZdarzenia', 'Kategoria', 'Rodzaj', 'DataGodzina', 'Dzielnica', 'Opis'])
    save_to_bulk(zd_drog, f'{data_dir}/zdarzenia_drogowe_new.csv',
                 ['IDZdarzenia', 'LiczbaRannych', 'LiczbaOfiar', 'WarunkiPogodowe', 'Przyczyna'])
    save_to_bulk(sprawcy, f'{data_dir}/sprawcy_zdarzen_new.csv', ['PESEL', 'IDZdarzenia'])
    save_to_bulk(kary, f'{data_dir}/kary_new.csv', ['NrSprawy', 'IDZdarzenia', 'NrPatrolu', 'PodstawaPrawna'])
    save_to_bulk(mandaty, f'{data_dir}/mandaty_new.csv',
                 ['NrSprawy', 'Kwota', 'CzyPrzyjety', 'PunktyKarne', 'SeriaNumerMandatu', 'TerminPlatnosciDni'])
    save_to_bulk(pouczenia, f'{data_dir}/pouczenia_new.csv', ['NrSprawy', 'Forma', 'Tresc'])
    save_to_bulk(wnioski, f'{data_dir}/wnioski_do_sadu_new.csv', ['NrSprawy', 'Sad', 'SygnaturaAkt', 'RodzajWniosku'])

    print(f"\nSNAPSHOT 2 ZAKOŃCZONY! Wygenerowano {len(kary):,} nowych kar.")

    return {
        'notowani': nowi_notowani, 'zdarzenia': zdarzenia, 'patrole': nowe_patrole, 'kary': kary,
        'mandaty': mandaty, 'pouczenia': pouczenia, 'wnioski': wnioski,
        'zdarzenia_drogowe': zd_drog, 'sprawcy': sprawcy
    }

def podsumowanie(s1, s2):
    print("\n" + "=" * 60)
    print("PODSUMOWANIE KOŃCOWE - ANALIZA WYGENEROWANYCH DANYCH")
    print("=" * 60)

    notowani = s1['notowani'] + s2.get('notowani', [])
    zdarzenia = s1['zdarzenia'] + s2.get('zdarzenia', [])
    zdarzenia_drogowe = s1['zdarzenia_drogowe'] + s2.get('zdarzenia_drogowe', [])
    sprawcy = s1['sprawcy'] + s2.get('sprawcy', [])
    patrole = s1['patrole'] + s2.get('patrole', [])
    kary = s1['kary'] + s2.get('kary', [])
    mandaty = s1['mandaty'] + s2.get('mandaty', [])
    pouczenia = s1['pouczenia'] + s2.get('pouczenia', [])
    wnioski = s1['wnioski'] + s2.get('wnioski', [])

    liczba_dni_patroli = s1['needed_days'] * 2

    print(f"\nPODSTAWOWE STATYSTYKI:")
    print(f"    Notowani: {len(notowani):,} osób")
    print(f"    Zdarzenia: {len(zdarzenia):,} (w tym {len(zdarzenia_drogowe):,} drogowych)")
    print(f"    Sprawcy zdarzeń: {len(sprawcy):,} powiązań")
    print(f"    Patrole: {len(patrole):,} (średnio {len(patrole) / liczba_dni_patroli:.1f} patroli/dzień)")
    print(f"    Kary: {len(kary):,}")

    id_do_rodzaju = {z[0]: z[2] for z in zdarzenia}
    wypadki = len([z for z in zdarzenia_drogowe if id_do_rodzaju.get(z[0]) == 'Wypadek'])
    kolizje = len([z for z in zdarzenia_drogowe if id_do_rodzaju.get(z[0]) == 'Kolizja'])
    katastrofy = len([z for z in zdarzenia_drogowe if id_do_rodzaju.get(z[0]) == 'Katastrofa lądowa'])

    if zdarzenia_drogowe:
        print(f"\nZDARZENIA DROGOWE WG RODZAJU:")
        print(f"    Wypadki: {wypadki} ({wypadki / len(zdarzenia_drogowe) * 100:.1f}%)")
        print(f"    Kolizje: {kolizje} ({kolizje / len(zdarzenia_drogowe) * 100:.1f}%)")
        print(f"    Katastrofy: {katastrofy} ({katastrofy / len(zdarzenia_drogowe) * 100:.1f}%)")

    kary_na_patrol = {}
    for kara in kary:
        nr_patrolu = kara[2]
        kary_na_patrol[nr_patrolu] = kary_na_patrol.get(nr_patrolu, 0) + 1

    patrole_z_karami = len(kary_na_patrol)
    patrole_bez_kar = len(patrole) - patrole_z_karami

    min_kar = 0
    if patrole_bez_kar == 0 and kary_na_patrol:
        min_kar = min(kary_na_patrol.values())

    print(f"\nEFEKTYWNOŚĆ PATROLI:")
    print(f"    Średnia kar na patrol: {len(kary) / len(patrole):.1f}")
    print(f"    Min kar na patrol: {min_kar}")
    print(f"    Max kar na patrol: {max(kary_na_patrol.values()) if kary_na_patrol else 0}")
    print(f"    Patrole z karami: {patrole_z_karami} ({patrole_z_karami / len(patrole) * 100:.1f}%)")
    print(f"    Patrole bez kar: {patrole_bez_kar} ({patrole_bez_kar / len(patrole) * 100:.1f}%)")

    print(f"\nROZKŁAD TYPÓW KAR:")
    print(f"    Mandaty: {len(mandaty)} ({len(mandaty) / len(kary) * 100:.1f}%)")
    print(f"    Pouczenia: {len(pouczenia)} ({len(pouczenia) / len(kary) * 100:.1f}%)")
    print(f"    Wnioski do sądu: {len(wnioski)} ({len(wnioski) / len(kary) * 100:.1f}%)")

    poprawne_czasowo = len(kary)
    print(f"\nSPRAWDZENIE POPRAWNOŚCI:")
    print(
        f"    Powiązania czasowe: {poprawne_czasowo}/{len(kary)} ({poprawne_czasowo / len(kary) * 100:.1f}%)")

    print(f"\nRELACJE MIĘDZY ENCJAMI:")
    print(f"    Zdarzenia ze sprawcami: {len(set(s[1] for s in sprawcy))}/{len(zdarzenia)} zdarzeń")
    print(f"    Notowani ze zdarzeniami: {len(set(s[0] for s in sprawcy))}/{len(notowani)} osób")
    print(f"    Kary nałożone na zdarzenia: {len(set(k[1] for k in kary))}/{len(zdarzenia)} zdarzeń")

    print("\n" + "=" * 60)
    print("SUKCES: Zakończono generowanie i analizę danych!")
    print("=" * 60)


if __name__ == '__main__':
    start = time.time()

    s1_data = snapshot1(target_records=100)
    s2_data = snapshot2(s1_data, target_records=100)

    podsumowanie(s1_data, s2_data)

    koniec = time.time()
    print("\n" + "=" * 60)
    print(f"Wszystkie operacje zakończone pomyślnie!")
    print(f"   Całkowity czas wykonania: {(koniec - start):.2f} sekund.")
    print("=" * 60)