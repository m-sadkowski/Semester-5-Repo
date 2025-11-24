USE baza
GO

IF OBJECT_ID('vETL_Miejsce', 'V') IS NOT NULL DROP VIEW vETL_Miejsce;
GO

-- select distinct wyciaga unikalne wartosci z surowych danych
CREATE VIEW vETL_Miejsce
AS
SELECT DISTINCT
   Dzielnica
FROM dane_do_hurtowni.dbo.Zdarzenia
WHERE Dzielnica IS NOT NULL 
GO

-- merge zapobiega duplikatom - jesli istnieje to nic nie rob
MERGE INTO dbo.Miejsce AS TT
    USING vETL_Miejsce AS ST
        ON TT.Dzielnica = ST.Dzielnica
            WHEN NOT MATCHED THEN
                INSERT (Dzielnica)
                VALUES (ST.Dzielnica);
GO

DROP VIEW vETL_Miejsce;
GO