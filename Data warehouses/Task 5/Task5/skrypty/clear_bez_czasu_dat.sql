USE baza
GO

EXEC sp_MSforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL';
GO

DELETE FROM dbo.Kary_Fakty;
DELETE FROM dbo.Interwencje_Fakty;
DELETE FROM dbo.Patrole_Fakty;
DELETE FROM dbo.Notowani;
DELETE FROM dbo.Opis_kary;
DELETE FROM dbo.Opis_patrolu;
DELETE FROM dbo.Zdarzenia;
DELETE FROM dbo.Miejsce;
DELETE FROM dbo.Smieci;
GO

DBCC CHECKIDENT ('dbo.Interwencje_Fakty', RESEED, 0);
DBCC CHECKIDENT ('dbo.Patrole_Fakty', RESEED, 0);
DBCC CHECKIDENT ('dbo.Notowani', RESEED, 0);
DBCC CHECKIDENT ('dbo.Opis_kary', RESEED, 0);
DBCC CHECKIDENT ('dbo.Opis_patrolu', RESEED, 0);
DBCC CHECKIDENT ('dbo.Zdarzenia', RESEED, 0);
DBCC CHECKIDENT ('dbo.Miejsce', RESEED, 0);
DBCC CHECKIDENT ('dbo.Smieci', RESEED, 0);
GO

EXEC sp_MSforeachtable 'ALTER TABLE ? WITH CHECK CHECK CONSTRAINT ALL';
GO