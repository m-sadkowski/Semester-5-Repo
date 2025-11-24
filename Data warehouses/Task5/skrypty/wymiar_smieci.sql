USE baza
GO

MERGE INTO dbo.Smieci AS TT
USING (VALUES 
    (0),
    (1)
) AS ST (Czy_interwencje)
ON TT.Czy_interwencje = ST.Czy_interwencje

WHEN NOT MATCHED THEN
    INSERT (Czy_interwencje)
    VALUES (ST.Czy_interwencje);
GO