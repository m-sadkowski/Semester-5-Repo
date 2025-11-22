USE baza
GO

IF OBJECT_ID('vETL_Notowani', 'V') IS NOT NULL DROP VIEW vETL_Notowani;
GO

CREATE VIEW vETL_Notowani
AS
SELECT DISTINCT
    CAST(LTRIM(RTRIM(Pesel)) AS VARCHAR(11)) AS Pesel,
    CAST(LEFT(LTRIM(RTRIM(Imie)) + ' ' + LTRIM(RTRIM(Nazwisko)), 60) AS VARCHAR(60)) AS Imie_nazwisko,
    CAST(Data_urodzenia AS DATE) AS Data_urodzenia,
    CAST(LEFT(LTRIM(RTRIM(Plec)), 1) AS VARCHAR(1)) AS Plec
FROM dane_do_hurtowni.dbo.Notowani
WHERE Pesel IS NOT NULL;
GO

DECLARE @DataLadowania DATE = GETDATE();

UPDATE TT
SET 
    TT.CzyAktualny = 0,
    TT.DataWaznosciDo = @DataLadowania
FROM dbo.Notowani TT
JOIN vETL_Notowani ST ON TT.Pesel = ST.Pesel
WHERE 
    TT.CzyAktualny = 1
    AND (
        TT.Imie_nazwisko <> ST.Imie_nazwisko
        OR TT.Plec <> ST.Plec
        OR TT.Data_urodzenia <> ST.Data_urodzenia
    );

INSERT INTO dbo.Notowani (
    Pesel,
    Imie_nazwisko,
    Data_urodzenia,
    Plec,
    DataWaznosciOd,
    DataWaznosciDo,
    CzyAktualny
)
SELECT 
    ST.Pesel,
    ST.Imie_nazwisko,
    ST.Data_urodzenia,
    ST.Plec,
    @DataLadowania,
    NULL,           
    1             
FROM vETL_Notowani ST
LEFT JOIN dbo.Notowani TT 
    ON ST.Pesel = TT.Pesel 
    AND TT.CzyAktualny = 1
WHERE 
    TT.Pesel IS NULL;
GO

DROP VIEW vETL_Notowani;
GO