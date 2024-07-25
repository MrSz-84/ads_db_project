# Settings for kantar_to_excel.py and radio_populate_sqlite.py scripts.
# If needed please adjust DB_PATH, FILE_PATH and SOURCE_PATH parameters.
# The first one is the path to DB file. The second is the path for source information containing
# radio ads data which is going to be used by processing script for creation of proper table
# and data format. The last one is the path for output file from which data is going to be added
# into the DB.

DB_PATH = '../bazy_danych/radio_ads.db'
DB_TEST = '../bazy_danych/radio_ads_test.db'
FILE_PATH = '../../Radio/Raporty Kantar/2024/7. Lipiec/'
SOURCE_PATH = './#kantar_output.xlsx'
REACH = './zasieg_medium.xlsx'
EMMITER = './wydawca_nadawca.xlsx'
