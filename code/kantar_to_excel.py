# -*- coding: utf-8 -*-
import config.find as find
import config.radio as cf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
import locale


print('---Kantar to Excel part---')
print('Program starting...')

# pobranie pliku
path = find.find(cf.FILE_PATH)

# tworzenie dataframe
df = pd.read_excel(path, sheet_name='Raport')
df_wyd = pd.read_excel(cf.BROADCASTER)
df_zas = pd.read_excel(cf.REACH)

print('DataFrame has been created...')


# funkcje dla operacji na dataframe za pomocą lambdy
def daypart(x: int) -> str:
    """
    Creates the information about the day part in which the ad was emitted.

    :param x: Integer representing hour of ad emission
    :return: a string representing the day part for table row
    :rtype: str
    """

    if x < 9:
        return 'do 9'
    elif x >= 9 and x < 16:
        return 'od 9 do 16'
    else:
        return 'po 16'


def ujednolicona(x: int) -> int:
    """
    Returns unified duration od advertisements.

    :param x: Integer representing ad duration
    :return: a unified duration for table row
    :rtype: int
    """

    if x <= 12:
        return 10
    elif x > 12 and x <= 17:
        return 15
    elif x > 17 and x <= 24:
        return 20
    elif x > 24 and x <= 37:
        return 30
    elif x > 37 and x <= 50:
        return 45
    else:
        return 60


# polish day of week names
polskie_dni_tyg = {
    'Monday': 'Poniedziałek',
    'Tuesday': 'Wtorek',
    'Wednesday': 'Środa',
    'Thursday': 'Czwartek',
    'Friday': 'Piątek',
    'Saturday': 'Sobota',
    'Sunday': 'Niedziela'
}

# operacja na dataframe tworzące potrzebne kolumny danych do późniejszego zapisu do pliku
# dataframe operations creating needed data columns for further write to the file.
df['Start'] = pd.to_datetime(df['Start'], format='%H:%M:%S')
locale.setlocale(locale.LC_TIME, 'pl_PL.utf8')
df.rename(columns={'Medium': 'Submedium'}, inplace=True)
df['Dzień'] = df['Data'].dt.day.astype('int')
df['Dzień tygodnia'] = df['Data'].dt.day_name()
df['Dzień tygodnia'] = df['Dzień tygodnia'].map(polskie_dni_tyg)
df['Dzień tygodnia'] = df['Dzień tygodnia'].str.title()
df['Nr. tyg.'] = df['Data'].dt.isocalendar().week.astype('int')
df['Rok'] = df['Data'].dt.year
df['Miesiąc'] = df['Data'].dt.month
df['GG'] = df['Start'].dt.hour
df['MM'] = df['Start'].dt.minute
df['SS'] = df['Start'].dt.second
df['L.emisji'] = 1
df['Typ reklamy'] = 'reklama'
df = pd.merge(df, df_wyd, on='Submedium', how='left')
df = pd.merge(df, df_zas, on='Submedium', how='left')
df['Daypart'] = df['GG'].apply(daypart)
df['dł. Ujednolicona'] = df['dł./mod.'].apply(ujednolicona)
df['Godzina bloku reklamowego'] = df.apply(lambda x: f'{x["GG"]}:00-{x["GG"]}:29' if x['MM'] < 30 else f'{x["GG"]}:30-{x["GG"]}:59', axis=1)
df.sort_values(by=['Data'], axis=0, ascending=True, inplace=True)

print('Data operations has ended...')

# utworzenie dataframe do zapisu i zapis do pliku
# creation of the final dataframe which is going to be written to the output file
df_to_excel = df[['Data', 'Dzień', 'Dzień tygodnia', 'Nr. tyg.', 'Rok', 'Miesiąc', 'Zasięg medium', 'Brand', 'Produkt(4)', 'Kod Reklamy', 'Opis Reklamy',
                  'Wydawca/Nadawca', 'Typ reklamy', 'Submedium', 'dł./mod.', 'GG', 'MM', 'SS', 'Koszt [zł]', 'L.emisji', 'Daypart', 'dł. Ujednolicona', 'Godzina bloku reklamowego',
                  ]]
with pd.ExcelWriter('#kantar_output.xlsx', mode='w', engine='xlsxwriter', date_format="YYYY-MM-DD", datetime_format="YYYY-MM-DD") as writer:
    sheet_name = f'kantar_{df_to_excel["Rok"].unique()[0]}_{df_to_excel["Miesiąc"].unique()[0]}'
    df_to_excel.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f'Saved to a file "#kantar_output.xlsx" ...')

print('Program has ended.')



