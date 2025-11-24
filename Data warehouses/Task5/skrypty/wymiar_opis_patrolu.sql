USE baza
GO

IF OBJECT_ID('vETL_OpisPatrolu', 'V') IS NOT NULL DROP VIEW vETL_OpisPatrolu;
GO

CREATE VIEW vETL_OpisPatrolu
AS
SELECT DISTINCT
    SUBSTRING(Radiowoz, 1, CHARINDEX(' ', Radiowoz) - 1) AS Marka_radiowozu,
	SUBSTRING(Radiowoz, CHARINDEX(' ', Radiowoz) + 1, LEN(Radiowoz)) AS Model_radiowozu,
	Nr_rejestracyjny AS Nr_rejestracyjny,
	Nr_odznaki_kierowcy AS Nr_odznaki_kierowcy,
    Nr_odznaki_partnera AS Nr_odznaki_partnera
FROM dane_do_hurtowni.dbo.Patrole
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