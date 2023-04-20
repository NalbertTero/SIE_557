__author__ = 'Nalbert Tero'
__copyright__ = "Copyright 2023"
__version__ = "1.0"
__date__ = "03/18/2021"

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pymysql as psql

import db_config_file
import GM_GUI_functions as ggf
import GM_db_functions as gdf

#1. Attempt to establish connection to database.
status, con = gdf.open_database()

#2. Handle exceptions causing failure to connect.
if status == 0:
    error_window = tk.Tk()
    error_window.title('Database connection error!')
    error_window.geometry('768x264')
    error_frame = tk.Frame(error_window)
    s = ttk.Style(error_frame)
    s.theme_use('clam')
    error_frame.pack(expand='true')

    label1 = tk.Label(
        error_frame, anchor='s',
        font="Helvetica 14 bold",
        foreground="black", text=f"An error occurred while trying to connect to the database:\n{con}\nCheck that connection settings are correct.", padx=5)
    label1.pack()

    exit_button = tk.Button(error_frame, font="Helvetica 14 bold", text='Exit', fg='black',
                            command=ggf.acknowledgeConnectionError, padx=5)
    exit_button.pack(side='bottom')

    error_window.mainloop()

#3. Begin main application.
else:

    '''1. Create  the root program and notebook.'''
    root = tk.Tk()
    root.title('Garden Manager 1.0')
    root.geometry('1024x640')
    s = ttk.Style(root)
    s.theme_use('clam')

    program = ttk.Notebook(root)
    s.configure("TNotebook", tabposition='n')

    """2. Create the 'Gardens' tab with subtabs for viewing and creating gardens."""
    gardens_tab = ttk.Frame(program)
    program.add(gardens_tab, text='Gardens')

    gardens_subtabs = ttk.Notebook(gardens_tab)

    view_gardens_subtab = ttk.Frame(gardens_subtabs)
    gardens_subtabs.add(view_gardens_subtab, text='View Existing Gardens')

    existing_gardens_list = tk.Listbox(view_gardens_subtab)
    existing_gardens_list.pack()

    create_garden_subtab = ttk.Frame(gardens_subtabs)
    gardens_subtabs.add(create_garden_subtab, text='Create New Garden')

    gardens_subtabs.pack(expand=1, fill='both')

    """3. Create the 'Plans' tab with subtabs for viewing and creating plans."""
    plans_tab = ttk.Frame(program)
    program.add(plans_tab, text='Garden Planning')

    plans_subtabs = ttk.Notebook(plans_tab)

    view_plans_tab = ttk.Frame(plans_subtabs)
    plans_subtabs.add(view_plans_tab, text='View Existing Plans')

    create_plan_tab = ttk.Frame(plans_subtabs)
    plans_subtabs.add(create_plan_tab, text='Create New Plan')

    plans_subtabs.pack(expand=1, fill='both')

    """4. Create the 'Records' tab with subtabs for viewing and creating records."""
    records_tab = ttk.Frame(program)
    program.add(records_tab, text='Garden Records')

    records_subtabs = ttk.Notebook(records_tab)

    view_records_tab = ttk.Frame(records_subtabs)
    records_subtabs.add(view_records_tab, text='View Existing Records')

    create_records_tab = ttk.Frame(records_subtabs)
    records_subtabs.add(create_records_tab, text='Create New Records')

    records_subtabs.pack(expand=1, fill='both')





    num_gardens, gardens = gdf.query_database(con, 'SELECT * FROM gardens')
    for num, garden in enumerate(gardens):
        existing_gardens_list.insert(num, garden[1])

    program.pack(expand=1, fill='both')
    # ======== main loop ============ #
    root.mainloop()