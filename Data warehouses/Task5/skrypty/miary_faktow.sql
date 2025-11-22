USE baza
GO

UPDATE I
SET 
    I.Liczba_kar = ISNULL(K.Liczba, 0),
    I.Suma_kwot_kar = ISNULL(K.Kwota, 0),
    I.Suma_punktow_karnych = ISNULL(K.Punkty, 0),
    I.Liczba_sprawcow = ISNULL(K.Sprawcy, 0)
FROM dbo.Interwencje_Fakty I
LEFT JOIN (
    SELECT 
        ID_Interwencji,
        COUNT(*) AS Liczba,
        SUM(Kwota_mandatu) AS Kwota,  
        SUM(Punkty_karne) AS Punkty,
        COUNT(DISTINCT ID_Notowanego) AS Sprawcy 
    FROM dbo.Kary_Fakty
    GROUP BY ID_Interwencji
) K ON I.ID_Interwencji = K.ID_Interwencji;
GO

UPDATE P
SET P.Liczba_interwencji = ISNULL(I.Cnt, 0)
FROM dbo.Patrole_Fakty P
LEFT JOIN (
    SELECT ID_Patrolu, COUNT(*) AS Cnt
    FROM dbo.Interwencje_Fakty
    GROUP BY ID_Patrolu
) I ON P.ID_Patrolu = I.ID_Patrolu;
GO

UPDATE dbo.Patrole_Fakty
SET ID_Smieci = (SELECT TOP 1 ID_Smieci FROM dbo.Smieci WHERE Czy_interwencje = 0)
WHERE Liczba_interwencji = 0;

UPDATE dbo.Patrole_Fakty
SET ID_Smieci = (SELECT TOP 1 ID_Smieci FROM dbo.Smieci WHERE Czy_interwencje = 1)
WHERE Liczba_interwencji > 0;
GO