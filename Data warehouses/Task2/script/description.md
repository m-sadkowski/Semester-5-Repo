Generujemy **dane do bazy policyjnej** w dwóch snapshotach:

* **Snapshot 1:** ok. **500 000 kar**
* **Snapshot 2:** dopisuje **kolejne 500 000 kar** (łącznie 1 000 000)
  z **modyfikacjami danych** (nowi policjanci, nowe radiowozy, recydywa, aktualizacje nazwisk, konwersje wniosków na mandaty itd.)

---

## 🧩 STRUKTURA DANYCH I ZALEŻNOŚCI

### 1️⃣ **Patrole (CSV)**

* Generowane **dzień po dniu**
* Każdy dzień:

  * **5–10 patroli** (równomiernie losowo)
  * **90% patroli** dwuosobowych
  * **10% patroli** jednoosobowych
  * Policjant może być maksymalnie w **1 patrolu dziennie**
* Czas trwania patrolu: **7–13 godzin**
* Dane: `nr_patrolu`, `data rozpoczęcia`, `data zakończenia`, `dzielnica`, `radiowóz`, `nr odznak`
* Radiowozy losowane z listy (`Skoda Octavia`, `Kia Ceed`, `Opel Astra`)
  → w Snapshot 2 lista jest rozszerzona (nowe modele, np. `Toyota Corolla`, `Hyundai i30`)
* Dzielnica: jedna z 7 (`Wrzeszcz`, `Oliwa`, `Główne Miasto`, `Chełm`, `Morena`, `Przymorze`, `Stogi`)

📌 **Patrole są źródłem wszystkich zdarzeń i kar.**

---

### 2️⃣ **Zdarzenia**

Każdy patrol „wykrywa” zdarzenia.

* **0–20 zdarzeń na patrol** (równomierny rozkład)
* Data zdarzenia: losowa chwila w trakcie patrolu
* Dzielnica zdarzenia:

  * **80%** – ta sama co dzielnica patrolu
  * **20%** – losowa inna dzielnica
* Kategorie:

  * **80%** – `Drogowe`
  * **20%** – losowo `Wykroczenie` lub `Przestępstwo`
* Rodzaj zdarzenia:

  * `Drogowe`: `Przekroczenie prędkości`, `Kolizja`, `Jazda pod wpływem`
  * `Wykroczenie`: `Zakłócanie ciszy nocnej`, `Spożywanie alkoholu w miejscu publicznym`, `Zaśmiecanie`
  * `Przestępstwo`: `Kradzież`, `Pobicie`, `Włamanie`

📌 **Każde zdarzenie jest powiązane z jednym patrolem.**

---

### 3️⃣ **Sprawcy zdarzeń (Notowani)**

#### Snapshot 1:

* Obliczana liczba notowanych:

  * Średnia kar na notowanego = `1×0.8 + 2×0.15 + 3×0.05 = 1.25`
  * Przy **500 000 kar** ⇒ ~**400 000 notowanych**
* Rozkład liczby kar na notowanego:

  * **80%** – 1 kara
  * **15%** – 2 kary
  * **5%** – 3 kary
* PESEL syntetyczny (losowy 11-cyfrowy)
* Imię i nazwisko losowe:

  * Imiona żeńskie i męskie osobno (dla zachowania płci)
  * Nazwiska generowane w wersjach żeńskiej/męskiej (np. `Kowalski` → `Kowalska`)

#### Snapshot 2:

* Część notowanych jest **nowa** (np. +20% nowych osób)
* Część zdarzeń popełniają **istniejący notowani** (recydywa)
* U części notowanych (kobiet) zmienia się nazwisko:

  * np. **5–10% kobiet** dostaje nazwisko żeńskie po mężu (`UPDATE Notowani SET Nazwisko = ...`)
* Snapshot 2 aktualizuje także niektóre rekordy w SQL (`UPDATE`)

---

### 4️⃣ **Sprawcy_zdarzeń (relacja N:M)**

* Każde zdarzenie ma:

  * **1–3 sprawców**
  * Rozkład:

    * **80%** – 1 sprawca
    * **15%** – 2 sprawców
    * **5%** – 3 sprawców
* Każdy sprawca ma co najmniej 1 karę (czyli jedno zdarzenie).

---

### 5️⃣ **Kary**

Każda relacja `(Sprawca, Zdarzenie)` = jedna kara.

#### Snapshot 1:

* Cel: **500 000 kar**
* Rodzaje kar (rozkład):

  * **50%** – `Mandat`
  * **25%** – `Wniosek_do_sądu`
  * **25%** – `Pouczenie`
* Podstawa prawna: losowo `Art. 86 KW`, `Art. 97 KW`, `Art. 177 KK`
* Każda kara powiązana z:

  * konkretnym zdarzeniem,
  * konkretnym patrolem,
  * konkretnym sprawcą (notowanym).

#### Snapshot 2:

* Dopisuje **kolejne 500 000 kar**
* Zachowuje ten sam rozkład kar (50/25/25)
* Ale:

  * **5% istniejących „Wniosków do sądu”** zamienia się w `Mandaty` (ktoś jednak przyjął mandat)

    * generowany skrypt SQL z `UPDATE`
  * **niektóre zdarzenia** przypisane są do już znanych sprawców (recydywa)
  * **część nowych notowanych** bierze udział w nowych zdarzeniach

---

### 6️⃣ **Mandaty**

* Tworzone dla kar typu `Mandat`
* Dane:

  * `Kwota`: [50, 100, 200, 500, 1000]
  * `Czy_przyjęty`: 2/3 przypadków `TRUE`
  * `Punkty_karne`: [0, 1, 2, 5, 8]
  * `Seria_numer_mandatu`: losowe UUID
  * `Termin_płatności`: 7 dni od wystawienia

---

### 7️⃣ **Pouczenia**

* Tworzone dla kar typu `Pouczenie`
* Dane:

  * `Forma`: `ustne` lub `pisemne`
  * `Treść`: tekst opisowy, np. *„Udzielono pouczenia za Art. 97 KW”*

---

### 8️⃣ **Wnioski_do_sądu**

* Tworzone dla kar typu `Wniosek_do_sądu`
* Dane:

  * `Sąd`: `Sąd Rejonowy Gdańsk-Północ` lub `Sąd Okręgowy Gdańsk`
  * `Sygnatura_akt`: losowe UUID
  * `Rodzaj_wniosku`: `o ukaranie` lub `o zastosowanie środka wychowawczego`
* W Snapshot 2:

  * **5% wniosków** zostaje przerobionych na `Mandaty` (z `UPDATE`).

---

### 9️⃣ **Zdarzenia_drogowe**

* Podzbiór zdarzeń o kategorii `Drogowe`
* Dodatkowe dane:

  * `Liczba_rannych`: 0–3
  * `Liczba_ofiar_śmiertelnych`: 0–1
  * `Warunki_pogodowe`: `Słonecznie`, `Deszcz`, `Mgła`
  * `Przyczyna_zdarzenia`: `Brak ostrożności`, `Prędkość`, `Wjechanie w tył`

---

## 🧮 PODSUMOWANIE ZALEŻNOŚCI

| Encja                 | Powiązanie / Źródło         | Ilość / Rozkład                           | Snapshot 2 modyfikacje                              |
| --------------------- | --------------------------- | ----------------------------------------- | --------------------------------------------------- |
| **Patrole**           | generowane dzień po dniu    | 5–10 dziennie, 90% 2-os, 10% 1-os, 7–13 h | zmiana listy policjantów (-10 + 20), nowe radiowozy |
| **Zdarzenia**         | z patroli                   | 0–20 na patrol, 80% drogowe               | część z udziałem istniejących notowanych            |
| **Sprawcy_zdarzeń**   | z notowanych                | 1–3 sprawców / zdarzenie (80/15/5)        | recydywa (część starych PESEL)                      |
| **Notowani**          | baza PESEL                  | ~400 000 (dla 500k kar)                   | część nowych, aktualizacja nazwisk kobiet           |
| **Kary**              | z relacji sprawca–zdarzenie | 1 per relacja                             | +500 000 nowych; 5% wniosków → mandaty              |
| **Mandaty**           | z kar typu Mandat           | 50%                                       | część z konwersji (z wniosków)                      |
| **Pouczenia**         | z kar typu Pouczenie        | 25%                                       | bez zmian                                           |
| **Wnioski_do_sądu**   | z kar typu Wniosek          | 25%                                       | -5% (zamienione na mandaty)                         |
| **Zdarzenia_drogowe** | z `Zdarzenia`               | 80% zdarzeń                               | proporcjonalnie w nowych danych                     |

---

💡 **W skrócie zależność logiczna:**

```
Patrol ──▶ Zdarzenia ──▶ (Sprawca + Notowany) ──▶ Kary ──▶ [Mandaty / Pouczenia / Wnioski_do_sądu]
```