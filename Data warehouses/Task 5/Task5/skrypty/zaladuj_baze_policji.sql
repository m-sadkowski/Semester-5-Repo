USE dane_do_hurtowni
GO

DELETE FROM dbo.Mandaty;
DELETE FROM dbo.Pouczenia;
DELETE FROM dbo.Wnioski_do_sadu;
DELETE FROM dbo.Zdarzenia_drogowe;
DELETE FROM dbo.Sprawcy_zdarzen;
DELETE FROM dbo.Kary;
DELETE FROM dbo.Patrole;
DELETE FROM dbo.Zdarzenia;
DELETE FROM dbo.Notowani;
GO

BULK INSERT Notowani 
FROM 'C:\temp\sql_data\snapshot1_data\notowani.bulk' 
WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001', FIRSTROW = 2);

BULK INSERT Patrole 
FROM 'C:\temp\sql_data\snapshot1_data\patrole.csv' 
WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', CODEPAGE = '65001', FIRSTROW = 2);

BULK INSERT Zdarzenia 
FROM 'C:\temp\sql_data\snapshot1_data\zdarzenia.bulk' 
WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001', FIRSTROW = 2);

BULK INSERT Zdarzenia_drogowe 
FROM 'C:\temp\sql_data\snapshot1_data\zdarzenia_drogowe.bulk' 
WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001', FIRSTROW = 2);

BULK INSERT Sprawcy_zdarzen 
FROM 'C:\temp\sql_data\snapshot1_data\sprawcy_zdarzen.bulk' 
WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001', FIRSTROW = 2);

BULK INSERT Kary 
FROM 'C:\temp\sql_data\snapshot1_data\kary.bulk' 
WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001', FIRSTROW = 2);

BULK INSERT Mandaty 
FROM 'C:\temp\sql_data\snapshot1_data\mandaty.bulk' 
WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001', FIRSTROW = 2);

BULK INSERT Pouczenia 
FROM 'C:\temp\sql_data\snapshot1_data\pouczenia.bulk' 
WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001', FIRSTROW = 2);

BULK INSERT Wnioski_do_sadu 
FROM 'C:\temp\sql_data\snapshot1_data\wnioski_do_sadu.bulk' 
WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001', FIRSTROW = 2);
GO