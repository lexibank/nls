db:
	rm NLS.sqlite || echo 'hello'
	cldf createdb ../cldf/cldf-metadata.json NLS.sqlite
	sqlite3 NLS.sqlite < db.sql
