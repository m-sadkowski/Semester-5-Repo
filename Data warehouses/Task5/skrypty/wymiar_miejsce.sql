USE baza
GO

IF OBJECT_ID('vETL_Miejsce', 'V') IS NOT NULL DROP VIEW vETL_Miejsce;
GO

CREATE VIEW vETL_Miejsce
AS
SELECT DISTINCT
    CAST(LEFT(LTRIM(RTRIM(Dzielnica)), 20) AS VARCHAR(20)) AS Dzielnica
FROM dane_do_hurtowni.dbo.Zdarzenia
WHERE Dzielnica IS NOT NULL 
  AND LTRIM(RTRIM(Dzielnica)) <> '';
GO

MERGE INTO dbo.Miejsce AS TT
    USING vETL_Miejsce AS ST
        ON TT.Dzielnica = ST.Dzielnica
            
            WHEN NOT MATCHED THEN
                INSERT (Dzielnica)
                VALUES (ST.Dzielnica);
GO

DROP VIEW vETL_Miejsce;
GO