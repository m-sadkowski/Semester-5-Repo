import random
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor
from itertools import chain

NAMES_M = ["Adam", "Bartosz", "Krzysztof", "Michał", "Piotr", "Paweł", "Marcin", "Tomasz", "Łukasz", "Mateusz",
            "Grzegorz", "Andrzej", "Rafał", "Jakub", "Maciej", "Jan", "Kamil", "Szymon", "Patryk", "Artur",
            "Damian", "Wojciech", "Sebastian", "Robert", "Dawid", "Daniel", "Dominik", "Marek", "Mariusz", "Karol",
            "Filip", "Adrian", "Cezary", "Hubert", "Oskar", "Igor", "Norbert", "Konrad", "Łukasz", "Eryk",
            "Mikołaj", "Julian", "Edward", "Franciszek", "Leon", "Aleksander", "Stefan", "Antoni", "Henryk", "Wiktor"]

NAMES_F = ["Anna", "Katarzyna", "Małgorzata", "Agnieszka", "Ewa", "Barbara", "Maria", "Joanna", "Magdalena", "Monika",
            "Paulina", "Karolina", "Marta", "Beata", "Aleksandra", "Natalia", "Julia", "Zuzanna", "Weronika", "Patrycja",
            "Dominika", "Sylwia", "Emilia", "Justyna", "Wiktoria", "Klaudia", "Elżbieta", "Gabriela", "Dorota", "Iwona",
            "Helena", "Kamila", "Teresa", "Urszula", "Anita", "Jolanta", "Alicja", "Renata", "Izabela", "Liliana",
            "Adrianna", "Antonina", "Lena", "Ewelina", "Oliwia", "Maja", "Amelia", "Aneta", "Sandra", "Jagoda"]

SURNAMES_M = ["Nowak", "Kowalski", "Wiśniewski", "Wójcik", "Kowalczyk", "Kamiński", "Lewandowski", "Zieliński", "Szymański", "Woźniak",
              "Dąbrowski", "Kozłowski", "Jankowski", "Mazur", "Wojciechowski", "Kwiatkowski", "Krawczyk", "Kaczmarek", "Piotrowski", "Grabowski",
              "Zając", "Pawlak", "Michalski", "Król", "Wieczorek", "Jabłoński", "Wróbel", "Nowakowski", "Majewski", "Olszewski",
              "Stępień", "Malinowski", "Jaworski", "Adamczyk", "Dudek", "Nowicki", "Wilk", "Pawłowski", "Sikora", "Walczak",
              "Baran", "Rutkowski", "Michalak", "Szewczyk", "Ostrowski", "Tomaszewski", "Pietrzak", "Marciniak", "Wróblewski", "Zalewski"]

SURNAMES_F = [
    "Nowak", "Kowalska", "Wiśniewska", "Wójcik", "Kowalczyk", "Kamińska", "Lewandowska", "Zielińska", "Szymańska", "Woźniak",
    "Dąbrowska", "Kozłowska", "Jankowska", "Mazur", "Wojciechowska", "Kwiatkowska", "Krawczyk", "Kaczmarek", "Piotrowska", "Grabowska",
    "Zając", "Pawlak", "Michalska", "Król", "Wieczorek", "Jabłońska", "Wróbel", "Nowakowska", "Majewska", "Olszewska",
    "Stępień", "Malinowska", "Jaworska", "Adamczyk", "Dudek", "Nowicka", "Wilk", "Pawłowska", "Sikora", "Walczak",
    "Baran", "Rutkowska", "Michalak", "Szewczyk", "Ostrowska", "Tomaszewska", "Pietrzak", "Marciniak", "Wróblewska", "Zalewska"
]


class RecordedPeopleGenerator:
    def __init__(self):
        self.pesels = set()

    def generate(self, number_of_records: int, threads: int = 1):
        if threads <= 1:
            return self._generate_batch(number_of_records)

        chunk = number_of_records // threads
        remainder = number_of_records % threads
        parts = [chunk + (1 if i < remainder else 0) for i in range(threads)]

        with ThreadPoolExecutor(max_workers=threads) as executor:
            results = list(executor.map(self._generate_batch, parts))

        return list(chain.from_iterable(results))

    def _generate_batch(self, number_of_records: int):
        local_pesels = set()
        recorded_people = []

        for _ in range(number_of_records):
            gender = random.choice(['M', 'K'])
            name = random.choice(NAMES_M if gender == 'M' else NAMES_F)
            surname = random.choice(SURNAMES_M if gender == 'M' else SURNAMES_F)

            start = date(1950, 1, 1)
            end = date(2000, 12, 31)
            delta = end - start
            date_of_birth = start + timedelta(days=random.randint(0, delta.days))

            while True:
                pesel = self.generate_pesel(date_of_birth, gender)
                if pesel not in local_pesels:
                    local_pesels.add(pesel)
                    break

            recorded_people.append({
                "imie": name,
                "nazwisko": surname,
                "data_urodzenia": date_of_birth.isoformat(),
                "pesel": pesel
            })

        return recorded_people

    def generate_pesel(self, data_of_birth: date, plec: str) -> str:
        year = data_of_birth.year
        month = data_of_birth.month
        day = data_of_birth.day

        if 1800 <= year < 1900:
            month += 80
        elif 2000 <= year < 2100:
            month += 20
        elif 2100 <= year < 2200:
            month += 40
        elif 2200 <= year < 2300:
            month += 60

        year_2 = year % 100
        month_2 = month
        day_2 = day

        random_number = random.randint(0, 999)
        gender_number = random.choice([1, 3, 5, 7, 9]) if plec == 'M' else random.choice([0, 2, 4, 6, 8])

        pesel_without_control = f"{year_2:02d}{month_2:02d}{day_2:02d}{random_number:03d}{gender_number}"
        check_digit = self.calculate_check_digit(pesel_without_control)
        return pesel_without_control + str(check_digit)

    def calculate_check_digit(self, pesel: str) -> int:
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        check_sum = sum(int(pesel[i]) * weights[i] for i in range(10))
        check_digit = (10 - (check_sum % 10)) % 10
        return check_digit
