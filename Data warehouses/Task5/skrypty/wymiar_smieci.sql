USE baza
GO

MERGE INTO dbo.Smieci AS Target
USING (VALUES 
    (0),
    (1)
) AS Source (Czy_interwencje)
ON Target.Czy_interwencje = Source.Czy_interwencje

WHEN NOT MATCHED THEN
    INSERT (Czy_interwencje)
    VALUES (Source.Czy_interwencje);
GO