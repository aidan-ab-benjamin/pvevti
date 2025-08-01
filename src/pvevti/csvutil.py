"""
A library of utilities relating to CSV opening, manipulation, saving, and conversions.
For help, explore the readme and the docs markdown files in the package source.
"""

import os
import pandas as pd

default_csv_dir   = os.path.expanduser("~")+"\\Downloads\\"

def read_csv(filepath:str):
    """
    Returns a latin-1 encoded CSV from the specified filepath in the form of a PD DF object
    """
    return pd.read_csv(filepath, encoding='latin-1')

def most_recent_csv(directory=default_csv_dir, ignore="", cascade = False):
    """
    Yields the complete path of the most recently modified CSV in the provided directory.
    Returns -1 if no CSVs exist.
    If left blank, searches the current user's downloads folder. 
    """
    files = os.listdir(directory)
    csv_files = [(directory + "\\" + file) for file in files if ".csv" in file and (ignore == "" or (ignore not in file))]
    if cascade:
        for path in os.listdir(directory):
            fullpath = os.path.join(directory, path)
            if os.path.isdir(fullpath):
                csv_files = csv_files + all_csvs(fullpath, ignore=ignore, cascade=True)
    csv_files.sort(key=os.path.getmtime)
    if len(csv_files) >= 1:
        return csv_files[-1]
    else:
        return -1

def all_csvs(directory, ignore="", cascade = False):
    """
    Yields a list of complete paths to CSV files located in the provided directory.
    Returns an empty list if no CSVs exist. Set cascade to True to iteratively search through sub-directories.
    """
    files = os.listdir(directory)
    csv_files = [(directory + "\\" + file) for file in files if ".csv" in file and (ignore == "" or (ignore not in file))]
    if cascade:
        for path in os.listdir(directory):
            fullpath = os.path.join(directory, path)
            if os.path.isdir(fullpath):
                csv_files = csv_files + all_csvs(fullpath, ignore=ignore, cascade=True)
    if len(csv_files) >= 1:
        return csv_files
    else:
        return []

def df_from_csv(csv_name, column_names=[]):
    """
    Yields a dataframe from a provided CSV (path). 
    Only passes specified column names unless none are specified, then passes the full table.
    """
    if type(column_names) == str:
        column_names = [column_names]

    if len(column_names) > 0:
        df = pd.read_csv(csv_name, usecols=column_names, encoding="latin-1", low_memory=False)
    else:
        df = pd.read_csv(csv_name, encoding="latin-1", low_memory=False)
    df.drop(df.columns[df.columns.str.contains('Unnamed', case=False)], axis=1, inplace=True)
    
    return df

def df_to_csv(df, csv_name, save_index=False, addition='_Filtered'):
    """
    Saves a provided pandas df to the provided csv path.
    Returns -1 if an error occurs in saving.
        df: dataframe object to save
        csv_name: full path of CSV
        save_index (optional): defaults to false, specifies saving the index columns.
        addition (optional): defaults to "_Filtered", specifies an appendage to add to the end of the literal CSV filename
    """
    csv_name = csv_name.split('.')[0] + addition + '.csv'
    try:
        df.to_csv(csv_name, index=save_index, encoding="latin-1")
    except Exception as e:
        if e.errno == 13:
            print("[Error 13] Failed to save CSV. Make sure the file destination is not open in another application.")
        else:
            print("[Error {e.errno}] Failed to save CSV.")
        return -1
    print("Saved DF to "+csv_name)
