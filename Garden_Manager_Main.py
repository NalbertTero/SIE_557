__author__ = 'Nalbert Tero'
__copyright__ = "Copyright 2023"
__version__ = "1.0"
__date__ = "04/21/2023"

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pymysql as psql

import db_config_file
import GM_db_functions as gdf

rows = []
num_rows = 0


# Defining functions for controlling application GUI behavior.
# --------------------------------------------------------------------------------------------------------------------------------

def acknowledgeConnectionError():
    quit()
def on_tab_selected(event):

    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "Garden Records":

        existing_gardens_listbox.delete(0,'end')
        num_rows, rows = gdf.load_database_results(con, "SELECT * FROM gardens")
        for index, row in enumerate(rows):
            existing_gardens_listbox.insert(index, row[1])

    if tab_text == "Garden Plans":

        plans_listbox.delete(0, 'end')
        num_rows, rows = gdf.load_database_results(con, "SELECT * FROM gardens")
        for index, row in enumerate(rows):
            plans_listbox.insert(index, row[1])

    if tab_text == "Manage Cultivars":

        #messagebox.showinfo("This tab is not yet implemented...")
        pass

    if tab_text == "Insights":

        messagebox.showinfo("This tab is not yet implemented...")

def onGardenSelect(event):

    for item in chosen_garden_records.get_children():
        chosen_garden_records.delete(item)

    list = event.widget
    selection = event.widget.curselection()
    selected_garden = list.get(selection)

    num_rows, rows = gdf.load_database_results(con, f"SELECT * FROM plantingbeds WHERE plantingbeds.InGarden = '{selected_garden}';")
    for row in rows:
        chosen_garden_records.insert('', 'end', row[0], text=f'Bed {row[0]} - {row[1]} sq. ft.')
        num_records, records = gdf.load_database_results(con, f"SELECT * FROM croprecord LEFT JOIN cultivar ON croprecord.cultivar = cultivar.CultivarName WHERE croprecord.Bed = '{row[0]}'")
        for record in records:
            chosen_garden_records.insert(row[0], 'end', record[1], text='', values=(record[2], record[1], record[12], record[4], record[5], record[6], record[7], record[8], record[9]))


# Test database connection by attempting to establish a connection.
# If the connection attempt fails, the program will exit with a warning message.
# --------------------------------------------------------------------------------------------------------------------------------

status, con = gdf.open_database()

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
                            command=acknowledgeConnectionError, padx=5)
    exit_button.pack(side='bottom')

    error_window.mainloop()


# If connection tests successfully, declare and launch main application.
# --------------------------------------------------------------------------------------------------------------------------------

else:

    # Create the root program and notebook to hold tabs.
    # --------------------------------------------------
    root = tk.Tk()
    root.title('Garden Manager 1.0')
    root.geometry('1300x640')
    s = ttk.Style(root)
    s.theme_use('clam')

    program = ttk.Notebook(root)
    s.configure("TNotebook", tabposition='n')
    program.bind("<<NotebookTabChanged>>", on_tab_selected)

    # Declare records tab.
    # --------------------------------------------------
    records_tab = ttk.Frame(program)
    program.add(records_tab, text='Garden Records')

    existing_gardens_list_label = tk.Label(records_tab, text='Existing Gardens', pady=5)
    existing_gardens_list_label.grid(column=0, row=1)
    existing_gardens_scrollbar = tk.Scrollbar(records_tab, orient="vertical", )
    existing_gardens_listbox = tk.Listbox(records_tab, yscrollcommand=existing_gardens_scrollbar.set)
    existing_gardens_scrollbar.config(command=existing_gardens_listbox.yview)
    existing_gardens_listbox.grid(column=0, row=2,)
    existing_gardens_listbox.bind("<<ListboxSelect>>", onGardenSelect)
    existing_gardens_scrollbar.grid(column=1, row=2)

    tree_columns = ('Year', 'Cultivar', 'Family', 'Area', 'Planted', 'Harvested', 'Pulled', 'Pest', 'Disease')
    chosen_garden_records = ttk.Treeview(records_tab, columns=tree_columns, height=25)
    for column in tree_columns:
        chosen_garden_records.column(column, width=80)
        chosen_garden_records.heading(column, text=column)
    chosen_garden_records.grid(column=2, row=2)

    # Declare plans tab.
    # --------------------------------------------------
    plans_tab = ttk.Frame(program)
    program.add(plans_tab, text='Garden Plans')

    plans_list_label = tk.Label(plans_tab, text='Garden Plans', pady=5)
    plans_list_label.grid(column=0, row=1)
    plans_scrollbar = tk.Scrollbar(plans_tab, orient="vertical", )
    plans_listbox = tk.Listbox(plans_tab, yscrollcommand=plans_scrollbar.set)
    plans_scrollbar.config(command=plans_listbox.yview)
    plans_listbox.grid(column=0, row=2,)
    plans_listbox.bind("<<ListboxSelect>>", onGardenSelect)
    plans_scrollbar.grid(column=1, row=2)

    tree_columns = ('Year', 'Cultivar', 'Family', 'Area', 'Planted', 'Harvested', 'Pulled', 'Pest', 'Disease')
    chosen_garden_records = ttk.Treeview(plans_tab, columns=tree_columns, height=25)
    for column in tree_columns:
        chosen_garden_records.column(column, width=80)
        chosen_garden_records.heading(column, text=column)
    chosen_garden_records.grid(column=2, row=2)

    # Declare manage tab.
    # --------------------------------------------------
    manage_tab = ttk.Frame(program)
    program.add(manage_tab, text='Manage Cultivars')

    # Declare insights tab.
    # --------------------------------------------------
    insights_tab = ttk.Frame(program)
    program.add(insights_tab, text='Insights')



    program.pack(expand=1, fill='both')
    # ======== main loop ============ #
    root.mainloop()