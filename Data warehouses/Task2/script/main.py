import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import math

random.seed(42)

# ========== CONFIG - BEZ ZMIAN WYNIKAJACYCH Z ZADANIA ==========
SNAP1_DIR = Path('./snapshot1')
SNAP2_DIR = Path('./snapshot2')
for d in [SNAP1_DIR, SNAP2_DIR]:
    d.mkdir(exist_ok=True)

TARGET_KARY_SNAP1 = 500_000
TARGET_KARY_SNAP2 = 500_000

OFFENDERS_PER_EVENT_CHOICES = [1, 2, 3]
OFFENDERS_PER_EVENT_PROBS = [0.80, 0.15, 0.05]

PATROLS_PER_DAY_MIN = 5
PATROLS_PER_DAY_MAX = 10
EVENTS_PER_PATROL_MIN = 0
EVENTS_PER_PATROL_MAX = 20

PATROL_DURATION_H_MIN = 7
PATROL_DURATION_H_MAX = 13

OFFICERS_POOL_SIZE_INIT = 50
OFFICER_REMOVE_COUNT = 10
OFFICER_ADD_COUNT = 20

PATROL_TWO_PERSON_PERCENT = 0.90

SQL_CHUNK_SIZE = 10_000

START_DATE = datetime(2025, 1, 1, 6, 0, 0)

DISTRICTS = ['Wrzeszcz', 'Oliwa', 'Glowne Miasto', 'Chelm', 'Morena', 'Przymorze', 'Stogi']
VEHICLES_INIT = ['Skoda Octavia', 'Kia Ceed', 'Opel Astra']
VEHICLES_ADDITIONAL_FOR_SNAP2 = ['Toyota Prius', 'Hyundai i30', 'Ford Focus']

SURNAME_BASE_MALE = ['Kowalski', 'Nowak', 'Zajac', 'Wisniewski', 'Kaczmarek', 'Lewandowski', 'Wojcik', 'Kubiak']
MALE_FIRST_NAMES = ['Adam', 'Piotr', 'Marek', 'Tomasz', 'Jan']
FEMALE_FIRST_NAMES = ['Katarzyna', 'Anna', 'Magdalena', 'Ewa', 'Agnieszka']

FEMALE_SURNAME_UPDATE_FRACTION = 0.05
SNAP2_EXISTING_NOTOWANI_SHARE = 0.60

# ========== ROZSZERZONY SŁOWNIK WIĄŻĄCY ZDARZENIA Z PRAWEM, KARAMI I POWODAMI ==========
LEGAL_MAPPING = {
    # --- ZDARZENIA DROGOWE (KW, KK, PoRD) ---
    'Przekroczenie predkosci': {
        'Kategoria': 'Drogowe',
        'Podstawy_Prawne': {
            'Art. 92a KW (do 30 km/h)': (['Mandat', 'Pouczenie'], 0.7),
            'Art. 92a KW (ponad 30 km/h)': (['Mandat', 'Wniosek_do_sadu'], 0.3),
        },
        'Powody': ['Niecierpliwość', 'Spieszenie się do pracy', 'Wyprzedzanie na trzeciego', 'Zła ocena sytuacji'],
    },
    'Kolizja': {
        'Kategoria': 'Drogowe',
        'Podstawy_Prawne': {
            'Art. 86 KW (spowodowanie zagrożenia)': (['Mandat', 'Wniosek_do_sadu'], 0.8),
            'Art. 177 KK (wypadek)': (['Wniosek_do_sadu'], 0.2),
        },
        'Powody': ['Brak ostrożności', 'Niezachowanie bezpiecznej odległości', 'Wymuszenie pierwszeństwa',
                   'Rozmowa przez telefon'],
    },
    'Jazda pod wplywem': {
        'Kategoria': 'Drogowe',
        'Podstawy_Prawne': {
            'Art. 87 KW (po użyciu alkoholu)': (['Mandat', 'Wniosek_do_sadu'], 0.6),
            'Art. 178a KK (w stanie nietrzeźwości)': (['Wniosek_do_sadu'], 0.4),
        },
        'Powody': ['Spożycie alkoholu', 'Zmęczenie', 'Brak odpowiedzialności'],
    },
    'Nieustapienie pierwszenstwa': {
        'Kategoria': 'Drogowe',
        'Podstawy_Prawne': {
            'Art. 86 par. 1 KW': (['Mandat', 'Pouczenie'], 1.0),
        },
        'Powody': ['Złe odczytanie znaków', 'Pośpiech', 'Brak koncentracji'],
    },
    'Nieprawidlowe parkowanie': {
        'Kategoria': 'Drogowe',
        'Podstawy_Prawne': {
            'Art. 97 KW (naruszenie przepisów PoRD)': (['Mandat'], 1.0),
        },
        'Powody': ['Brak wolnych miejsc', 'Pośpiech', 'Wygoda', 'Ignorowanie zakazu'],
    },
    'Ucieczka z miejsca zdarzenia': {
        'Kategoria': 'Drogowe',
        'Podstawy_Prawne': {
            'Art. 93 KW (nieudzielenie pomocy)': (['Wniosek_do_sadu'], 1.0),
        },
        'Powody': ['Strach przed odpowiedzialnością', 'Wpływ alkoholu/narkotyków'],
    },

    # --- WYKROCZENIA (KW) ---
    'Zaklocanie ciszy nocnej': {
        'Kategoria': 'Wykroczenie',
        'Podstawy_Prawne': {
            'Art. 51 KW (zakłócanie porządku)': (['Mandat', 'Pouczenie', 'Wniosek_do_sadu'], 1.0),
        },
        'Powody': ['Impreza towarzyska', 'Awaria alarmu', 'Kłótnia sąsiedzka'],
    },
    'Spozywanie alkoholu w miejscu publicznym': {
        'Kategoria': 'Wykroczenie',
        'Podstawy_Prawne': {
            'Art. 43(1) Ustawy o wychowaniu w trzeźwości': (['Mandat'], 1.0),
        },
        'Powody': ['Brak świadomości przepisów', 'Brak lokalu', 'Spotkanie ze znajomymi'],
    },
    'Zasmiecanie': {
        'Kategoria': 'Wykroczenie',
        'Podstawy_Prawne': {
            'Art. 145 KW (zaśmiecanie)': (['Mandat', 'Pouczenie'], 1.0),
        },
        'Powody': ['Lenistwo', 'Brak kosza', 'Beztroska'],
    },
    'Wandalizm (niska szkoda)': {
        'Kategoria': 'Wykroczenie',
        'Podstawy_Prawne': {
            'Art. 124 KW (niszczenie mienia)': (['Mandat', 'Wniosek_do_sadu'], 1.0),
        },
        'Powody': ['Chuligaństwo', 'Działanie pod wpływem emocji', 'Zemsta'],
    },
    'Uzywanie wulgaryzmow': {
        'Kategoria': 'Wykroczenie',
        'Podstawy_Prawne': {
            'Art. 141 KW (nieobyczajny wybryk)': (['Mandat', 'Pouczenie'], 1.0),
        },
        'Powody': ['Kłótnia', 'Agresja', 'Reakcja na zaczepkę'],
    },

    # --- PRZESTĘPSTWA (KK) ---
    'Kradziez': {
        'Kategoria': 'Przestepstwo',
        'Podstawy_Prawne': {
            'Art. 278 KK (kradzież)': (['Wniosek_do_sadu'], 1.0),
        },
        'Powody': ['Potrzeba finansowa', 'Kradzież na zlecenie', 'Okazja'],
    },
    'Pobicie': {
        'Kategoria': 'Przestepstwo',
        'Podstawy_Prawne': {
            'Art. 158 KK (udział w bójce/pobiciu)': (['Wniosek_do_sadu'], 1.0),
        },
        'Powody': ['Spór', 'Zazdrość', 'Agresja wywołana alkoholem'],
    },
    'Wlamanie': {
        'Kategoria': 'Przestepstwo',
        'Podstawy_Prawne': {
            'Art. 279 KK (kradzież z włamaniem)': (['Wniosek_do_sadu'], 1.0),
        },
        'Powody': ['Potrzeba finansowa', 'Planowane działanie', 'Chęć zdobycia kosztowności'],
    },
    'Grozba karalna': {
        'Kategoria': 'Przestepstwo',
        'Podstawy_Prawne': {
            'Art. 190 KK (groźba bezprawna)': (['Wniosek_do_sadu'], 1.0),
        },
        'Powody': ['Zemsta', 'Konflikt rodzinny/sąsiedzki', 'Działanie pod wpływem emocji'],
    },
    'Narkotyki (posiadanie)': {
        'Kategoria': 'Przestepstwo',
        'Podstawy_Prawne': {
            'Art. 62 Ustawy o przeciwdziałaniu narkomanii': (['Wniosek_do_sadu'], 1.0),
        },
        'Powody': ['Własny użytek', 'Dystrybucja', 'Próba sprzedaży'],
    }
}
ALL_EVENT_TYPES = list(LEGAL_MAPPING.keys())
EVENTS_DROGOWE_PROB = sum(1 for v in LEGAL_MAPPING.values() if v['Kategoria'] == 'Drogowe') / len(
    LEGAL_MAPPING) if LEGAL_MAPPING else 0.5


# ========== HELPERS ==========
def gen_patrol_id():
    return str(uuid.uuid4())[:10].upper()


def gen_pesel():
    return "".join(str(random.randint(0, 9)) for _ in range(11))


def gen_badge():
    return f"{random.randint(100000, 999999)}"


def gen_case_number():
    return str(uuid.uuid4())[:20].upper()


def female_form_of_surname(male):
    if male.endswith('ski'):
        return male[:-3] + 'ska'
    if male.endswith('cki'):
        return male[:-3] + 'cka'
    if male.endswith('dzki'):
        return male[:-4] + 'dzka'
    if male.endswith('owski'):
        return male[:-5] + 'owska'
    if male.endswith('i'):
        return male[:-1] + 'a'
    return male + 'a'


# SQL bulk writer - zapisuje porcjami
def sql_bulk_writer(path: Path, table_name: str, columns: list, rows_iter):
    buf = []
    count = 0
    with open(path, 'a', encoding='utf-8') as f:
        for row in rows_iter:
            escaped = []
            for v in row:
                if v is None or v == 'NULL':
                    escaped.append("NULL")
                elif isinstance(v, (int, float)):
                    escaped.append(str(v))
                elif isinstance(v, bool):
                    escaped.append('TRUE' if v else 'FALSE')
                else:
                    s = str(v).replace("'", "''")
                    escaped.append(f"'{s}'")
            buf.append(f"({', '.join(escaped)})")
            count += 1
            if count % SQL_CHUNK_SIZE == 0:
                f.write(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n")
                f.write(",\n".join(buf) + ";\n\n")
                buf = []
        if buf:
            f.write(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n")
            f.write(",\n".join(buf) + ";\n\n")


# NOWA FUNKCJA MERGUJĄCA PLIKI
def merge_sql_files(output_path: Path, sql_files_map: dict):
    """Łączy wiele plików SQL w jeden, w zadanej kolejności."""
    print(f"Łączenie plików SQL w jeden plik: {output_path.name}")
    with open(output_path, 'w', encoding='utf-8') as outfile:

        # Sekwencja ładowania z powodu kluczy obcych
        # A) Tabele podstawowe
        # B) Tabele zależące od Zdarzeń
        # C) Tabela Kary
        # D) Tabele zależące od Kary

        order = [
            'Notowani',
            'Zdarzenia',
            'Zdarzenia_drogowe',
            'Sprawcy_zdarzeń',
            'Kary',
            'Mandaty',
            'Pouczenia',
            'Wnioski_do_sadu',
        ]

        for key in order:
            if key in sql_files_map:
                filepath = sql_files_map[key]
                if not filepath.exists():
                    print(f"Ostrzeżenie: Plik {filepath} nie istnieje. Pomijanie.")
                    continue

                outfile.write(f"\n-- ######################################################################\n")
                outfile.write(f"-- INSERT INTO {key}\n")
                outfile.write(f"-- Źródło: {filepath.name}\n")
                outfile.write(f"-- ######################################################################\n\n")

                with open(filepath, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())

                outfile.write("\n")
            else:
                print(f"Ostrzeżenie: Nie znaleziono pliku dla klucza '{key}' w mapowaniu.")


# ========== GENERACJA ZDARZENIA Z LOGIKĄ PRAWNĄ ==========
def generate_event_with_legal_logic():
    """Losuje rodzaj zdarzenia, podstawę prawną, typ kary i powód zgodnie z LEGAL_MAPPING."""

    rodzaj = random.choice(ALL_EVENT_TYPES)
    mapping = LEGAL_MAPPING[rodzaj]
    kategoria = mapping['Kategoria']

    # 1. Losowanie Podstawy Prawnej z wagami
    podstawy_prawne_choices = list(mapping['Podstawy_Prawne'].keys())
    wagi = [v[1] for v in mapping['Podstawy_Prawne'].values()]
    podstawa_prawna = random.choices(podstawy_prawne_choices, weights=wagi, k=1)[0]

    # 2. Losowanie Typu Kary z dostępnych dla wylosowanej podstawy
    mozliwe_kary = mapping['Podstawy_Prawne'][podstawa_prawna][0]
    typ_kary = random.choice(mozliwe_kary)

    # 3. Losowanie Powodu zdarzenia
    powod_zdarzenia = random.choice(mapping['Powody'])

    # Parametry Mandatu (jeśli kara to Mandat)
    mandat_info = {}
    if typ_kary == 'Mandat':
        if kategoria == 'Drogowe':
            if 'ponad 30 km/h' in podstawa_prawna or rodzaj == 'Kolizja':
                kwota = random.choice([1000, 2000, 3000, 5000])
                punkty = random.choice([10, 12, 15])
            elif 'Art. 87 KW' in podstawa_prawna:
                kwota = 2500
                punkty = 15
            else:
                kwota = random.choice([50, 100, 200, 500, 800])
                punkty = random.choice([0, 1, 2, 5, 8])
        else:
            kwota = random.choice([50, 100, 300, 500, 1000])
            punkty = 0

        mandat_info['Kwota'] = kwota
        mandat_info['Punkty'] = punkty
        mandat_info['Czy_przyjety'] = random.choice([True, True, False])

    # Parametry Pouczenia
    pouczenie_info = {}
    if typ_kary == 'Pouczenie':
        pouczenie_info['Forma'] = random.choice(['ustne', 'pisemne'])
        pouczenie_info['Tresc'] = f"Udzielono pouczenia za naruszenie {podstawa_prawna.split('(')[0].strip()}"

    # Parametry Wniosku do sądu
    wniosek_info = {}
    if typ_kary == 'Wniosek_do_sadu':
        if kategoria == 'Przestepstwo' or 'KK' in podstawa_prawna:
            wniosek_info['Sad'] = random.choice(['Sad Okręgowy Gdańsk', 'Prokuratura Rejonowa'])
            wniosek_info['Rodzaj_wniosku'] = random.choice(['Akt oskarżenia', 'Wniosek o środek zapobiegawczy'])
        else:
            wniosek_info['Sad'] = random.choice(['Sad Rejonowy Gdańsk-Północ', 'Sad Rejonowy Gdańsk-Południe'])
            wniosek_info['Rodzaj_wniosku'] = random.choice(['Wniosek o ukaranie', 'Wniosek o środek wychowawczy'])

    return {
        'Kategoria': kategoria,
        'Rodzaj': rodzaj,
        'Podstawa_prawna': podstawa_prawna,
        'Typ_kary': typ_kary,
        'Powod': powod_zdarzenia,
        'Mandat_info': mandat_info,
        'Pouczenie_info': pouczenie_info,
        'Wniosek_info': wniosek_info
    }


# ========== SNAPSHOT 1 GENERATION ==========
def generate_snapshot1(output_dir: Path, target_kary: int, officers_pool_size=OFFICERS_POOL_SIZE_INIT, vehicles=None):
    output_dir.mkdir(exist_ok=True)
    print(f"Generuje snapshot1 -> katalog: {output_dir} (target kary: {target_kary})")
    if vehicles is None:
        vehicles = VEHICLES_INIT.copy()

    patrols_csv = output_dir / 'patrole.csv'
    events_csv = output_dir / 'zdarzenia.csv'
    events_map_csv = output_dir / 'zdarzenia_patrol_map.csv'
    sprawcy_csv = output_dir / 'sprawcy_zdarzen.csv'
    notowani_csv = output_dir / 'notowani.csv'
    kary_csv = output_dir / 'kary.csv'
    mandaty_csv = output_dir / 'mandaty.csv'
    pouczenia_csv = output_dir / 'pouczenia.csv'
    wnioski_csv = output_dir / 'wnioski.csv'

    sql_dir = output_dir / 'sql'
    sql_dir.mkdir(exist_ok=True)

    sql_files = {
        'Notowani': sql_dir / 'notowani_insert.sql',
        'Zdarzenia': sql_dir / 'zdarzenia_insert.sql',
        'Zdarzenia_drogowe': sql_dir / 'zdarzenia_drogowe_insert.sql',
        'Sprawcy_zdarzeń': sql_dir / 'sprawcy_zdarzen_insert.sql',
        'Kary': sql_dir / 'kary_insert.sql',
        'Mandaty': sql_dir / 'mandaty_insert.sql',
        'Pouczenia': sql_dir / 'pouczenia_insert.sql',
        'Wnioski_do_sadu': sql_dir / 'wnioski_do_sadu_insert.sql',
    }
    for p in list(sql_files.values()):
        if p.exists():
            p.unlink()

    # --- 1) przygotuj pule notowanych ---
    avg_per = 1 * 0.8 + 2 * 0.15 + 3 * 0.05
    est_notowani_needed = math.ceil(target_kary / avg_per)
    notowani_list = []
    remaining_kary = target_kary
    with open(notowani_csv, 'w', newline='', encoding='utf-8') as nf:
        w = csv.writer(nf)
        w.writerow(['Pesel', 'Imie', 'Nazwisko', 'Plec', 'Data_urodzenia', 'Przydzielone_kary'])
        while remaining_kary > 0:
            pesel = gen_pesel()
            plec = random.choice(['M', 'F'])
            if plec == 'M':
                imie = random.choice(MALE_FIRST_NAMES); nazwisko = random.choice(SURNAME_BASE_MALE)
            else:
                imie = random.choice(FEMALE_FIRST_NAMES); nazwisko = female_form_of_surname(
                    random.choice(SURNAME_BASE_MALE))
            data_ur = (datetime.now() - timedelta(days=random.randint(365 * 20, 365 * 60))).strftime('%Y-%m-%d')
            proposed = random.choices([1, 2, 3], [0.8, 0.15, 0.05], k=1)[0]
            quota = min(proposed, remaining_kary)
            w.writerow([pesel, imie, nazwisko, plec, data_ur, quota])
            notowani_list.append([pesel, imie, nazwisko, plec, data_ur, quota])
            remaining_kary -= quota

    def pesel_assigner(pool):
        idx = 0
        while idx < len(pool):
            pesel, imie, nazwisko, plec, data_ur, quota = pool[idx]
            if quota <= 0: idx += 1; continue
            pool[idx][5] -= 1
            yield pesel

    assigner = pesel_assigner(notowani_list)

    # --- 2) generuj patroli i zdarzeń oraz kar (CSV) ---
    officers = [gen_badge() for _ in range(officers_pool_size)]
    with open(output_dir / 'officers_pool.csv', 'w', newline='', encoding='utf-8') as of:
        w = csv.writer(of);
        w.writerow(['Badge'])
        for b in officers: w.writerow([b])

    event_details_map = {}

    with open(patrols_csv, 'w', newline='', encoding='utf-8') as pf, \
            open(events_csv, 'w', newline='', encoding='utf-8') as ef, \
            open(events_map_csv, 'w', newline='', encoding='utf-8') as emf, \
            open(sprawcy_csv, 'w', newline='', encoding='utf-8') as sf, \
            open(kary_csv, 'w', newline='', encoding='utf-8') as kf, \
            open(mandaty_csv, 'w', newline='', encoding='utf-8') as mf, \
            open(pouczenia_csv, 'w', newline='', encoding='utf-8') as pfou, \
            open(wnioski_csv, 'w', newline='', encoding='utf-8') as wf:

        pw = csv.writer(pf);
        ew = csv.writer(ef);
        emw = csv.writer(emf)
        sw = csv.writer(sf);
        kw = csv.writer(kf);
        mw = csv.writer(mf)
        pouw = csv.writer(pfou);
        ww = csv.writer(wf)

        pw.writerow(['nr_patrolu', 'data_godzina_rozpoczecia', 'data_godzina_zakonczenia',
                     'dzielnica_patrolu', 'radiowoz', 'nr_rejestracyjny', 'nr_odznaki_kierowcy', 'nr_odznaki_partnera'])
        ew.writerow(['id_zdarzenia', 'kategoria', 'rodzaj', 'data_godzina_zdarzenia', 'dzielnica', 'opis', 'powod'])
        emw.writerow(['id_zdarzenia', 'nr_patrolu'])
        sw.writerow(['pesel', 'id_zdarzenia'])
        kw.writerow(['nr_sprawy', 'pesel', 'id_zdarzenia', 'podstawa_prawna', 'typ_kary'])
        mw.writerow(['FK_Kary', 'Kwota', 'Czy_przyjety', 'Punkty_karne', 'Seria_numer_mandatu', 'Termin_platnosci'])
        pouw.writerow(['FK_Kary', 'Forma', 'Tresc'])
        ww.writerow(['FK_Kary', 'Sad', 'Sygnatura_akt', 'Rodzaj_wniosku'])

        current_date = START_DATE;
        issued_kary = 0;
        event_id = 1;
        patrol_count = 0
        while issued_kary < target_kary:
            available_officers = officers.copy();
            random.shuffle(available_officers)
            patrols_today = random.randint(PATROLS_PER_DAY_MIN, PATROLS_PER_DAY_MAX)
            avg_people = PATROL_TWO_PERSON_PERCENT * 2 + (1 - PATROL_TWO_PERSON_PERCENT) * 1
            max_patrols_possible = max(1, len(available_officers) // math.ceil(avg_people))
            patrols_today = min(patrols_today, max_patrols_possible)

            for _ in range(patrols_today):
                if issued_kary >= target_kary: break
                two_person = random.random() < PATROL_TWO_PERSON_PERCENT
                if two_person and len(available_officers) >= 2:
                    driver = available_officers.pop(); partner = available_officers.pop()
                elif len(available_officers) >= 1:
                    driver = available_officers.pop(); partner = None
                else:
                    break

                start = current_date + timedelta(minutes=random.randint(0, 60 * 6))
                duration_h = random.randint(PATROL_DURATION_H_MIN, PATROL_DURATION_H_MAX)
                end = start + timedelta(hours=duration_h, minutes=random.randint(0, 59))
                nr_patrolu = gen_patrol_id();
                dzielnica_patrolu = random.choice(DISTRICTS)
                radiowoz = random.choice(vehicles);
                nr_rej = f"GD{random.randint(10000, 99999)}"

                pw.writerow([nr_patrolu, start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'),
                             dzielnica_patrolu, radiowoz, nr_rej, driver, partner if partner else ''])
                patrol_count += 1

                num_events = random.randint(EVENTS_PER_PATROL_MIN, EVENTS_PER_PATROL_MAX)
                for _e in range(num_events):
                    if issued_kary >= target_kary: break

                    event_data = generate_event_with_legal_logic()
                    kategoria = event_data['Kategoria'];
                    rodzaj = event_data['Rodzaj']
                    podstawa = event_data['Podstawa_prawna'];
                    typ = event_data['Typ_kary']
                    powod = event_data['Powod']

                    patrol_minutes = max(1, int((end - start).total_seconds() // 60))
                    event_time = start + timedelta(minutes=random.randint(0, patrol_minutes))
                    dzielnica_zdarzenia = dzielnica_patrolu if random.random() < 0.8 else random.choice(
                        [d for d in DISTRICTS if d != dzielnica_patrolu])

                    num_offenders = random.choices(OFFENDERS_PER_EVENT_CHOICES, OFFENDERS_PER_EVENT_PROBS, k=1)[0]

                    ew.writerow([event_id, kategoria, rodzaj, event_time.strftime('%Y-%m-%d %H:%M:%S'),
                                 dzielnica_zdarzenia, f"Zdarzenie: {rodzaj} (Podstawa: {podstawa})", powod])
                    emw.writerow([event_id, nr_patrolu])

                    event_details_map[event_id] = {'kategoria': kategoria, 'powod': powod}

                    for _o in range(num_offenders):
                        if issued_kary >= target_kary: break
                        try:
                            pesel = next(assigner)
                        except StopIteration:
                            pesel = gen_pesel();
                            plec = random.choice(['M', 'F'])
                            if plec == 'M':
                                imie = random.choice(MALE_FIRST_NAMES); nazw = random.choice(SURNAME_BASE_MALE)
                            else:
                                imie = random.choice(FEMALE_FIRST_NAMES); nazw = female_form_of_surname(
                                    random.choice(SURNAME_BASE_MALE))
                            data_ur = (datetime.now() - timedelta(days=random.randint(365 * 20, 365 * 60))).strftime(
                                '%Y-%m-%d')
                            with open(notowani_csv, 'a', newline='', encoding='utf-8') as nf2:
                                w2 = csv.writer(nf2);
                                w2.writerow([pesel, imie, nazw, plec, data_ur, 1])
                            notowani_list.append([pesel, imie, nazw, plec, data_ur, 0])

                        sw.writerow([pesel, event_id]);
                        nr_sprawy = gen_case_number()
                        kw.writerow([nr_sprawy, pesel, event_id, podstawa, typ])

                        if typ == 'Mandat':
                            info = event_data['Mandat_info'];
                            termin = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
                            mw.writerow([nr_sprawy, info['Kwota'], info['Czy_przyjety'], info['Punkty'],
                                         str(uuid.uuid4())[:20].upper(), termin])
                        elif typ == 'Pouczenie':
                            info = event_data['Pouczenie_info']
                            pouw.writerow([nr_sprawy, info['Forma'], info['Tresc']])
                        elif typ == 'Wniosek_do_sadu':
                            info = event_data['Wniosek_info']
                            ww.writerow(
                                [nr_sprawy, info['Sad'], str(uuid.uuid4())[:10].upper(), info['Rodzaj_wniosku']])

                        issued_kary += 1

                    event_id += 1

            current_date += timedelta(days=1)

    # --- Tworzymy bulk SQLy na podstawie CSV (strumieniowo) ---
    def rows_notowani():
        with open(notowani_csv, 'r', newline='', encoding='utf-8') as f:
            r = csv.DictReader(f);
            for row in r: yield row['Pesel'], row['Imie'], row['Nazwisko'], row['Data_urodzenia']

    sql_bulk_writer(sql_files['Notowani'], 'Notowani', ['Pesel', 'Imie', 'Nazwisko', 'Data_urodzenia'], rows_notowani())

    def rows_zdarzenia():
        with open(events_csv, 'r', newline='', encoding='utf-8') as f:
            r = csv.DictReader(f);
            for row in r: yield int(row['id_zdarzenia']), row['kategoria'], row['rodzaj'], row[
                'data_godzina_zdarzenia'], row['dzielnica'], row['opis']

    sql_bulk_writer(sql_files['Zdarzenia'], 'Zdarzenia',
                    ['ID_zdarzenia', 'Kategoria', 'Rodzaj', 'Data_godzina_zdarzenia', 'Dzielnica', 'Opis'],
                    rows_zdarzenia())

    def rows_zdarzenia_drogowe_snap1():
        for id_z, details in event_details_map.items():
            if details['kategoria'] == 'Drogowe':
                warunki = random.choice(['Slonecznie', 'Deszcz', 'Mgla'])
                yield id_z, random.randint(0, 3), 0, warunki, details['powod']

    sql_bulk_writer(sql_files['Zdarzenia_drogowe'], 'Zdarzenia_drogowe',
                    ['FK_Zdarzenia', 'Liczba_rannych', 'Liczba_ofiar_smiertelnych', 'Warunki_pogodowe',
                     'Przyczyna_zdarzenia'], rows_zdarzenia_drogowe_snap1())

    sql_bulk_writer(sql_files['Sprawcy_zdarzeń'], 'Sprawcy_zdarzeń', ['FK_Notowani', 'FK_Zdarzenia'],
                    ((row['pesel'], int(row['id_zdarzenia'])) for row in
                     csv.DictReader(open(sprawcy_csv, 'r', newline='', encoding='utf-8'))))

    event_to_patrol = {}
    with open(events_map_csv, 'r', newline='', encoding='utf-8') as emf:
        for row in csv.DictReader(emf): event_to_patrol[int(row['id_zdarzenia'])] = row['nr_patrolu']

    def rows_kary():
        with open(kary_csv, 'r', newline='', encoding='utf-8') as kf:
            r = csv.DictReader(kf)
            for row in r:
                nr_sprawy = row['nr_sprawy'];
                id_z = int(row['id_zdarzenia'])
                podst = row['podstawa_prawna'];
                nr_pat = event_to_patrol.get(id_z, 'UNKNOWN')
                yield nr_sprawy, id_z, nr_pat, podst

    sql_bulk_writer(sql_files['Kary'], 'Kary', ['Nr_sprawy', 'FK_Zdarzenia', 'Nr_patrolu', 'Podstawa_prawna'],
                    rows_kary())

    def rows_mandaty():
        with open(mandaty_csv, 'r', newline='', encoding='utf-8') as mf:
            r = csv.DictReader(mf)
            for row in r: yield row['FK_Kary'], int(row['Kwota']), row['Czy_przyjety'] == 'True', int(
                row['Punkty_karne']), row['Seria_numer_mandatu'], row['Termin_platnosci']

    sql_bulk_writer(sql_files['Mandaty'], 'Mandaty',
                    ['FK_Kary', 'Kwota', 'Czy_przyjety', 'Punkty_karne', 'Seria_numer_mandatu', 'Termin_platnosci'],
                    rows_mandaty())

    def rows_pouczenia():
        with open(pouczenia_csv, 'r', newline='', encoding='utf-8') as pfou:
            r = csv.DictReader(pfou)
            for row in r: yield row['FK_Kary'], row['Forma'], row['Tresc']

    sql_bulk_writer(sql_files['Pouczenia'], 'Pouczenia', ['FK_Kary', 'Forma', 'Tresc'], rows_pouczenia())

    def rows_wnioski():
        with open(wnioski_csv, 'r', newline='', encoding='utf-8') as wf:
            r = csv.DictReader(wf)
            for row in r: yield row['FK_Kary'], row['Sad'], row['Sygnatura_akt'], row['Rodzaj_wniosku']

    sql_bulk_writer(sql_files['Wnioski_do_sadu'], 'Wnioski_do_sadu',
                    ['FK_Kary', 'Sad', 'Sygnatura_akt', 'Rodzaj_wniosku'], rows_wnioski())

    print("Snapshot1: gotowe pliki SQL w ", sql_dir.resolve())
    return {
        'dir': output_dir,
        'officers': officers,
        'sql_files': sql_files,
        'notowani_list': notowani_list,
        'wnioski_csv': wnioski_csv
    }


# ========== SNAPSHOT 2 GENERATION ==========
def generate_snapshot2(output_dir: Path, base_snapshot_info: dict, target_kary: int,
                       officer_remove=OFFICER_REMOVE_COUNT, officer_add=OFFICER_ADD_COUNT,
                       vehicles_add=None):
    output_dir.mkdir(exist_ok=True)
    print(f"Generuje snapshot2 -> katalog: {output_dir} (target kary: {target_kary})")
    if vehicles_add is None: vehicles_add = VEHICLES_ADDITIONAL_FOR_SNAP2.copy()

    base_dir = base_snapshot_info['dir']
    base_officers = base_snapshot_info['officers']
    base_notowani_csv = base_dir / 'notowani.csv'
    base_wnioski_csv = base_snapshot_info['wnioski_csv']

    # --- Aktualizacje (SQL dla mergowania) ---
    notowani_update_script = output_dir / 'notowani_updates.sql'
    convert_script = output_dir / 'convert_wnioski_to_mandaty.sql'

    # ... (Generacja danych notowanych i skryptów aktualizacyjnych) ...
    officers = base_officers.copy();
    random.shuffle(officers);
    removed = []
    for _ in range(min(officer_remove, len(officers))): removed.append(officers.pop())
    new_officers = [gen_badge() for _ in range(officer_add)];
    officers.extend(new_officers)
    vehicles = VEHICLES_INIT.copy();
    vehicles.extend(vehicles_add)

    existing_notowani = []
    with open(base_notowani_csv, 'r', newline='', encoding='utf-8') as nf:
        r = csv.DictReader(nf);
        for row in r: existing_notowani.append(
            {'Pesel': row['Pesel'], 'Imie': row['Imie'], 'Nazwisko': row['Nazwisko'], 'Plec': row.get('Plec', 'M'),
             'Data_urodzenia': row.get('Data_urodzenia', '1970-01-01')})

    female_pesels = [n['Pesel'] for n in existing_notowani if n['Plec'] == 'F']
    num_to_update = max(1, int(len(female_pesels) * FEMALE_SURNAME_UPDATE_FRACTION))
    pesels_to_update = set(random.sample(female_pesels, num_to_update)) if female_pesels else set()
    with open(notowani_update_script, 'w', encoding='utf-8') as fupd:
        fupd.write("-- Aktualizacja nazwisk kobiet (5% z S#1)\n")
        for pesel in pesels_to_update:
            new_male = random.choice(SURNAME_BASE_MALE);
            new_female = female_form_of_surname(new_male)
            escaped_name = new_female.replace("'", "''");
            fupd.write(f"UPDATE Notowani SET Nazwisko = '{escaped_name}' WHERE Pesel = '{pesel}';\n")

    wnioski_rows = []
    with open(base_wnioski_csv, 'r', newline='', encoding='utf-8') as wf:
        r = csv.DictReader(wf);
        for row in r: wnioski_rows.append(row)
    num_to_convert = max(1, int(len(wnioski_rows) * 0.05));
    to_convert = random.sample(wnioski_rows, num_to_convert) if wnioski_rows else []
    with open(convert_script, 'w', encoding='utf-8') as convf:
        fk_list = [row['FK_Kary'] for row in to_convert]
        convf.write('-- Konwersja 5% wniosków do sądu z Snapshot #1 na mandaty\n')
        for fk in fk_list: convf.write(f"DELETE FROM Wnioski_do_sadu WHERE FK_Kary = '{fk}';\n")
        convf.write('\n-- Wstaw nowe rekordy Mandaty\n')
        for fk in fk_list:
            kwota = random.choice([500, 1000, 2000]);
            czy_przy = random.choice([True, True, False]);
            punkty = random.choice([5, 8, 10])
            seria = str(uuid.uuid4())[:20].upper();
            termin = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
            convf.write(
                f"INSERT INTO Mandaty (FK_Kary, Kwota, Czy_przyjety, Punkty_karne, Seria_numer_mandatu, Termin_platnosci) VALUES ('{fk}', {kwota}, {'TRUE' if czy_przy else 'FALSE'}, {punkty}, '{seria}', '{termin}');\n")

    existing_share = SNAP2_EXISTING_NOTOWANI_SHARE;
    existing_kary_target = int(target_kary * existing_share)
    new_kary_target = target_kary - existing_kary_target
    notowani_out_csv = output_dir / 'notowani.csv'
    with open(notowani_out_csv, 'w', newline='', encoding='utf-8') as nf:
        w = csv.writer(nf);
        w.writerow(['Pesel', 'Imie', 'Nazwisko', 'Plec', 'Data_urodzenia', 'Przydzielone_kary'])
        for n in existing_notowani: w.writerow(
            [n['Pesel'], n['Imie'], n['Nazwisko'], n['Plec'], n['Data_urodzenia'], 0])
    existing_pool = random.sample(existing_notowani, min(len(existing_notowani), max(1, existing_kary_target // 1)))
    notowani_pool = [];
    remaining = existing_kary_target;
    idx = 0
    while remaining > 0:
        person = existing_pool[idx % len(existing_pool)];
        proposed = random.choices([1, 2, 3], [0.8, 0.15, 0.05], k=1)[0]
        quota = min(proposed, remaining);
        notowani_pool.append(
            [person['Pesel'], person['Imie'], person['Nazwisko'], person['Plec'], person['Data_urodzenia'], quota])
        remaining -= quota;
        idx += 1
    remaining_new = new_kary_target;
    new_notowani_created = []
    with open(notowani_out_csv, 'a', newline='', encoding='utf-8') as nf:
        w = csv.writer(nf)
        while remaining_new > 0:
            pesel = gen_pesel();
            plec = random.choice(['M', 'F'])
            if plec == 'M':
                imie = random.choice(MALE_FIRST_NAMES); nazw = random.choice(SURNAME_BASE_MALE)
            else:
                imie = random.choice(FEMALE_FIRST_NAMES); nazw = female_form_of_surname(
                    random.choice(SURNAME_BASE_MALE))
            data_ur = (datetime.now() - timedelta(days=random.randint(365 * 20, 365 * 60))).strftime('%Y-%m-%d')
            proposed = random.choices([1, 2, 3], [0.8, 0.15, 0.05], k=1)[0];
            quota = min(proposed, remaining_new)
            w.writerow([pesel, imie, nazw, plec, data_ur, quota]);
            notowani_pool.append([pesel, imie, nazw, plec, data_ur, quota])
            new_notowani_created.append(pesel);
            remaining_new -= quota

    def pesel_assigner(pool):
        idx = 0
        while idx < len(pool):
            pesel, imie, nazwisko, plec, data_ur, quota = pool[idx]
            if quota <= 0: idx += 1; continue
            pool[idx][5] -= 1;
            yield pesel

    assigner = pesel_assigner(notowani_pool)

    # --- 5) Generacja patroli/zdarzeń/kary dla snapshot2 ---
    patrols_csv = output_dir / 'patrole.csv'
    events_csv = output_dir / 'zdarzenia.csv'
    events_map_csv = output_dir / 'zdarzenia_patrol_map.csv'
    sprawcy_csv = output_dir / 'sprawcy_zdarzen.csv'
    kary_csv = output_dir / 'kary.csv'
    mandaty_csv = output_dir / 'mandaty.csv'
    pouczenia_csv = output_dir / 'pouczenia.csv'
    wnioski_csv = output_dir / 'wnioski.csv'

    event_details_map = {}

    with open(patrols_csv, 'w', newline='', encoding='utf-8') as pf, \
            open(events_csv, 'w', newline='', encoding='utf-8') as ef, \
            open(events_map_csv, 'w', newline='', encoding='utf-8') as emf, \
            open(sprawcy_csv, 'w', newline='', encoding='utf-8') as sf, \
            open(kary_csv, 'w', newline='', encoding='utf-8') as kf, \
            open(mandaty_csv, 'w', newline='', encoding='utf-8') as mf, \
            open(pouczenia_csv, 'w', newline='', encoding='utf-8') as pfou, \
            open(wnioski_csv, 'w', newline='', encoding='utf-8') as wf:

        pw = csv.writer(pf);
        ew = csv.writer(ef);
        emw = csv.writer(emf)
        sw = csv.writer(sf);
        kw = csv.writer(kf);
        mw = csv.writer(mf)
        pouw = csv.writer(pfou);
        ww = csv.writer(wf)

        pw.writerow(['nr_patrolu', 'data_godzina_rozpoczecia', 'data_godzina_zakonczenia',
                     'dzielnica_patrolu', 'radiowoz', 'nr_rejestracyjny', 'nr_odznaki_kierowcy', 'nr_odznaki_partnera'])
        ew.writerow(['id_zdarzenia', 'kategoria', 'rodzaj', 'data_godzina_zdarzenia', 'dzielnica', 'opis', 'powod'])
        emw.writerow(['id_zdarzenia', 'nr_patrolu'])
        sw.writerow(['pesel', 'id_zdarzenia'])
        kw.writerow(['nr_sprawy', 'pesel', 'id_zdarzenia', 'podstawa_prawna', 'typ_kary'])
        mw.writerow(['FK_Kary', 'Kwota', 'Czy_przyjety', 'Punkty_karne', 'Seria_numer_mandatu', 'Termin_platnosci'])
        pouw.writerow(['FK_Kary', 'Forma', 'Tresc'])
        ww.writerow(['FK_Kary', 'Sad', 'Sygnatura_akt', 'Rodzaj_wniosku'])

        current_date = START_DATE + timedelta(days=365);
        issued_kary = 0;
        event_id = 1;
        patrol_count = 0

        while issued_kary < target_kary:
            available_officers = officers.copy();
            random.shuffle(available_officers)
            patrols_today = random.randint(PATROLS_PER_DAY_MIN, PATROLS_PER_DAY_MAX)
            avg_people = PATROL_TWO_PERSON_PERCENT * 2 + (1 - PATROL_TWO_PERSON_PERCENT) * 1
            max_patrols_possible = max(1, len(available_officers) // math.ceil(avg_people))
            patrols_today = min(patrols_today, max_patrols_possible)

            for _ in range(patrols_today):
                if issued_kary >= target_kary: break
                two_person = random.random() < PATROL_TWO_PERSON_PERCENT
                if two_person and len(available_officers) >= 2:
                    driver = available_officers.pop(); partner = available_officers.pop()
                elif len(available_officers) >= 1:
                    driver = available_officers.pop(); partner = None
                else:
                    break

                start = current_date + timedelta(minutes=random.randint(0, 60 * 6))
                duration_h = random.randint(PATROL_DURATION_H_MIN, PATROL_DURATION_H_MAX)
                end = start + timedelta(hours=duration_h, minutes=random.randint(0, 59))
                nr_patrolu = gen_patrol_id();
                dzielnica_patrolu = random.choice(DISTRICTS)
                radiowoz = random.choice(vehicles);
                nr_rej = f"GD{random.randint(10000, 99999)}"

                pw.writerow([nr_patrolu, start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'),
                             dzielnica_patrolu, radiowoz, nr_rej, driver, partner if partner else ''])
                patrol_count += 1

                num_events = random.randint(EVENTS_PER_PATROL_MIN, EVENTS_PER_PATROL_MAX)
                for _e in range(num_events):
                    if issued_kary >= target_kary: break

                    event_data = generate_event_with_legal_logic()
                    kategoria = event_data['Kategoria'];
                    rodzaj = event_data['Rodzaj']
                    podstawa = event_data['Podstawa_prawna'];
                    typ = event_data['Typ_kary']
                    powod = event_data['Powod']

                    patrol_minutes = max(1, int((end - start).total_seconds() // 60))
                    event_time = start + timedelta(minutes=random.randint(0, patrol_minutes))
                    dzielnica_zdarzenia = dzielnica_patrolu if random.random() < 0.8 else random.choice(
                        [d for d in DISTRICTS if d != dzielnica_patrolu])

                    num_offenders = random.choices(OFFENDERS_PER_EVENT_CHOICES, OFFENDERS_PER_EVENT_PROBS, k=1)[0]

                    ew.writerow([event_id, kategoria, rodzaj, event_time.strftime('%Y-%m-%d %H:%M:%S'),
                                 dzielnica_zdarzenia, f"Zdarzenie: {rodzaj} (Podstawa: {podstawa})", powod])
                    emw.writerow([event_id, nr_patrolu])

                    event_details_map[event_id] = {'kategoria': kategoria, 'powod': powod}

                    for _o in range(num_offenders):
                        if issued_kary >= target_kary: break
                        try:
                            pesel = next(assigner)
                        except StopIteration:
                            pesel = gen_pesel();
                            plec = random.choice(['M', 'F'])
                            if plec == 'M':
                                imie = random.choice(MALE_FIRST_NAMES); nazw = random.choice(SURNAME_BASE_MALE)
                            else:
                                imie = random.choice(FEMALE_FIRST_NAMES); nazw = female_form_of_surname(
                                    random.choice(SURNAME_BASE_MALE))
                            data_ur = (datetime.now() - timedelta(days=random.randint(365 * 20, 365 * 60))).strftime(
                                '%Y-%m-%d')
                            with open(notowani_out_csv, 'a', newline='', encoding='utf-8') as nf:
                                w2 = csv.writer(nf);
                                w2.writerow([pesel, imie, nazw, plec, data_ur, 1])
                            notowani_pool.append([pesel, imie, nazw, plec, data_ur, 0])

                        sw.writerow([pesel, event_id]);
                        nr_sprawy = gen_case_number()
                        kw.writerow([nr_sprawy, pesel, event_id, podstawa, typ])

                        if typ == 'Mandat':
                            info = event_data['Mandat_info'];
                            termin = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
                            mw.writerow([nr_sprawy, info['Kwota'], info['Czy_przyjety'], info['Punkty'],
                                         str(uuid.uuid4())[:20].upper(), termin])
                        elif typ == 'Pouczenie':
                            info = event_data['Pouczenie_info'];
                            pouw.writerow([nr_sprawy, info['Forma'], info['Tresc']])
                        elif typ == 'Wniosek_do_sadu':
                            info = event_data['Wniosek_info'];
                            ww.writerow(
                                [nr_sprawy, info['Sad'], str(uuid.uuid4())[:10].upper(), info['Rodzaj_wniosku']])

                        issued_kary += 1

                    event_id += 1

            current_date += timedelta(days=1)

    # --- Tworzymy bulk SQLy na podstawie CSV (strumieniowo) ---
    sql_dir = output_dir / 'sql';
    sql_dir.mkdir(exist_ok=True)
    sql_files = {
        'Notowani': sql_dir / 'notowani_insert.sql',
        'Zdarzenia': sql_dir / 'zdarzenia_insert.sql',
        'Zdarzenia_drogowe': sql_dir / 'zdarzenia_drogowe_insert.sql',
        'Sprawcy_zdarzeń': sql_dir / 'sprawcy_zdarzen_insert.sql',
        'Kary': sql_dir / 'kary_insert.sql',
        'Mandaty': sql_dir / 'mandaty_insert.sql',
        'Pouczenia': sql_dir / 'pouczenia_insert.sql',
        'Wnioski_do_sadu': sql_dir / 'wnioski_do_sadu_insert.sql',
    }
    for p in sql_files.values():
        if p.exists(): p.unlink()

    def rows_notowani_to_insert():
        # Wczytujemy z pliku wynikowego, który zawiera nowych notowanych (starszych pomijamy/DB obsłuży duplikaty)
        with open(notowani_out_csv, 'r', newline='', encoding='utf-8') as f:
            r = csv.DictReader(f)
            # W tym przypadku wstawiamy wszystkich, a baza danych musi obsłużyć klucze (np. INSERT IGNORE)
            # Aby wstawić TYLKO nowych, trzeba by porównać z listą existing_notowani, ale w bulk insert jest to trudne.
            # Zostawiamy wstawienie wszystkich, bo to bezpieczniejsze w SQL Bulk.
            for row in r: yield row['Pesel'], row['Imie'], row['Nazwisko'], row['Data_urodzenia']

    sql_bulk_writer(sql_files['Notowani'], 'Notowani', ['Pesel', 'Imie', 'Nazwisko', 'Data_urodzenia'],
                    rows_notowani_to_insert())

    def rows_zdarzenia():
        with open(events_csv, 'r', newline='', encoding='utf-8') as f:
            r = csv.DictReader(f)
            for row in r: yield int(row['id_zdarzenia']), row['kategoria'], row['rodzaj'], row[
                'data_godzina_zdarzenia'], row['dzielnica'], row['opis']

    sql_bulk_writer(sql_files['Zdarzenia'], 'Zdarzenia',
                    ['ID_zdarzenia', 'Kategoria', 'Rodzaj', 'Data_godzina_zdarzenia', 'Dzielnica', 'Opis'],
                    rows_zdarzenia())

    def rows_zdarzenia_drogowe_snap2():
        for id_z, details in event_details_map.items():
            if details['kategoria'] == 'Drogowe':
                warunki = random.choice(['Slonecznie', 'Deszcz', 'Mgla'])
                yield id_z, random.randint(0, 3), 0, warunki, details['powod']

    sql_bulk_writer(sql_files['Zdarzenia_drogowe'], 'Zdarzenia_drogowe',
                    ['FK_Zdarzenia', 'Liczba_rannych', 'Liczba_ofiar_smiertelnych', 'Warunki_pogodowe',
                     'Przyczyna_zdarzenia'], rows_zdarzenia_drogowe_snap2())

    sql_bulk_writer(sql_files['Sprawcy_zdarzeń'], 'Sprawcy_zdarzeń', ['FK_Notowani', 'FK_Zdarzenia'],
                    ((row['pesel'], int(row['id_zdarzenia'])) for row in
                     csv.DictReader(open(sprawcy_csv, 'r', newline='', encoding='utf-8'))))

    event_to_patrol = {}
    with open(events_map_csv, 'r', newline='', encoding='utf-8') as emf:
        for row in csv.DictReader(emf): event_to_patrol[int(row['id_zdarzenia'])] = row['nr_patrolu']

    def rows_kary():
        with open(kary_csv, 'r', newline='', encoding='utf-8') as kf:
            r = csv.DictReader(kf)
            for row in r:
                nr_sprawy = row['nr_sprawy'];
                id_z = int(row['id_zdarzenia'])
                podst = row['podstawa_prawna'];
                nr_pat = event_to_patrol.get(id_z, 'UNKNOWN')
                yield nr_sprawy, id_z, nr_pat, podst

    sql_bulk_writer(sql_files['Kary'], 'Kary', ['Nr_sprawy', 'FK_Zdarzenia', 'Nr_patrolu', 'Podstawa_prawna'],
                    rows_kary())

    def rows_mandaty():
        with open(mandaty_csv, 'r', newline='', encoding='utf-8') as mf:
            r = csv.DictReader(mf)
            for row in r: yield row['FK_Kary'], int(row['Kwota']), row['Czy_przyjety'] == 'True', int(
                row['Punkty_karne']), row['Seria_numer_mandatu'], row['Termin_platnosci']

    sql_bulk_writer(sql_files['Mandaty'], 'Mandaty',
                    ['FK_Kary', 'Kwota', 'Czy_przyjety', 'Punkty_karne', 'Seria_numer_mandatu', 'Termin_platnosci'],
                    rows_mandaty())

    def rows_pouczenia():
        with open(pouczenia_csv, 'r', newline='', encoding='utf-8') as pfou:
            r = csv.DictReader(pfou)
            for row in r: yield row['FK_Kary'], row['Forma'], row['Tresc']

    sql_bulk_writer(sql_files['Pouczenia'], 'Pouczenia', ['FK_Kary', 'Forma', 'Tresc'], rows_pouczenia())

    def rows_wnioski():
        with open(wnioski_csv, 'r', newline='', encoding='utf-8') as wf:
            r = csv.DictReader(wf)
            for row in r: yield row['FK_Kary'], row['Sad'], row['Sygnatura_akt'], row['Rodzaj_wniosku']

    sql_bulk_writer(sql_files['Wnioski_do_sadu'], 'Wnioski_do_sadu',
                    ['FK_Kary', 'Sad', 'Sygnatura_akt', 'Rodzaj_wniosku'], rows_wnioski())

    print("Snapshot2: gotowe pliki SQL w ", sql_dir.resolve())
    return {
        'dir': output_dir,
        'sql_files': sql_files,
        'notowani_updates_script': notowani_update_script,
        'convert_script': convert_script,
    }


# ========== EXECUTE BOTH SNAPSHOTS AND MERGE SQL FILES ==========
if __name__ == '__main__':
    # 1. Generacja Snapshot 1
    snap1_info = generate_snapshot1(SNAP1_DIR, TARGET_KARY_SNAP1)

    # 2. Generacja Snapshot 2 i skryptów aktualizacyjnych
    snap2_info = generate_snapshot2(SNAP2_DIR, snap1_info, TARGET_KARY_SNAP2)

    # 3. Mergowanie SQL dla S#1
    merge_sql_files(SNAP1_DIR / 'insert_snapshot1.sql', snap1_info['sql_files'])

    # 4. Mergowanie SQL dla S#2 (wraz z aktualizacjami S#1)
    # Dodajemy skrypty aktualizacyjne do mapowania S#2
    snap2_merged_files = {
        '0_UPDATES_A': snap2_info['notowani_updates_script'],
        '0_UPDATES_B': snap2_info['convert_script'],
        **snap2_info['sql_files']
    }


    # Tworzymy niestandardową sekwencję, aby najpierw wykonać UPDATES.
    def merge_sql_files_with_updates(output_path: Path, sql_files_map: dict):
        print(f"Łączenie plików SQL w jeden plik: {output_path.name}")
        with open(output_path, 'w', encoding='utf-8') as outfile:

            # Najpierw aktualizacje
            for key in sorted(sql_files_map.keys()):
                if key.startswith('0_UPDATES'):
                    filepath = sql_files_map[key]
                    outfile.write(f"\n-- ######################################################################\n")
                    outfile.write(
                        f"-- {key.replace('0_UPDATES_A', 'AKTUALIZACJA NAZWISK KOBIET').replace('0_UPDATES_B', 'KONWERSJA WNIOSKÓW NA MANDATY')}\n")
                    outfile.write(f"-- Źródło: {filepath.name}\n")
                    outfile.write(f"-- ######################################################################\n\n")
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                    outfile.write("\n")

            # Następnie regularne INSERTy
            order = ['Notowani', 'Zdarzenia', 'Zdarzenia_drogowe', 'Sprawcy_zdarzeń', 'Kary', 'Mandaty', 'Pouczenia',
                     'Wnioski_do_sadu']
            for key in order:
                if key in sql_files_map:
                    filepath = sql_files_map[key]
                    outfile.write(f"\n-- ######################################################################\n")
                    outfile.write(f"-- INSERT INTO {key}\n")
                    outfile.write(f"-- Źródło: {filepath.name}\n")
                    outfile.write(f"-- ######################################################################\n\n")

                    with open(filepath, 'r', encoding='utf-8') as infile:
                        # Wstawiamy tylko nowe wiersze z S#2 (choć dla Notowani i tak musi być insert all)
                        outfile.write(infile.read())
                    outfile.write("\n")


    merge_sql_files_with_updates(SNAP2_DIR / 'insert_snapshot2.sql', snap2_merged_files)

    print("\n\n#####################################################")
    print("## GENERACJA ZAKOŃCZONA ##")
    print("Pliki SQL gotowe do wklejenia:")
    print(f"1. SNAPSHOT #1: {SNAP1_DIR / 'insert_snapshot1.sql'}")
    print(f"2. SNAPSHOT #2: {SNAP2_DIR / 'insert_snapshot2.sql'} (Zawiera konwersje i aktualizacje)")
    print("#####################################################")