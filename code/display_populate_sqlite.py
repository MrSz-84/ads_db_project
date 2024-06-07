from typing import Any
import config.display as cf
import sqlite3
import pandas as pd
import numpy as np
import os
import sys
import time


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print('---Display populate sqlite part---')

file_path = cf.FILE_PATH


def iter_over_inputs(data_set: list[dict[str, Any] | dict[str, Any] | dict[str, Any] | dict[str, Any]],
                     con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    """
    Main loop for iteration over one column tables.

    :param data_set: List containing dicts with data, table name and field/column name.
    :param con: Is a connection object, pointing to a DB
    :param cur: Is a cursor object created for con object
    :raise KeyError: If key name does not match the pattern
    :raise sqlite3.ProgrammingError: If there are any error raised by the DB-API
    :raise sqlite3.OperationalError: If any exceptions on the DB side are raised, i.g. DB being
    locked
    :return: None
    """
    
    for elem in data_set:
        data = elem['data']
        table = elem['table']
        field = elem['field']
        table_type = elem['type']
        data_type = elem['dtype']
        new_data, data = check_for_data_1_field(data, table, field, data_type, cur)
        if new_data:
            add_1_field(data, table, field, table_type, data_type, con, cur)


def add_1_field(data: list, table_name: str, field_name: str, type_: str, dtype: str,
                con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    """
    Skeleton function for adding data to up to three column tables.
    :param type_: String representing type of target where to add the data. Available table or view
    :param data: List of strings or integers representing table contents
    :param table_name: String representing name of the table into which data is going to be added
    :param field_name: String representing the name of a column in destination table
    :param dtype: String representing to what type data should be converted before upload
    :param con: Is a connection object, pointing to a DB
    :param cur: Is a cursor object created for con object
    :raise sqlite3.ProgrammingError: If there are any error raised by the DB-API
    :raise sqlite3.OperationalError: If any exceptions on the DB side are raised, i.g. DB being
    locked
    :return: None
    """

    type_ = type_
    query = (f'INSERT INTO {table_name} ({field_name}) VALUES(:name);')
    for elem in data:
        if dtype.startswith('int'):
            to_add = {'name': int(elem)}
        else:
            to_add = {'name': str(elem)}
            
        cur.execute(query, to_add)
    con.commit()


def check_for_data_1_field(data_: list | pd.DataFrame, table_name: str, field_name: str, dtype: str,
                            cur: sqlite3.Cursor,) -> tuple[bool, list[str | int]]:
    """
    Skeleton function for checking if there is data inside each of one column tables.
    It adds data if there are any new entries, skips if no new data was found.
    If DB is empty returns immediately.

    :param data_: List containing data to be checked and added. Data is of str or int types.
    :param table_name: String representing name of the table into which data is going to be added
    :param field_name: String representing name of the field / column name
    :param dtype: String representing to what type data should be converted before upload
    :param cur: Is a cursor object created for con object
    :raise sqlite3.ProgrammingError: If there is an error raised by the DB-API
    :raise sqlite3.OperationalError: If any exceptions on the DB side are raised, i.g. DB being
    locked
    :return: A tuple containing bool for logic purposes, and the data set to be added
    :rtype: tuple[bool, list[str | int]]
    """
    
    query = (f"SELECT {field_name} FROM {table_name};")
    cur.execute(query)
    
    in_db = pd.DataFrame([elem[0] for elem in cur.fetchall()])
    in_db.rename(columns={0: field_name}, inplace=True)
    in_db = in_db.astype(dtype) # new

    if len(in_db) == 0:
        return (True, data_)

    data_ = pd.DataFrame(data_)
    data_ = data_.rename(columns={0: field_name})
    data_ = data_.astype({field_name: dtype})
    filtr = ~data_[field_name].isin(in_db[field_name])
    new_data = data_[filtr].dropna()
    new_data = new_data[field_name]
    
    new_data = list(new_data)
    
    if len(new_data) != 0:
        print(f'>>> Adding to {table_name}. New data found.')
        return (True, new_data)
    else:
        print(f'>>> Not adding to {table_name}. No new data found.')
        return (False, list(''))


def get_column_names(table_name: str, cur: sqlite3.Cursor) -> list[str]:
    """
    A function which returns the names of selected table from the DB.

    :param table_name: Name of a table out of which colum names are extracted from
    :param cur: A cursor database object
    :raise sqlite3.ProgrammingError: If column names does not match DB contents
    :raise sqlite3.OperationalError: If any exceptions on the DB side are raised, i.g. DB being locked
    :return: List containing all the column names present in selected table. 
    :rtype: list[str]
    """
    
    query = ("SELECT name FROM pragma_table_info(:table_name);")
    data = {'table_name': table_name}
    cur.execute(query, data)
    table_data = cur.fetchall()
    temp = []
    for elem in table_data[1:]:
        temp.append(elem[0])
    table_data = temp
    
    return table_data


def add_6_fields(data_set: dict[str, list[str] | str | Any], con: sqlite3.Connection,
                cur: sqlite3.Cursor) -> None:
    """
    Function adding data into placementy table, which consists of 6 columns.

    :param data_set: A dict containing data to be added, table name, and field / column name.
    Data is a Pandas DataFrame, table name and field name are both strings.
    :param con: A database connection object
    :param cur: A cursor database object
    :raise KeyError: If key name does not match the pattern
    :raise sqlite3.ProgrammingError: If column names don't fit into the table design
    :raise sqlite3.OperationalError: If any exceptions on the DB side are raised, i.g. DB being locked
    :return: None
    """
    
    query = (f"""
             INSERT INTO {data_set['table']} (
                {data_set['fields'][0]},
                {data_set['fields'][1]},
                {data_set['fields'][2]},
                {data_set['fields'][3]},
                {data_set['fields'][4]},
                {data_set['fields'][5]})
             VALUES(
                :{data_set['fields'][0]},
                :{data_set['fields'][1]},
                :{data_set['fields'][2]},
                :{data_set['fields'][3]},
                :{data_set['fields'][4]},
                :{data_set['fields'][5]})
             ;""")

    for _, elem in data_set['data'].iterrows():
        elem.Data = elem.Data.strftime('%Y-%m-%d')
        data = {field: elem for field, elem in zip(data_set['fields'], elem)}
        cur.execute(query, data)
        
    con.commit()


def get_id_for_placementy(fields: list[str], table_: str,
                        cur: sqlite3.Cursor) -> tuple[bool, pd.DataFrame]:
    """
    Gets IDs from reference tables to placementy table.
    Mainly connects other tables and data of singular ad emission via IDs with other tables.
    This function populates one of two core tables in this DB.
    Returns a bool for logic purposes and data to be added into placementy.

    :param fields: A list containing field / column names represented as a str
    :param table_: Name of the table out of which the data is going to be pulled, 
    represented as a str
    :param cur: A cursor database object
    :raise sqlite3.ProgrammingError: If column names don't fit into the table design
    :raise sqlite3.OperationalError: If any exceptions on the DB side are raised, i.g. DB being
    locked
    :return: Tuple containing bool for logic purposes and a Pandas DataFrame 
    as data to be added into the DB during the update or initial DB fill.
    :rtype: tuple[bool, pd.DataFrame]
    """
    
    placementy = df_d[['Data', 'wydawca', 'format', 'Urządzenie', 'Brand', 'PV', 'Zlepek']]

    query1 = ("SELECT wydawca, id FROM wydawcy;")
    cur.execute(query1)
    wydawca_id = dict(cur.fetchall())
    query2 =("SELECT format, id FROM formaty;")
    cur.execute(query2)
    format_id = dict(cur.fetchall())
    query3 = ("SELECT brand, id FROM brandy;")
    cur.execute(query3)
    brand_id = dict(cur.fetchall())
    query4 = ("SELECT urzadzenie, id FROM urzadzenia;")
    cur.execute(query4)
    urzadzenie_id = dict(cur.fetchall())
    
    placementy.loc[:, 'wydawca'] = placementy['wydawca'].map(wydawca_id)
    placementy.loc[:, 'format'] = placementy['format'].map(format_id)
    placementy.loc[:, 'Brand'] = placementy['Brand'].map(brand_id)
    placementy.loc[:, 'Urządzenie'] = placementy['Urządzenie'].map(urzadzenie_id)

    trigger, placementy = get_unique_record(fields, table_, placementy, cur)

    return (trigger, placementy)


def get_unique_record(fields: list[str], table_: str, dataframe: pd.DataFrame, 
                     cur: sqlite3.Cursor) -> tuple[bool, pd.DataFrame]:
    """
    Checks if given record is present in the DB. If not, allows data insertion into the DB, if so it
    informs the user, and proceeds with the rest of the code.

    :param fields: A list containing field / column names represented as a str
    :param table_: Name of the table out of which the data is going to be pulled, 
    represented as a str
    :param dataframe: Pandas DataFrame with the new data to be checked if not present in selected
    table
    :param cur: A cursor database object
    :raise sqlite3.ProgrammingError: If column names don't fit into the table design
    :raise sqlite3.OperationalError: If any exceptions on the DB side are raised, i.g. DB being locked
    :return: Tuple containing bool for logic purposes and a Pandas DataFrame 
    as data to be added into the DB during the update or initial DB fill.
    :rtype: tuple[bool, pd.DataFrame]
    """
    
    # Get dates range from DB
    query = (f"""
                SELECT {fields[0]} || brand || wydawca || format || urzadzenie
                FROM {table_}
                JOIN brandy ON brandy.id = placementy.brand_id
                JOIN wydawcy ON placementy.wydawca_id = wydawcy.id
                JOIN formaty ON placementy.format_id = formaty.id
                JOIN urzadzenia ON placementy.urzadzenie_id = urzadzenia.id;
            """)
    
    cur.execute(query)
    in_db = pd.DataFrame(cur.fetchall())
    in_db.rename(columns={0: 'Zlepek'}, inplace=True)
    
    # # Filter out dates that are already in DB.
    if not in_db.empty:
        filtr = ~dataframe['Zlepek'].isin(in_db['Zlepek'])
        dataframe = dataframe.loc[filtr]
    
    # Main logic add if empty or when dates not present in DB.
    if in_db.empty:
        return (True, dataframe)
    elif dataframe.empty:
        print(f'>>> Not adding to {table_}. One or more dates already in DB.')
        print(f'>>> Check the data you want to insert into DB.')
        return (False, dataframe)
    else:
        print(f'>>> Adding to {table_}. New data found.')
        return (True, dataframe)


main_dir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(main_dir)

m_start = time.time()
# Opens connection to the DB
print('Oppening connection.')
con = sqlite3.Connection(cf.DB_PATH)
cur = con.cursor()

print('Creating DataFrame.')
df_start = time.time()
# Reads the dataframe from EXCEL
dfs = pd.read_excel(file_path, sheet_name='aktywnosc_2024', thousands=' ', decimal=',', dtype={
                    'Rok': 'int16', 'wydawca': 'object', 'format': 'object',
                    'Brand': 'object', 'docelowe_staty': 'int64',
                    'Urządzenie' : 'object'},
                    parse_dates=['Data']
                    )
# df_d = pd.concat(dfs, ignore_index=True)
df_d = dfs
del dfs
df_d.rename(columns={'docelowe_staty': 'PV'}, inplace=True)
df_d['Brand'] = df_d['Brand'].str.strip()
df_d['Brand'] = df_d['Brand'].str.upper()
df_d['wydawca'] = df_d['wydawca'].str.strip()
df_d['wydawca'] = df_d['wydawca'].str.upper()
df_d['format'] = df_d['format'].str.strip()
df_d['format'] = df_d['format'].str.upper()
df_d['Urządzenie'] = df_d['Urządzenie'].str.strip()
df_d['Urządzenie'] = df_d['Urządzenie'].str.upper()
df_d['Zlepek'] = df_d['Data'].dt.strftime('%Y-%m-%d').astype('str') + df_d['Brand'] \
                  + df_d['wydawca'] + df_d['format'] + df_d['Urządzenie']
df_d.sort_values(by='Data', inplace=True, axis=0)
df_d.reset_index(inplace=True)
df_d.drop('index', axis=1, inplace=True)
df_end = time.time()
df_diff = df_end - df_start

# Create datasets for simple tables
dates = df_d['Data'].dt.strftime('%Y-%m-%d').unique()
brands = df_d['Brand'].unique()
pubs = df_d['wydawca'].unique()
formats = df_d['format'].unique()

data_set = [{'data': dates, **cf.DATES},
            {'data': pubs, **cf.PUBS},
            {'data': formats, **cf.FORMATS},
            {'data': brands, **cf.BRANDS},
            ]


# Inserting data into simple tables
ones_start = time.time()
print('Inserting data to one input tables.')
try:
    iter_over_inputs(data_set, con, cur)
except sqlite3.ProgrammingError as e:
    con.close()
    print('Failed to input the data.')
    print(f'Error: {e}')
except sqlite3.OperationalError as e:
    con.close()
    print('Failed to input the data.')
    print(f'Error: {e}')
    exit()
except sqlite3.IntegrityError as e:
    con.close()
    print('Failed to input the data.')
    print(f'Error: {e}')
    exit()
ones_end = time.time()
ones_diff = ones_end - ones_start


# Create and insert data into placementy table
six_start = time.time()
print('Inserting data to the five input table.')
fields = get_column_names('placementy', cur)
trigger, placementy = get_id_for_placementy(fields, 'placementy', cur)
data_set2 = {'data': placementy, 'table': 'placementy', 'fields': fields}
if trigger:
    try:
        add_6_fields(data_set2, con, cur)
    except sqlite3.ProgrammingError as e:
        con.close()
        print('Failed to input the data.')
        print(f'Error: {e}')
        exit()
    except sqlite3.OperationalError as e:
        con.close()
        print('Failed to input the data.')
        print(f'Error: {e}')
        exit()
    except sqlite3.IntegrityError as e:
        con.close()
        print('Failed to input the data.')
        print(f'Error: {e}')
        exit()
six_end = time.time()
six_diff = six_end - six_start


print('Closing connection.')
con.close()
m_end = time.time()
m_diff = m_end - m_start


print('Program has finished.')
print(f"""
Total time             : {m_diff:.2f}
DF creation            : {df_diff:.2f}
Ones processing time   : {ones_diff:.2f}
Sixes processing time  : {six_diff:.2f}
""")
