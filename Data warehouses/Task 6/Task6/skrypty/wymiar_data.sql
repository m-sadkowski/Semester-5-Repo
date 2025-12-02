USE baza
GO

DECLARE @DataPoczatkowa DATE = '2024-01-01';
DECLARE @DataKoncowa DATE = '2030-12-31';
DECLARE @AktualnaData DATE = @DataPoczatkowa;

WHILE @AktualnaData <= @DataKoncowa
BEGIN
    DECLARE @isSwieto BIT = 0;
    DECLARE @isDzienPrzedswiateczny BIT = 0;
    DECLARE @Rok INT = YEAR(@AktualnaData);
    DECLARE @Miesiac INT = MONTH(@AktualnaData);
    DECLARE @Dzien INT = DAY(@AktualnaData);

    SET @isSwieto = CASE
        WHEN @Miesiac = 1  AND @Dzien = 1  THEN 1
        WHEN @Miesiac = 1  AND @Dzien = 6  THEN 1
        WHEN @Miesiac = 5  AND @Dzien = 1  THEN 1
        WHEN @Miesiac = 5  AND @Dzien = 3  THEN 1
        WHEN @Miesiac = 8  AND @Dzien = 15 THEN 1
        WHEN @Miesiac = 11 AND @Dzien = 1  THEN 1
        WHEN @Miesiac = 11 AND @Dzien = 11 THEN 1
        WHEN @Miesiac = 12 AND @Dzien = 25 THEN 1
        WHEN @Miesiac = 12 AND @Dzien = 26 THEN 1
        WHEN @AktualnaData IN ('2024-03-31', '2025-04-20', '2026-04-05', '2027-03-28', '2028-04-16', '2029-04-01', '2030-04-21') THEN 1
        WHEN @AktualnaData IN ('2024-04-01', '2025-04-21', '2026-04-06', '2027-03-29', '2028-04-17', '2029-04-02', '2030-04-22') THEN 1
        WHEN @AktualnaData IN ('2024-05-30', '2025-06-19', '2026-06-04', '2027-05-27', '2028-06-15', '2029-05-31', '2030-06-20') THEN 1
        ELSE 0
    END;

    SET @isDzienPrzedswiateczny = CASE
        WHEN @Miesiac = 12 AND @Dzien = 31 THEN 1
        WHEN @Miesiac = 1  AND @Dzien = 5  THEN 1
        WHEN @Miesiac = 4  AND @Dzien = 30 THEN 1
        WHEN @Miesiac = 5  AND @Dzien = 2  THEN 1
        WHEN @Miesiac = 8  AND @Dzien = 14 THEN 1
        WHEN @Miesiac = 10 AND @Dzien = 31 THEN 1
        WHEN @Miesiac = 11 AND @Dzien = 10 THEN 1
        WHEN @Miesiac = 12 AND @Dzien = 24 THEN 1
        WHEN @AktualnaData IN ('2024-03-30', '2025-04-19', '2026-04-04', '2027-03-27', '2028-04-15', '2029-03-31', '2030-04-20') THEN 1
        WHEN @AktualnaData IN ('2024-05-29', '2025-06-18', '2026-06-03', '2027-05-26', '2028-06-14', '2029-05-30', '2030-06-19') THEN 1
        ELSE 0
    END;

    IF @isSwieto = 1
        SET @isDzienPrzedswiateczny = 0;

    INSERT INTO dbo.Data (
        Data,
        Rok,
        Miesiac,
        Dzien_tygodnia,
        Dzien_pracujacy,
        Czas_wakacyjny,
        Swieto,
        Dzien_przedswiateczny,
        Miesiac_nr
    )
    VALUES (
        @AktualnaData,
        @Rok,
        DATENAME(MONTH, @AktualnaData),
        DATENAME(WEEKDAY, @AktualnaData),
        CASE 
            WHEN DATEPART(WEEKDAY, @AktualnaData) IN (1, 7) OR @isSwieto = 1 THEN 0 
            ELSE 1 
        END,
        CASE WHEN @Miesiac IN (7, 8) THEN 1 ELSE 0 END,
        @isSwieto, 
        @isDzienPrzedswiateczny,
        @Miesiac
    );

    SET @AktualnaData = DATEADD(DAY, 1, @AktualnaData);
END;