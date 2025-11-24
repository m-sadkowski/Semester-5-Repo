USE baza
GO

IF OBJECT_ID('vETL_KaryFakty', 'V') IS NOT NULL DROP VIEW vETL_KaryFakty;
GO

WITH 

Sprawcy_Ranked AS (
    SELECT 
        FK_Notowani, 
        FK_Zdarzenia, 
        ROW_NUMBER() OVER (PARTITION BY FK_Zdarzenia ORDER BY FK_Notowani) as Rn
    FROM dane_do_hurtowni.dbo.Sprawcy_zdarzen
),

Kary_Ranked AS (
    SELECT 
        Nr_sprawy, 
        FK_Zdarzenia, 
        Nr_patrolu, 
        ROW_NUMBER() OVER (PARTITION BY FK_Zdarzenia ORDER BY Nr_sprawy) as Rn
    FROM dane_do_hurtowni.dbo.Kary
),

Zdarzenia_Notowani_Kary_Raw AS (
    SELECT 
        s.FK_Notowani,
        k.Nr_sprawy,
        k.FK_Zdarzenia,
        m.Kwota,
        m.Punkty_karne,
        z.Data_godzina_zdarzenia, 
        z.Dzielnica, 
        z.Kategoria, 
        z.Rodzaj,    
        zd.Warunki_pogodowe,
        p.Nr_rejestracyjny AS Nr_rejestracyjny_patrolu_src,
        p.Nr_odznaki_kierowcy AS Nr_odznaki_kierowcy_src,
        p.Nr_odznaki_partnera AS Nr_odznaki_partnera_src,
        p.Data_godzina_rozpoczecia AS Data_rozpoczecia_patrolu_src,
        p.Data_godzina_zakonczenia AS Data_zakonczenia_patrolu_src,
        p.Dzielnica_patrolu AS Dzielnica_patrolu_src
    FROM Kary_Ranked k
    INNER JOIN Sprawcy_Ranked s 
        ON k.FK_Zdarzenia = s.FK_Zdarzenia AND k.Rn = s.Rn
    INNER JOIN dane_do_hurtowni.dbo.Zdarzenia z 
        ON k.FK_Zdarzenia = z.ID_zdarzenia 
    LEFT JOIN dane_do_hurtowni.dbo.Zdarzenia_drogowe zd 
        ON z.ID_zdarzenia = zd.FK_Zdarzenia
    LEFT JOIN dane_do_hurtowni.dbo.Mandaty m 
        ON k.Nr_sprawy = m.FK_Kary
    INNER JOIN dane_do_hurtowni.dbo.Patrole p 
        ON k.Nr_patrolu = p.Nr_patrolu 
),

Zdarzenia_Notowani_Kary_Klucze AS (
    SELECT 
		--
        znk.*, 
        
        -- a
        (SELECT ID_Zdarzenia FROM dbo.Zdarzenia dz 
         WHERE dz.Kategoria = znk.Kategoria
           AND dz.Rodzaj = znk.Rodzaj
           AND dz.Warunki_pogodowe = ISNULL(znk.Warunki_pogodowe, 'Brak danych')
        ) AS ID_Zdarzenia_H,
        
		--
        (SELECT ID_Daty FROM dbo.Data WHERE Data = CAST(znk.Data_godzina_zdarzenia AS DATE)) AS ID_Daty_H,
        (SELECT ID_Czasu FROM dbo.Czas WHERE DATEPART(HOUR, Godzina) = DATEPART(HOUR, znk.Data_godzina_zdarzenia)) AS ID_Czasu_H,
        (SELECT ID_Miejsca FROM dbo.Miejsce WHERE Dzielnica = znk.Dzielnica) AS ID_Miejsca_H,

		--
        (SELECT pf.ID_Patrolu
         FROM dbo.Patrole_Fakty pf
         INNER JOIN dbo.Opis_patrolu op ON pf.ID_Opisu_patrolu = op.ID_Opisu_patrolu
         INNER JOIN dbo.Data dr ON pf.ID_Daty_rozpoczecia = dr.ID_Daty
         INNER JOIN dbo.Data dz ON pf.ID_Daty_zakonczenia = dz.ID_Daty
         INNER JOIN dbo.Czas cr ON pf.ID_Czasu_rozpoczecia = cr.ID_Czasu
         INNER JOIN dbo.Czas cz ON pf.ID_Czasu_zakonczenia = cz.ID_Czasu
         INNER JOIN dbo.Miejsce m ON pf.ID_Miejsca = m.ID_Miejsca
         WHERE 
             op.Nr_rejestracyjny = znk.Nr_rejestracyjny_patrolu_src
             AND op.Nr_odznaki_kierowcy = znk.Nr_odznaki_kierowcy_src
             AND op.Nr_odznaki_partnera = znk.Nr_odznaki_partnera_src
             AND dr.Data = CAST(znk.Data_rozpoczecia_patrolu_src AS DATE)
             AND dz.Data = CAST(znk.Data_zakonczenia_patrolu_src AS DATE)
             AND DATEPART(HOUR, cr.Godzina) = DATEPART(HOUR, znk.Data_rozpoczecia_patrolu_src)
             AND DATEPART(HOUR, cz.Godzina) = DATEPART(HOUR, znk.Data_zakonczenia_patrolu_src)
             AND m.Dzielnica = znk.Dzielnica_patrolu_src
        ) AS ID_Patrolu_H
        
    FROM Zdarzenia_Notowani_Kary_Raw znk
)

INSERT INTO dbo.Kary_Fakty (
    ID_Notowanego,
    ID_Opisu_kary,
    ID_Interwencji,
    Kwota_mandatu,
    Punkty_karne
)
SELECT
    n.ID_Notowanego,
    ok.ID_Opisu_kary,
    ifakt.ID_Interwencji,
    CAST(ISNULL(znk.Kwota, 0) AS MONEY) AS Kwota_mandatu,
    CAST(ISNULL(znk.Punkty_karne, 0) AS INT) AS Punkty_karne
FROM Zdarzenia_Notowani_Kary_Klucze znk
-- 
INNER JOIN dbo.Notowani n 
    ON LTRIM(RTRIM(n.Pesel)) = LTRIM(RTRIM(znk.FK_Notowani)) 
    AND n.CzyAktualny = 1 
--
INNER JOIN dbo.Opis_kary ok 
    ON LTRIM(RTRIM(ok.Nr_sprawy)) = LTRIM(RTRIM(znk.Nr_sprawy))
-- 
INNER JOIN dbo.Interwencje_Fakty ifakt 
    ON ifakt.ID_Zdarzenia = znk.ID_Zdarzenia_H
    AND ifakt.ID_Daty = znk.ID_Daty_H
    AND ifakt.ID_Czasu = znk.ID_Czasu_H
    AND ifakt.ID_Miejsca = znk.ID_Miejsca_H
    AND ifakt.ID_Patrolu = znk.ID_Patrolu_H
GO