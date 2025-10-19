DROP TABLE IF EXISTS Wnioski_do_sądu;
DROP TABLE IF EXISTS Pouczenia;
DROP TABLE IF EXISTS Mandaty;
DROP TABLE IF EXISTS Kary;
DROP TABLE IF EXISTS Sprawcy_zdarzeń;
DROP TABLE IF EXISTS Zdarzenia_drogowe;
DROP TABLE IF EXISTS Zdarzenia;
DROP TABLE IF EXISTS Notowani;
DROP TABLE IF EXISTS Patrole;

CREATE TABLE Notowani (
    Pesel CHAR(11) PRIMARY KEY,
    Imie VARCHAR(50),
    Nazwisko VARCHAR(50),
    Data_urodzenia DATE
);

CREATE TABLE Patrole (
    Nr_patrolu CHAR(10) PRIMARY KEY,
    Data_godzina_rozpoczecia TIMESTAMP,
    Data_godzina_zakonczenia TIMESTAMP,
    Dzielnica_patrolu VARCHAR(50),
    Radiowoz VARCHAR(50),
    Nr_rejestracyjny VARCHAR(15),
    Nr_odznaki_kierowcy VARCHAR(10),
    Nr_odznaki_partnera VARCHAR(10)
);

CREATE TABLE Zdarzenia (
    ID_zdarzenia BIGINT PRIMARY KEY,
    Kategoria VARCHAR(30),
    Rodzaj VARCHAR(100),
    Data_godzina_zdarzenia TIMESTAMP,
    Dzielnica VARCHAR(50),
    Opis TEXT
);

CREATE TABLE Zdarzenia_drogowe (
    FK_Zdarzenia BIGINT PRIMARY KEY REFERENCES Zdarzenia(ID_zdarzenia),
    Liczba_rannych INT,
    Liczba_ofiar_śmiertelnych INT,
    Warunki_pogodowe VARCHAR(30),
    Przyczyna_zdarzenia VARCHAR(100)
);

CREATE TABLE Sprawcy_zdarzeń (
    FK_Notowani CHAR(11) REFERENCES Notowani(Pesel),
    FK_Zdarzenia BIGINT REFERENCES Zdarzenia(ID_zdarzenia),
    PRIMARY KEY (FK_Notowani, FK_Zdarzenia)
);

CREATE TABLE Kary (
    Nr_sprawy CHAR(20) PRIMARY KEY,
    FK_Zdarzenia BIGINT REFERENCES Zdarzenia(ID_zdarzenia),
    Nr_patrolu CHAR(10) REFERENCES Patrole(Nr_patrolu),
    Podstawa_prawna VARCHAR(50)
);

CREATE TABLE Mandaty (
    FK_Kary CHAR(20) PRIMARY KEY REFERENCES Kary(Nr_sprawy),
    Kwota DECIMAL(10,2),
    Czy_przyjęty BOOLEAN,
    Punkty_karne INT,
    Seria_numer_mandatu CHAR(20),
    Termin_płatności TIMESTAMP
);

CREATE TABLE Pouczenia (
    FK_Kary CHAR(20) PRIMARY KEY REFERENCES Kary(Nr_sprawy),
    Forma VARCHAR(20),
    Treść TEXT
);

CREATE TABLE Wnioski_do_sądu (
    FK_Kary CHAR(20) PRIMARY KEY REFERENCES Kary(Nr_sprawy),
    Sąd VARCHAR(100),
    Sygnatura_akt CHAR(10),
    Rodzaj_wniosku VARCHAR(100)
);
