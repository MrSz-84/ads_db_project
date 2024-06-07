# Settings for display_populate_sqlite.py script.
# If needed please adjust DB_PATH and FILE_PATH parameters. The first one is the path to DB file.
# The second is the path for source information containing display ads data.

DB_PATH = '../bazy_danych/display_ads.db'
FILE_PATH = './query.xlsx'
DATES = {'table': 'data_czas', 'field': 'data', 'type': 'table', "dtype": 'object'}
PUBS = {'table': 'wydawcy', 'field': 'wydawca', 'type': 'table', "dtype": 'object'}
FORMATS = {'table': 'formaty', 'field': 'format', 'type': 'table', "dtype": 'object'}
BRANDS = {'table': 'brandy', 'field': 'brand', 'type': 'tab;e', "dtype": 'object'}

