USE baza
GO

DECLARE @Godzina INT = 0;

WHILE @Godzina < 24
BEGIN
    INSERT INTO dbo.Czas (Godzina, Pora_dnia)
    VALUES (
        CAST(CAST(@Godzina AS VARCHAR(2)) + ':00:00' AS TIME), 
        
        CASE 
            WHEN @Godzina BETWEEN 6 AND 9 THEN 'rano'
            WHEN @Godzina BETWEEN 10 AND 13 THEN 'okolo poludnia'
            WHEN @Godzina BETWEEN 14 AND 18 THEN 'po poludniu'
            WHEN @Godzina BETWEEN 19 AND 23 THEN 'wieczorem'
            ELSE 'w nocy'
        END
    );
    SET @Godzina = @Godzina + 1;
END;