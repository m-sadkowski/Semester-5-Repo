USE baza
GO

-- Miary interwencji

IF OBJECT_ID('vAGR_InterwencjeMiary', 'V') IS NOT NULL DROP VIEW vAGR_InterwencjeMiary;
GO

CREATE VIEW vAGR_InterwencjeMiary
AS
SELECT 
    kf.ID_Interwencji,
    COUNT(DISTINCT kf.ID_Notowanego) AS Liczba_sprawcow,
    COUNT(kf.ID_Interwencji) AS Liczba_kar,
    SUM(kf.Kwota_mandatu) AS Suma_kwot_kar,
    SUM(kf.Punkty_karne) AS Suma_punktow_karnych
FROM dbo.Kary_Fakty kf
GROUP BY kf.ID_Interwencji;
GO

-- miar wyliczone z Kary_Fakty
UPDATE inf
SET 
    inf.Liczba_sprawcow = T.Liczba_sprawcow,
    inf.Liczba_kar = T.Liczba_kar,
    inf.Suma_kwot_kar = T.Suma_kwot_kar,
    inf.Suma_punktow_karnych = T.Suma_punktow_karnych
FROM dbo.Interwencje_Fakty inf
INNER JOIN vAGR_InterwencjeMiary AS T
    ON inf.ID_Interwencji = T.ID_Interwencji;
GO

DROP VIEW vAGR_InterwencjeMiary;
GO

-- Miary patroli

IF OBJECT_ID('vAGR_PatroleMiary', 'V') IS NOT NULL DROP VIEW vAGR_PatroleMiary;
GO

CREATE VIEW vAGR_PatroleMiary
AS
SELECT 
    inf.ID_Patrolu,
    COUNT(inf.ID_Interwencji) AS Liczba_interwencji
FROM dbo.Interwencje_Fakty inf
GROUP BY inf.ID_Patrolu;
GO

-- liczba interwencji (i czy_interwencje) wyliczone z Interwencje_Fakty
UPDATE pf
SET 
    pf.Liczba_interwencji = T.Liczba_interwencji
FROM dbo.Patrole_Fakty pf
INNER JOIN vAGR_PatroleMiary AS T
    ON pf.ID_Patrolu = T.ID_Patrolu;
GO

UPDATE pf
SET pf.ID_Smieci = (SELECT ID_Smieci FROM dbo.Smieci WHERE Czy_interwencje = 1)
FROM dbo.Patrole_Fakty pf
WHERE pf.Liczba_interwencji > 0;
GO

DROP VIEW vAGR_PatroleMiary;
GO