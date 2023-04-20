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
import db_functions


"""1. Establish connection to database and handle possible exceptions."""
try:
    con = psql.connect(host=db_config_file.DB_SERVER,
                      user=db_config_file.DB_USER,
                      password=db_config_file.DB_PASS,
                      database=db_config_file.DB, port=db_config_file.DB_PORT)

except:

    error_window = tk.Tk()
    error_window.title('Database connection error!')
    error_window.geometry('640x480')

    message_frame = ttk.Frame(error_window)
    label = tk.Label(
        message_frame, compound=tk.CENTER,
        font="Helvetica 14 bold",
        foreground="black", text="Failed to connect to garden database."
                                  "\nCheck that connection settings are correct.")
    label.pack()

    error_window.mainloop()

else:

    '''1. Create  the root program and notebook.'''
    root = tk.Tk()
    root.title('Garden Manager 1.0')
    root.geometry('1024x640')

    program = ttk.Notebook(root)

    """2. Create the 'Gardens' tab with subtabs for viewing and creating gardens."""
    gardens_tab = ttk.Frame(program)
    program.add(gardens_tab, text='Gardens')

    gardens_subtabs = ttk.Notebook(gardens_tab)

    view_gardens_subtab = ttk.Frame(gardens_subtabs)
    gardens_subtabs.add(view_gardens_subtab, text='View Existing Garden')

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

    program.pack(expand=1, fill='both')



    # ======== main loop ============ #
    root.mainloop()