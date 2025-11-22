USE baza
GO

DELETE FROM dbo.Kary_Fakty;
DELETE FROM dbo.Opis_kary;
GO

IF OBJECT_ID('vETL_OpisKary', 'V') IS NOT NULL DROP VIEW vETL_OpisKary;
GO

CREATE VIEW vETL_OpisKary
AS
WITH RawData AS (
    SELECT 
        k.Nr_sprawy,
        k.Podstawa_prawna,
		CASE 
            WHEN m.FK_Kary IS NOT NULL THEN 'Mandat'
            WHEN p.FK_Kary IS NOT NULL THEN 'Pouczenie'
            WHEN w.FK_Kary IS NOT NULL THEN 'Wniosek do sadu'
            ELSE 'Inne'
        END AS Rodzaj,
		m.Czy_przyjety,
        m.Seria_numer_mandatu,
        p.Forma,
        w.Sad,
        w.Sygnatura_akt,
        w.Rodzaj_wniosku,
		ROW_NUMBER() OVER (PARTITION BY k.Nr_sprawy ORDER BY k.Nr_sprawy) as RowNum
    FROM dane_do_hurtowni.dbo.Kary k
    LEFT JOIN dane_do_hurtowni.dbo.Mandaty m ON k.Nr_sprawy = m.FK_Kary
    LEFT JOIN dane_do_hurtowni.dbo.Pouczenia p ON k.Nr_sprawy = p.FK_Kary
    LEFT JOIN dane_do_hurtowni.dbo.Wnioski_do_sadu w ON k.Nr_sprawy = w.FK_Kary
    WHERE k.Nr_sprawy IS NOT NULL AND LTRIM(RTRIM(k.Nr_sprawy)) <> ''
)
SELECT 
    CAST(LEFT(LTRIM(RTRIM(Nr_sprawy)), 10) AS VARCHAR(10)) AS Nr_sprawy,
    CAST(LEFT(LTRIM(RTRIM(ISNULL(Podstawa_prawna, 'Brak'))), 20) AS VARCHAR(20)) AS Podstawa_prawna,
    CAST(Rodzaj AS VARCHAR(50)) AS Rodzaj,
	CAST(ISNULL(Czy_przyjety, 0) AS BIT) AS Czy_przyjeta,
    CAST(LEFT(LTRIM(RTRIM(ISNULL(Seria_numer_mandatu, 'Brak'))), 10) AS VARCHAR(10)) AS Seria_numer_mandatu,
    CAST(LEFT(LTRIM(RTRIM(ISNULL(Forma, 'Brak'))), 10) AS VARCHAR(10)) AS Forma,
    CAST(LEFT(LTRIM(RTRIM(ISNULL(Sad, 'Brak'))), 50) AS VARCHAR(50)) AS Nazwa_sadu,
    CAST(LEFT(LTRIM(RTRIM(ISNULL(Sygnatura_akt, 'Brak'))), 10) AS VARCHAR(10)) AS Sygnatura_akt,
    CAST(LEFT(LTRIM(RTRIM(ISNULL(Rodzaj_wniosku, 'Brak'))), 30) AS VARCHAR(30)) AS Rodzaj_wniosku

FROM RawData
WHERE RowNum = 1;
GO

INSERT INTO dbo.Opis_kary (
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
SELECT 
    Nr_sprawy,
    Podstawa_prawna,
    Rodzaj,
    Czy_przyjeta,
    Seria_numer_mandatu,
    Forma,
    Nazwa_sadu,
    Sygnatura_akt,
    Rodzaj_wniosku
FROM vETL_OpisKary;
GO

DROP VIEW vETL_OpisKary;
GO