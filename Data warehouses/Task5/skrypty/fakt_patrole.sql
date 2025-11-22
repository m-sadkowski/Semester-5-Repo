USE baza
GO

IF OBJECT_ID('vETL_PatroleFakty', 'V') IS NOT NULL DROP VIEW vETL_PatroleFakty;
GO

CREATE VIEW vETL_PatroleFakty
AS
SELECT
    op.ID_Opisu_patrolu,
    dr.ID_Daty AS ID_Daty_rozpoczecia,
    dz.ID_Daty AS ID_Daty_zakonczenia,
    cr.ID_Czasu AS ID_Czasu_rozpoczecia,
    cz.ID_Czasu AS ID_Czasu_zakonczenia,
    m.ID_Miejsca,
    (SELECT TOP 1 ID_Smieci FROM dbo.Smieci WHERE Czy_interwencje = 0) AS ID_Smieci,
    DATEDIFF(MINUTE, p.Data_godzina_rozpoczecia, p.Data_godzina_zakonczenia) AS Czas_trwania_min,
    0 AS Liczba_interwencji
FROM dane_do_hurtowni.dbo.Patrole p
LEFT JOIN dbo.Opis_patrolu op ON 
    LTRIM(RTRIM(op.Nr_rejestracyjny)) = LTRIM(RTRIM(p.Nr_rejestracyjny))
    AND LTRIM(RTRIM(op.Nr_odznaki_kierowcy)) = LTRIM(RTRIM(p.Nr_odznaki_kierowcy))
    AND LTRIM(RTRIM(op.Nr_odznaki_partnera)) = LTRIM(RTRIM(p.Nr_odznaki_partnera))
LEFT JOIN dbo.Data dr ON dr.Data = CAST(p.Data_godzina_rozpoczecia AS DATE)
LEFT JOIN dbo.Data dz ON dz.Data = CAST(p.Data_godzina_zakonczenia AS DATE)
LEFT JOIN dbo.Czas cr ON DATEPART(HOUR, cr.Godzina) = DATEPART(HOUR, p.Data_godzina_rozpoczecia)
LEFT JOIN dbo.Czas cz ON DATEPART(HOUR, cz.Godzina) = DATEPART(HOUR, p.Data_godzina_zakonczenia)
LEFT JOIN dbo.Miejsce m ON LTRIM(RTRIM(m.Dzielnica)) = LEFT(LTRIM(RTRIM(p.Dzielnica_patrolu)), 20);
GO

INSERT INTO dbo.Patrole_Fakty (
    ID_Opisu_patrolu,
    ID_Daty_rozpoczecia,
    ID_Daty_zakonczenia,
    ID_Czasu_rozpoczecia,
    ID_Czasu_zakonczenia,
    ID_Miejsca,
    ID_Smieci,
    Czas_trwania_min,
    Liczba_interwencji
)
SELECT
    ID_Opisu_patrolu,
    ID_Daty_rozpoczecia,
    ID_Daty_zakonczenia,
    ID_Czasu_rozpoczecia,
    ID_Czasu_zakonczenia,
    ID_Miejsca,
    ID_Smieci,
    Czas_trwania_min,
    Liczba_interwencji
FROM vETL_PatroleFakty
WHERE ID_Opisu_patrolu IS NOT NULL;
GO

DROP VIEW vETL_PatroleFakty;
GO