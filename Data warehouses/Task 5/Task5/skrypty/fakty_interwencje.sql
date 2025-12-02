USE baza
GO

IF OBJECT_ID('vETL_InterwencjeFakty', 'V') IS NOT NULL DROP VIEW vETL_InterwencjeFakty;
GO

CREATE VIEW vETL_InterwencjeFakty
AS
WITH
Zdarzenia_Patrol AS (
    -- wybieramy każde zdarzenie i próbujemy przypisać patrol, który podjął interwencję
    SELECT
		-- ze zrodla pobieramy wszystko o zdarzeniu
        ST_Zdarzenia_Patrole.FK_Zdarzenia,
        ST_Zdarzenia_Patrole.Nr_patrolu,
        ST_Zdarzenia.Data_godzina_zdarzenia, 
		ST_Zdarzenia.Dzielnica, 
		ST_Zdarzenia.Kategoria, 
		ST_Zdarzenia.Rodzaj, 
		ST_Zdarzenia_Drogowe.Warunki_pogodowe, 
		ST_Zdarzenia_Drogowe.Liczba_rannych, 
		ST_Zdarzenia_Drogowe.Liczba_ofiar_smiertelnych,
		
		-- ze zrodla pobieramy wszystko o patrolu
        ST_Patrole.Nr_rejestracyjny,
		ST_Patrole.Nr_odznaki_kierowcy,
		ST_Patrole.Nr_odznaki_partnera,
        ST_Patrole.Data_godzina_rozpoczecia,
		ST_Patrole.Data_godzina_zakonczenia,
		ST_Patrole.Dzielnica_patrolu
		
    FROM dane_do_hurtowni.dbo.Zdarzenia ST_Zdarzenia
	-- dane o zdarzeniach drogowych (jesli sa)
    LEFT JOIN dane_do_hurtowni.dbo.Zdarzenia_drogowe ST_Zdarzenia_Drogowe ON ST_Zdarzenia.ID_zdarzenia = ST_Zdarzenia_Drogowe.FK_Zdarzenia
	-- jeden rekord w tym fakcie reprezentuje jedną interwencję, w ramach której mogło być kilka kar
	-- używamy row_number żeby pogrupować np. 3 kary wystawione w ramach tej interwencji
	-- i wziąć pierwszą z brzegu po to, żeby dowiedzieć się jaki patrol tam pojechał
	INNER JOIN (
        SELECT FK_Zdarzenia, Nr_patrolu, ROW_NUMBER() OVER (PARTITION BY FK_Zdarzenia ORDER BY Nr_patrolu) as Rn 
        FROM dane_do_hurtowni.dbo.Kary WHERE FK_Zdarzenia IS NOT NULL
    ) ST_Zdarzenia_Patrole ON ST_Zdarzenia.ID_zdarzenia = ST_Zdarzenia_Patrole.FK_Zdarzenia AND ST_Zdarzenia_Patrole.Rn = 1
	-- dane o patrolu
	INNER JOIN dane_do_hurtowni.dbo.Patrole ST_Patrole
        ON ST_Zdarzenia_Patrole.Nr_patrolu = ST_Patrole.Nr_patrolu
)
SELECT
    -- znajdujemy id (opisu) zdarzenia ze Zdarzenia.dim na podstawie kategorii, rodzaju, i waurnków pogodowych
	(
        SELECT ID_Zdarzenia FROM dbo.Zdarzenia dim_Zdarzenia
        WHERE dim_Zdarzenia.Kategoria = ST_Zdarzenia_Patrole.Kategoria
          AND dim_Zdarzenia.Rodzaj = ST_Zdarzenia_Patrole.Rodzaj
          AND dim_Zdarzenia.Warunki_pogodowe = CAST(LEFT(LTRIM(RTRIM(ISNULL(ST_Zdarzenia_Patrole.Warunki_pogodowe, 'Brak danych'))), 50) AS VARCHAR(50))
    ) AS ID_Zdarzenia,
    
	-- znajdujemy id patrolu z Patrole_Fakty na na podstawie nr rejestracyjnego
	-- radiowozu, odznak policjantów, dat i czasu oraz miejsca
	(
        SELECT fakt_Patrole.ID_Patrolu
        FROM dbo.Patrole_Fakty fakt_Patrole
        INNER JOIN dbo.Opis_patrolu opis_pat ON fakt_Patrole.ID_Opisu_patrolu = opis_pat.ID_Opisu_patrolu
        INNER JOIN dbo.Data data_roz ON fakt_Patrole.ID_Daty_rozpoczecia = data_roz.ID_Daty
        INNER JOIN dbo.Data data_zak ON fakt_Patrole.ID_Daty_zakonczenia = data_zak.ID_Daty
        INNER JOIN dbo.Czas czas_roz ON fakt_Patrole.ID_Czasu_rozpoczecia = czas_roz.ID_Czasu
        INNER JOIN dbo.Czas czas_zak ON fakt_Patrole.ID_Czasu_zakonczenia = czas_zak.ID_Czasu
        INNER JOIN dbo.Miejsce miej ON fakt_Patrole.ID_Miejsca = miej.ID_Miejsca
        WHERE opis_pat.Nr_rejestracyjny = ST_Zdarzenia_Patrole.Nr_rejestracyjny
            AND opis_pat.Nr_odznaki_kierowcy = ST_Zdarzenia_Patrole.Nr_odznaki_kierowcy
            AND opis_pat.Nr_odznaki_partnera = ST_Zdarzenia_Patrole.Nr_odznaki_partnera
            AND data_roz.Data = CAST(ST_Zdarzenia_Patrole.Data_godzina_rozpoczecia AS DATE)
            AND data_zak.Data = CAST(ST_Zdarzenia_Patrole.Data_godzina_zakonczenia AS DATE)
            AND DATEPART(HOUR, czas_roz.Godzina) = DATEPART(HOUR, ST_Zdarzenia_Patrole.Data_godzina_rozpoczecia)
            AND DATEPART(HOUR, czas_zak.Godzina) = DATEPART(HOUR, ST_Zdarzenia_Patrole.Data_godzina_zakonczenia)
            AND miej.Dzielnica = ST_Zdarzenia_Patrole.Dzielnica_patrolu
    ) AS ID_Patrolu,
	
	-- znajdujemy ID daty, czasu i miejsca które są datą zdarzenia ze źródła
    (SELECT ID_Daty FROM dbo.Data WHERE Data = CAST(ST_Zdarzenia_Patrole.Data_godzina_zdarzenia AS DATE)) AS ID_Daty,
	(SELECT ID_Czasu FROM dbo.Czas WHERE DATEPART(HOUR, Godzina) = DATEPART(HOUR, ST_Zdarzenia_Patrole.Data_godzina_zdarzenia)) AS ID_Czasu,
	(SELECT ID_Miejsca FROM dbo.Miejsce WHERE Dzielnica = ST_Zdarzenia_Patrole.Dzielnica) AS ID_Miejsca,
	
	-- miary pobrane ze źrodła
	ISNULL(ST_Zdarzenia_Patrole.Liczba_rannych, 0) AS Liczba_rannych,
    ISNULL(ST_Zdarzenia_Patrole.Liczba_ofiar_smiertelnych, 0) AS Liczba_ofiar,
	
	-- miary wyliczane (potem)
    0 AS Liczba_sprawcow,
    0 AS Liczba_kar,
    0 AS Suma_kwot_kar,
    0 AS Suma_punktow_karnych
	
FROM Zdarzenia_Patrol ST_Zdarzenia_Patrole
GO

INSERT INTO dbo.Interwencje_Fakty (
    ID_Zdarzenia,
    ID_Patrolu,
    ID_Daty,
    ID_Czasu,
    ID_Miejsca,
    Liczba_rannych,
    Liczba_ofiar,
    Liczba_sprawcow,
    Liczba_kar,
    Suma_kwot_kar,
    Suma_punktow_karnych
)
SELECT
    ID_Zdarzenia,
    ID_Patrolu,
    ID_Daty,
    ID_Czasu,
    ID_Miejsca,
    Liczba_rannych,
    Liczba_ofiar,
    Liczba_sprawcow,
    Liczba_kar,
    Suma_kwot_kar,
    Suma_punktow_karnych
FROM vETL_InterwencjeFakty v;
GO

DROP VIEW vETL_InterwencjeFakty;
GO