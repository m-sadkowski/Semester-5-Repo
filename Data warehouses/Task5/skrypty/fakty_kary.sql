USE baza
GO

IF OBJECT_ID('vETL_KaryFakty', 'V') IS NOT NULL DROP VIEW vETL_KaryFakty;
GO

CREATE VIEW vETL_KaryFakty
AS
WITH 
Mandaty_Enum AS (
    SELECT 
        k.Nr_sprawy,
        k.FK_Zdarzenia,
        m.Kwota,
        m.Punkty_karne,
        ROW_NUMBER() OVER (PARTITION BY k.FK_Zdarzenia ORDER BY k.Nr_sprawy) as Rn
    FROM dane_do_hurtowni.dbo.Kary k
    JOIN dane_do_hurtowni.dbo.Mandaty m ON k.Nr_sprawy = m.FK_Kary
),

Sprawcy_Enum AS (
    SELECT 
        FK_Notowani AS Pesel,
        FK_Zdarzenia,
        ROW_NUMBER() OVER (PARTITION BY FK_Zdarzenia ORDER BY FK_Notowani) as Rn
    FROM dane_do_hurtowni.dbo.Sprawcy_zdarzen
)

SELECT
    n.ID_Notowanego,
    ok.ID_Opisu_kary,
    ifakt.ID_Interwencji,
    CAST(ISNULL(me.Kwota, 0) AS MONEY) AS Kwota_mandatu,
    CAST(ISNULL(me.Punkty_karne, 0) AS INT) AS Punkty_karne
FROM Mandaty_Enum me
INNER JOIN Sprawcy_Enum se 
    ON me.FK_Zdarzenia = se.FK_Zdarzenia 
    AND me.Rn = se.Rn
LEFT JOIN dbo.Notowani n 
    ON LTRIM(RTRIM(n.Pesel)) = LTRIM(RTRIM(se.Pesel)) 
    AND n.CzyAktualny = 1
LEFT JOIN dbo.Opis_kary ok 
    ON LTRIM(RTRIM(ok.Nr_sprawy)) = LTRIM(RTRIM(me.Nr_sprawy))
LEFT JOIN dbo.Interwencje_Fakty ifakt 
    ON ifakt.ID_Zdarzenia = me.FK_Zdarzenia;
GO

INSERT INTO dbo.Kary_Fakty (
    ID_Notowanego,
    ID_Opisu_kary,
    ID_Interwencji,
    Kwota_mandatu,
    Punkty_karne
)
SELECT
    ID_Notowanego,
    ID_Opisu_kary,
    ID_Interwencji,
    Kwota_mandatu,
    Punkty_karne
FROM vETL_KaryFakty
WHERE 
    ID_Interwencji IS NOT NULL 
    AND ID_Notowanego IS NOT NULL
    AND ID_Opisu_kary IS NOT NULL;
GO

DROP VIEW vETL_KaryFakty;
GO