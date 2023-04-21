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

rows = []
num_rows = 0

def acknowledgeConnectionError():
    quit()
def on_tab_selected(event):

    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "View Existing Records":

        existing_gardens_listbox.delete(0,'end')
        num_rows, rows = gdf.load_database_results(con, "SELECT * FROM gardens")
        for index, row in enumerate(rows):
            existing_gardens_listbox.insert(index, row[1])

    if tab_text == "Add New Records":

        messagebox.showinfo("This tab is not yet implemented...")

    if tab_text == "View Existing Plans":

        #messagebox.showinfo("This tab is not yet implemented...")
        pass

    if tab_text == "Create New Plan":

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
            print(record)
            chosen_garden_records.insert(row[0], 'end', record[1], text='Amish Paste Tomato', values=(record[2], record[1], record[12], record[4], record[5], record[6], record[7], record[8], record[9]))





# 1. Attempt to establish connection to database as a test.
status, con = gdf.open_database()

# 2. Handle exceptions causing failure to connect.
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

# 3. Begin main application.
else:

    # 3-A. Create  the root program and notebook.
    root = tk.Tk()
    root.title('Garden Manager 1.0')
    root.geometry('1300x640')
    s = ttk.Style(root)
    s.theme_use('clam')

    program = ttk.Notebook(root)
    s.configure("TNotebook", tabposition='n')

    # 3-B. Create the 'Records' tab with subtabs for viewing and adding records.
    records_tab = ttk.Frame(program)
    program.add(records_tab, text='Garden Records')

    records_subtabs = ttk.Notebook(records_tab)
    records_subtabs.bind("<<NotebookTabChanged>>", on_tab_selected)

    view_records_subtab = ttk.Frame(records_subtabs)
    records_subtabs.add(view_records_subtab, text='View Existing Records')

    existing_gardens_list_label = tk.Label(view_records_subtab, text='Existing Gardens', pady=5)
    existing_gardens_list_label.grid(column=0, row=1)
    existing_gardens_scrollbar = tk.Scrollbar(view_records_subtab, orient="vertical", )
    existing_gardens_listbox = tk.Listbox(view_records_subtab, yscrollcommand=existing_gardens_scrollbar.set)
    existing_gardens_scrollbar.config(command=existing_gardens_listbox.yview)
    existing_gardens_listbox.grid(column=0, row=2,)
    existing_gardens_listbox.bind("<<ListboxSelect>>", onGardenSelect)
    existing_gardens_scrollbar.grid(column=1, row=2)

    tree_columns = ('Year', 'Cultivar', 'Family', 'Area', 'Planted', 'Harvested', 'Pulled', 'Pest', 'Disease')
    chosen_garden_records = ttk.Treeview(view_records_subtab, columns=tree_columns, height=25)
    for column in tree_columns:
        chosen_garden_records.column(column, width=100)
        chosen_garden_records.heading(column, text=column)
    chosen_garden_records.grid(column=2, row=2)

    add_records_subtab = ttk.Frame(records_subtabs)
    records_subtabs.add(add_records_subtab, text='Add New Records')

    records_subtabs.pack(expand=1, fill='both')

    # 3-C. Create the 'Plans' tab with subtabs for viewing and creating plans.
    plans_tab = ttk.Frame(program)
    program.add(plans_tab, text='Garden Plans')

    plans_subtabs = ttk.Notebook(plans_tab)
    plans_subtabs.bind("<<NotebookTabChanged>>", on_tab_selected)

    view_plans_tab = ttk.Frame(plans_subtabs)
    plans_subtabs.add(view_plans_tab, text='View Existing Plans')

    create_plan_tab = ttk.Frame(plans_subtabs)
    plans_subtabs.add(create_plan_tab, text='Create New Plan')

    plans_subtabs.pack(expand=1, fill='both')



    program.pack(expand=1, fill='both')
    # ======== main loop ============ #
    root.mainloop()