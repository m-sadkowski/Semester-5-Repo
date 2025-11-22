USE baza
GO

IF OBJECT_ID('vETL_InterwencjeFakty', 'V') IS NOT NULL DROP VIEW vETL_InterwencjeFakty;
GO

CREATE VIEW vETL_InterwencjeFakty
AS
SELECT
    dim_z.ID_Zdarzenia,
	(
        SELECT TOP 1 pf.ID_Patrolu
        FROM dbo.Patrole_Fakty pf
        JOIN dbo.Opis_patrolu op ON pf.ID_Opisu_patrolu = op.ID_Opisu_patrolu
        JOIN dbo.Data d ON pf.ID_Daty_rozpoczecia = d.ID_Daty
        WHERE 
            op.Nr_rejestracyjny = LEFT(LTRIM(RTRIM(p.Nr_rejestracyjny)), 8)
            AND d.Data = CAST(p.Data_godzina_rozpoczecia AS DATE)
    ) AS ID_Patrolu,
    (SELECT TOP 1 ID_Daty FROM dbo.Data WHERE Data = CAST(z.Data_godzina_zdarzenia AS DATE)) AS ID_Daty,
    (SELECT TOP 1 ID_Czasu FROM dbo.Czas WHERE DATEPART(HOUR, Godzina) = DATEPART(HOUR, z.Data_godzina_zdarzenia)) AS ID_Czasu,
    (SELECT TOP 1 ID_Miejsca FROM dbo.Miejsce WHERE LTRIM(RTRIM(Dzielnica)) = LEFT(LTRIM(RTRIM(z.Dzielnica)), 20)) AS ID_Miejsca,
    ISNULL(CAST(zd.Liczba_rannych AS INT), 0) AS Liczba_rannych,
    ISNULL(CAST(zd.Liczba_ofiar_smiertelnych AS INT), 0) AS Liczba_ofiar,
    0 AS Liczba_sprawcow, 
    0 AS Liczba_kar, 
    0 AS Suma_kwot_kar, 
    0 AS Suma_punktow_karnych
FROM dane_do_hurtowni.dbo.Zdarzenia z
LEFT JOIN dane_do_hurtowni.dbo.Zdarzenia_drogowe zd 
    ON z.ID_zdarzenia = zd.FK_Zdarzenia
INNER JOIN dbo.Zdarzenia dim_z ON
    dim_z.Kategoria = CAST(LEFT(LTRIM(RTRIM(z.Kategoria)), 20) AS VARCHAR(20))
    AND dim_z.Rodzaj = CAST(LEFT(LTRIM(RTRIM(z.Rodzaj)), 50) AS VARCHAR(50))
    AND dim_z.Warunki_pogodowe = CAST(LEFT(LTRIM(RTRIM(ISNULL(zd.Warunki_pogodowe, 'Brak danych'))), 50) AS VARCHAR(50))
LEFT JOIN (
    SELECT DISTINCT FK_Zdarzenia, Nr_patrolu 
    FROM dane_do_hurtowni.dbo.Kary 
    WHERE FK_Zdarzenia IS NOT NULL
) k ON z.ID_zdarzenia = k.FK_Zdarzenia
LEFT JOIN dane_do_hurtowni.dbo.Patrole p 
    ON k.Nr_patrolu = p.Nr_patrolu
WHERE z.ID_zdarzenia IS NOT NULL;
GO

INSERT INTO dbo.Interwencje_Fakty (
    ID_Zdarzenia,
    ID_Patrolu,
    ID_Daty,
    ID_Czasu,
    ID_Miejsca,
    Liczba_rannych,
    Liczba_ofiar,
    Liczba_sprawcow,
    Liczba_kar,
    Suma_kwot_kar,
    Suma_punktow_karnych
)
SELECT
    ID_Zdarzenia,
    ID_Patrolu,
    ID_Daty,
    ID_Czasu,
    ID_Miejsca,
    Liczba_rannych,
    Liczba_ofiar,
    Liczba_sprawcow,
    Liczba_kar,
    Suma_kwot_kar,
    Suma_punktow_karnych
FROM vETL_InterwencjeFakty v;
GO

DROP VIEW vETL_InterwencjeFakty;
GO