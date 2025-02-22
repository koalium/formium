import FreeSimpleGUI as sg

import pandas as pd
import sqlite3

def get_table_names(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    conn.close()
    return tables

# Layout of the UI
layout = [
    [sg.Text('Select CSV File')],
    [sg.Input(), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
    [sg.Text('Database Name')],
    [sg.Input(default_text='data.db', key='-DB-')],
    [sg.Text('Table Name')],
    [sg.Input(key='-TABLE-NAME-')],
    [sg.Button('Load'), sg.Button('Exit')],
    [sg.Table(values=[], headings=[], key='-TABLE-')],
    [sg.Button('Add to DB')],
    [sg.Text('Available Databases')],
    [sg.Listbox(values=[], size=(30, 6), key='-DB-LIST-')],
    [sg.Button('Show Tables')],
    [sg.Listbox(values=[], size=(30, 6), key='-TABLE-LIST-')],
    [sg.Button('Show Table Data')]
]

# Create the window
window = sg.Window('CSV Loader', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Load':
        try:
            # Read the CSV file
            df = pd.read_csv(values[0])
            # Update the table with CSV data
            window['-TABLE-'].update(values=df.values.tolist(), headings=list(df.columns))
        except Exception as e:
            sg.popup_error(f"Error: {e}")
    elif event == 'Show Tables':
        try:
            db_name = values['-DB-']
            tables = get_table_names(db_name)
            window['-TABLE-LIST-'].update(values=tables)
        except Exception as e:
            sg.popup_error(f"Error: {e}")
    elif event == 'Show Table Data':
        try:
            db_name = values['-DB-']
            table_name = values['-TABLE-LIST-'][0]
            conn = sqlite3.connect(db_name)
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            conn.close()
            window['-TABLE-'].update(values=df.values.tolist(), headings=list(df.columns))
        except Exception as e:
            sg.popup_error(f"Error: {e}")



    if event == 'Add to DB':
        try:
            # Get the database and table name from user input
            db_name = values['-DB-']
            table_name = values['-TABLE-NAME-']
            
            # Connect to SQLite database (or create it)
            conn = sqlite3.connect(db_name)
            
            # Check if table exists
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if cursor.fetchone():
                sg.popup('Table already exists! Data will be appended.')
            else:
                sg.popup('Table does not exist. A new table will be created.')
            
            # Insert CSV data into the user-defined table
            df.to_sql(table_name, conn, if_exists='append', index=False)
            sg.popup('Data successfully added to database!')
        except Exception as e:
            sg.popup_error(f"Error: {e}")
        finally:
            conn.close()



window.close()
