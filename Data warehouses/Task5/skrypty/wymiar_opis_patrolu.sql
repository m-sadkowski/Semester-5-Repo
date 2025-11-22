USE baza
GO

IF OBJECT_ID('vETL_OpisPatrolu', 'V') IS NOT NULL DROP VIEW vETL_OpisPatrolu;
GO

CREATE VIEW vETL_OpisPatrolu
AS
SELECT DISTINCT
    CAST(LEFT(SUBSTRING(Radiowoz, 1, CHARINDEX(' ', Radiowoz) - 1), 20) AS VARCHAR(20)) AS Marka_radiowozu,
    CAST(LEFT(SUBSTRING(Radiowoz, CHARINDEX(' ', Radiowoz) + 1, LEN(Radiowoz)), 20) AS VARCHAR(20)) AS Model_radiowozu,
	CAST(LEFT(LTRIM(RTRIM(Nr_rejestracyjny)), 8) AS VARCHAR(8)) AS Nr_rejestracyjny,
	CAST(LEFT(LTRIM(RTRIM(Nr_odznaki_kierowcy)), 6) AS VARCHAR(6)) AS Nr_odznaki_kierowcy,
    CAST(LEFT(LTRIM(RTRIM(Nr_odznaki_partnera)), 6) AS VARCHAR(6)) AS Nr_odznaki_partnera

FROM dane_do_hurtowni.dbo.Patrole
WHERE Radiowoz IS NOT NULL 
  AND CHARINDEX(' ', Radiowoz) > 0
  AND Nr_rejestracyjny IS NOT NULL;
GO

MERGE INTO dbo.Opis_patrolu AS TT
    USING vETL_OpisPatrolu AS ST
        ON TT.Nr_rejestracyjny = ST.Nr_rejestracyjny
        AND TT.Nr_odznaki_kierowcy = ST.Nr_odznaki_kierowcy
        AND TT.Nr_odznaki_partnera = ST.Nr_odznaki_partnera
            WHEN NOT MATCHED THEN
                INSERT (
                    Marka_radiowozu,
                    Model_radiowozu,
                    Nr_rejestracyjny,
                    Nr_odznaki_kierowcy,
                    Nr_odznaki_partnera
                )
                VALUES (
                    ST.Marka_radiowozu,
                    ST.Model_radiowozu,
                    ST.Nr_rejestracyjny,
                    ST.Nr_odznaki_kierowcy,
                    ST.Nr_odznaki_partnera
                );
GO

DROP VIEW vETL_OpisPatrolu;
GO