USE baza
GO

IF OBJECT_ID('vETL_OpisKary', 'V') IS NOT NULL DROP VIEW vETL_OpisKary;
GO

CREATE VIEW vETL_OpisKary
AS
SELECT DISTINCT
    k.Nr_sprawy AS Nr_sprawy,
    LEFT(k.Podstawa_prawna, 20) AS Podstawa_prawna,
    CASE 
        WHEN m.FK_Kary IS NOT NULL THEN 'Mandat'
        WHEN p.FK_Kary IS NOT NULL THEN 'Pouczenie'
        WHEN w.FK_Kary IS NOT NULL THEN 'Wniosek do sadu'
        ELSE 'Inne'
    END AS Rodzaj,    
    ISNULL(m.Czy_przyjety, 0) AS Czy_przyjeta,
    LEFT(ISNULL(m.Seria_numer_mandatu, 'Brak'), 10) AS Seria_numer_mandatu,
    ISNULL(p.Forma, 'Brak') AS Forma,
    ISNULL(w.Sad, 'Brak') AS Nazwa_sadu,
    ISNULL(w.Sygnatura_akt, 'Brak') AS Sygnatura_akt,
    ISNULL(w.Rodzaj_wniosku, 'Brak') AS Rodzaj_wniosku
FROM dane_do_hurtowni.dbo.Kary k
LEFT JOIN dane_do_hurtowni.dbo.Mandaty m ON k.Nr_sprawy = m.FK_Kary
LEFT JOIN dane_do_hurtowni.dbo.Pouczenia p ON k.Nr_sprawy = p.FK_Kary
LEFT JOIN dane_do_hurtowni.dbo.Wnioski_do_sadu w ON k.Nr_sprawy = w.FK_Kary
GO

MERGE INTO dbo.Opis_kary AS TT
    USING vETL_OpisKary AS ST
        ON TT.Nr_sprawy = ST.Nr_sprawy
            WHEN NOT MATCHED THEN
                INSERT (
                    Nr_sprawy,
                    Podstawa_prawna,
                    Rodzaj,
                    Czy_przyjeta,
                    Seria_numer_mandatu,
                    Forma,
                    Nazwa_sadu,
                    Sygnatura_akt,
                    Rodzaj_wniosku
                )
                VALUES (
                    ST.Nr_sprawy,
                    ST.Podstawa_prawna,
                    ST.Rodzaj,
                    ST.Czy_przyjeta,
                    ST.Seria_numer_mandatu,
                    ST.Forma,
                    ST.Nazwa_sadu,
                    ST.Sygnatura_akt,
                    ST.Rodzaj_wniosku
                );
GO

DROP VIEW vETL_OpisKary;
GO