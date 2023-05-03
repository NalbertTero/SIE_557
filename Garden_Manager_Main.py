__author__ = 'Nalbert Tero'
__copyright__ = "Copyright 2023"
__version__ = "1.0"
__date__ = "04/21/2023"

import tkinter as tk
from tkinter import ttk
import tkcalendar as tkc
from tkinter import filedialog
from tkinter import messagebox
import pymysql as psql

import db_config_file
import GM_db_functions as gdf

rows = []
num_rows = 0


# Defining functions for controlling application GUI behavior.
# --------------------------------------------------------------------------------------------------------------------------------

# Database testing function. -------------------------
def acknowledgeConnectionError():
    quit()

# Tab Control function. -----------------------------
def onTabSelected(event):

    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "Crop Records":

        existing_gardens_listbox.delete(0,'end')
        num_rows, rows = gdf.load_database_results(con, "SELECT * FROM gardens")
        for index, row in enumerate(rows):
            existing_gardens_listbox.insert(index, row[1])

        cultivar_list = ['Choose cultivar']
        num_cults, cults = gdf.load_database_results(con, "SELECT cultivar.CultivarName FROM cultivar")
        for c in cults:
            cultivar_list.append(c[0])
        addrecord_CultivarEntry['values'] = cultivar_list
        addrecord_CultivarEntry.set(cultivar_list[0])

    if tab_text == "Garden Plans":

        plans_listbox.delete(0, 'end')
        num_rows, rows = gdf.load_database_results(con, "SELECT * FROM gardens")
        for index, row in enumerate(rows):
            plans_listbox.insert(index, row[1])

    if tab_text == "Manage Cultivars":

        pass

    if tab_text == "Insights":

        pass

# Crop record functions. --------------------------
def onGardenSelect_Record(event):

    list = event.widget
    selection = event.widget.curselection()
    selected_garden = list.get(selection)

    if selected_garden is not None:
        for item in records_treeview.get_children():
            records_treeview.delete(item)

    bedlist = ['Choose planting bed']
    num_rows, rows = gdf.load_database_results(con, f"SELECT * FROM plantingbeds WHERE plantingbeds.InGarden = '{selected_garden}';")
    for row in rows:
        records_treeview.insert('', 'end', row[0], text=f'Bed {row[0]} - {row[1]} sq. ft.')
        num_records, records = gdf.load_database_results(con, f"SELECT * FROM croprecord LEFT JOIN cultivar ON croprecord.cultivar = cultivar.CultivarName WHERE croprecord.Bed = '{row[0]}'")
        for record in records:
            records_treeview.insert(row[0], 'end', record[1], text='', values=(record[2], record[1], record[12], record[4], record[5], record[6], record[7], record[8], record[9]))
        bedlist.append(row[0])
        addrecord_BedEntry['values'] = bedlist
        addrecord_BedEntry.set(bedlist[0])

def addCropRecord():

    bed = addrecord_BedEntry.get()
    year = addrecord_YearEntry.get()
    cultivar = addrecord_CultivarEntry.get()
    area = addrecord_AreaEntry.get()
    datePlant = addrecord_PlantedEntry.get_date()
    dateHarvest = addrecord_HarvestedEntry.get_date()
    datePulled = addrecord_PulledEntry.get_date()
    pest = addrecord_PestEntry.get()
    disease = addrecord_DiseaseEntry.get()
    if addrecord_FailureEntry.get() == 'No':
        failure = 0
    else:
        failure = 1

    sql = f"INSERT INTO croprecord " \
          f"(Cultivar, Year, Bed, SqFtPlanted, PlantingDate, HarvestDate, PullDate, DiseasePressure, PestPressure, Failure) VALUES" \
          f"('{cultivar}', {year}, {bed}, {area}, '{datePlant}', '{dateHarvest}', '{datePulled}', '{disease}', '{pest}', {failure})"

    gdf.insertIntoDatabase(con, sql)


def onGardenSelect_Plan(event):

    for item in plans_treeview.get_children():
        plans_treeview.delete(item)

    list = event.widget
    selection = event.widget.curselection()
    selected_garden = list.get(selection)

    num_rows, rows = gdf.load_database_results(con, f"SELECT * FROM plantingbeds WHERE plantingbeds.InGarden = '{selected_garden}';")
    for row in rows:
        plans_treeview.insert('', 'end', row[0], text=f'Bed {row[0]} - {row[1]} sq. ft.')
        num_records, records = gdf.load_database_results(con, f"SELECT * FROM cropplan LEFT JOIN cultivar ON cropplan.cultivar = cultivar.CultivarName WHERE cropplan.Bed = '{row[0]}'")
        for record in records:
            plans_treeview.insert(row[0], 'end', record[1], text='', values=(record[2], record[1], record[12], record[4], record[5], record[6], record[7], record[8], record[9]))


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
    root.geometry('1250x640')
    s = ttk.Style(root)
    s.theme_use('clam')

    program = ttk.Notebook(root)
    s.configure("TNotebook", tabposition='n')
    program.bind("<<NotebookTabChanged>>", onTabSelected)

    # Declare records tab.
    # --------------------------------------------------
    records_tab = ttk.Frame(program)
    program.add(records_tab, text='Crop Records')

    # Declare subframe for garden list ------------------
    garden_subframe = ttk.Frame(records_tab, borderwidth=2)
    garden_subframe.grid(column=0, row=0)

    existing_gardens_list_label = tk.Label(garden_subframe, text='Choose Garden', pady=5)
    existing_gardens_list_label.grid(column=0, row=0, sticky='n')

    existing_gardens_scrollbar = tk.Scrollbar(garden_subframe, orient="vertical", )

    existing_gardens_listbox = tk.Listbox(garden_subframe, yscrollcommand=existing_gardens_scrollbar.set)
    existing_gardens_listbox.grid(column=0, row=1,)
    existing_gardens_listbox.bind("<<ListboxSelect>>", onGardenSelect_Record)

    existing_gardens_scrollbar.config(command=existing_gardens_listbox.yview)
    existing_gardens_scrollbar.grid(column=0, row=1)

    # Declare subframe for crop records  ------------------
    records_subframe = ttk.Frame(records_tab)
    records_subframe.grid(column=1, row=0)

    tree_columns = ('Year', 'Cultivar', 'Family', 'Area', 'Planted', 'Harvested', 'Pulled', 'Pest', 'Disease')
    records_treeview = ttk.Treeview(records_subframe, columns=tree_columns, height=25)
    for column in tree_columns:
        records_treeview.column(column, width=80)
        records_treeview.heading(column, text=column)
    records_treeview.grid(column=0, row=0)

    # Declare subframe for adding crop records  ------------------
    addrecord_subframe = ttk.Frame(records_tab, borderwidth=2)
    addrecord_subframe.grid(column=2, row=0)

    addrecord_Label = tk.Label(addrecord_subframe, text= "Add record")
    addrecord_Label.grid(column=0, row=0, pady=10)

    addrecord_BedLabel = tk.Label(addrecord_subframe, text='Bed')
    addrecord_BedEntry = ttk.Combobox(addrecord_subframe, state='readonly')
    addrecord_BedLabel.grid(column=0, row=1, pady=(6,2), padx=10, sticky='w')
    addrecord_BedEntry.grid(column=0, row=2, pady=0, padx=10)

    addrecord_YearLabel = tk.Label(addrecord_subframe, text='Year')
    addrecord_YearEntry = tk.Entry(addrecord_subframe)
    addrecord_YearLabel.grid(column=0, row=3, pady=(6,2), padx=10, sticky='w')
    addrecord_YearEntry.grid(column=0, row=4, pady=0, padx=10)

    addrecord_CultivarLabel = tk.Label(addrecord_subframe, text='Cultivar')
    addrecord_CultivarEntry = ttk.Combobox(addrecord_subframe, state='readonly')
    addrecord_CultivarLabel.grid(column=0, row=5, pady=(6,2), padx=10, sticky='w')
    addrecord_CultivarEntry.grid(column=0, row=6, pady=0, padx=10)

    addrecord_AreaLabel = tk.Label(addrecord_subframe, text='Area')
    addrecord_AreaEntry = tk.Entry(addrecord_subframe)
    addrecord_AreaLabel.grid(column=0, row=7, pady=(6,2), padx=10, sticky='w')
    addrecord_AreaEntry.grid(column=0, row=8, pady=0, padx=10)

    addrecord_PlantedLabel = tk.Label(addrecord_subframe, text='Date Planted')
    addrecord_PlantedEntry = tkc.DateEntry(addrecord_subframe)
    addrecord_PlantedLabel.grid(column=0, row=9, pady=(6,2), padx=10, sticky='w')
    addrecord_PlantedEntry.grid(column=0, row=10, pady=0, padx=10, sticky='w')

    addrecord_HarvestedLabel = tk.Label(addrecord_subframe, text='Date Harvested')
    addrecord_HarvestedEntry = tkc.DateEntry(addrecord_subframe)
    addrecord_HarvestedLabel.grid(column=0, row=11, pady=(6,2), padx=10, sticky='w')
    addrecord_HarvestedEntry.grid(column=0, row=12, pady=0, padx=10, sticky='w')

    addrecord_PulledLabel = tk.Label(addrecord_subframe, text='Date Pulled')
    addrecord_PulledEntry = tkc.DateEntry(addrecord_subframe)
    addrecord_PulledLabel.grid(column=0, row=13, pady=(6,2), padx=10, sticky='w')
    addrecord_PulledEntry.grid(column=0, row=14, pady=0, padx=10, sticky='w')

    addrecord_PestLabel = tk.Label(addrecord_subframe, text='Pest')
    addrecord_PestEntry = ttk.Combobox(addrecord_subframe, state='readonly', values=['None', 'Low', 'Medium', 'High'])
    addrecord_PestEntry.set('None')
    addrecord_PestLabel.grid(column=0, row=15, pady=(6,2), padx=10, sticky='w')
    addrecord_PestEntry.grid(column=0, row=16, pady=0, padx=10)

    addrecord_DiseaseLabel = tk.Label(addrecord_subframe, text='Disease')
    addrecord_DiseaseEntry = ttk.Combobox(addrecord_subframe, state='readonly', values=['None', 'Low', 'Medium', 'High'])
    addrecord_DiseaseEntry.set('None')
    addrecord_DiseaseLabel.grid(column=0, row=17, pady=(6,2), padx=10, sticky='w')
    addrecord_DiseaseEntry.grid(column=0, row=18, pady=0, padx=10)

    addrecord_FailureLabel = tk.Label(addrecord_subframe, text='Failed?')
    addrecord_FailureEntry = ttk.Combobox(addrecord_subframe, state='readonly', values=['Yes', 'No'])
    addrecord_FailureEntry.set('No')
    addrecord_FailureLabel.grid(column=0, row=19, pady=(6,2), padx=10, sticky='w')
    addrecord_FailureEntry.grid(column=0, row=20, pady=0, padx=10)

    addrecord_button = tk.Button(addrecord_subframe, text='Add to records', command=addCropRecord)
    addrecord_button.grid(column=0, row=21, pady=5, padx=10)


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
    plans_listbox.bind("<<ListboxSelect>>", onGardenSelect_Plan)
    plans_scrollbar.grid(column=1, row=2)

    tree_columns = ('Year', 'Cultivar', 'Family', 'Area', 'Planted', 'Harvested', 'Pulled', 'Pest', 'Disease')
    plans_treeview = ttk.Treeview(plans_tab, columns=tree_columns, height=25)
    for column in tree_columns:
        plans_treeview.column(column, width=80)
        plans_treeview.heading(column, text=column)
    plans_treeview.grid(column=2, row=2)



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