USE baza
GO

IF OBJECT_ID('vETL_Zdarzenia', 'V') IS NOT NULL DROP VIEW vETL_Zdarzenia;
GO

CREATE VIEW vETL_Zdarzenia
AS
SELECT DISTINCT
    CAST(LEFT(LTRIM(RTRIM(z.Kategoria)), 20) AS VARCHAR(20)) AS Kategoria,
	CAST(LEFT(LTRIM(RTRIM(z.Rodzaj)), 50) AS VARCHAR(50)) AS Rodzaj,
	CAST(LEFT(LTRIM(RTRIM(ISNULL(zd.Warunki_pogodowe, 'Brak danych'))), 50) AS VARCHAR(50)) AS Warunki_pogodowe
FROM dane_do_hurtowni.dbo.Zdarzenia z
LEFT JOIN dane_do_hurtowni.dbo.Zdarzenia_drogowe zd 
    ON z.ID_zdarzenia = zd.FK_Zdarzenia
WHERE z.Kategoria IS NOT NULL;
GO

MERGE INTO dbo.Zdarzenia AS TT
    USING vETL_Zdarzenia AS ST
        ON TT.Kategoria = ST.Kategoria
        AND TT.Rodzaj = ST.Rodzaj
        AND TT.Warunki_pogodowe = ST.Warunki_pogodowe
            WHEN NOT MATCHED THEN
                INSERT (
                    Kategoria,
                    Rodzaj,
                    Warunki_pogodowe
                )
                VALUES (
                    ST.Kategoria,
                    ST.Rodzaj,
                    ST.Warunki_pogodowe
                );
GO

DROP VIEW vETL_Zdarzenia;
GO