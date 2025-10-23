BULK INSERT Notowani FROM 'C:\temp\sql_data\snapshot2_data\notowani_new.bulk' WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001');
BULK INSERT Patrole FROM 'C:\temp\sql_data\snapshot2_data\patrole_new.csv' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', CODEPAGE = '65001', FIRSTROW = 2);
BULK INSERT Zdarzenia FROM 'C:\temp\sql_data\snapshot2_data\zdarzenia_new.bulk' WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001');
BULK INSERT Zdarzenia_drogowe FROM 'C:\temp\sql_data\snapshot2_data\zdarzenia_drogowe_new.bulk' WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001');
BULK INSERT Sprawcy_zdarzen FROM 'C:\temp\sql_data\snapshot2_data\sprawcy_zdarzen_new.bulk' WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001');
BULK INSERT Kary FROM 'C:\temp\sql_data\snapshot2_data\kary_new.bulk' WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001');
BULK INSERT Mandaty FROM 'C:\temp\sql_data\snapshot2_data\mandaty_new.bulk' WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001');
BULK INSERT Pouczenia FROM 'C:\temp\sql_data\snapshot2_data\pouczenia_new.bulk' WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001');
BULK INSERT Wnioski_do_sadu FROM 'C:\temp\sql_data\snapshot2_data\wnioski_do_sadu_new.bulk' WITH (FIELDTERMINATOR = '~|~', ROWTERMINATOR = '\n', CODEPAGE = '65001');

PRINT 'Nowe dane ze snapshotu 2 zaladowane pomyslnie!';
GO