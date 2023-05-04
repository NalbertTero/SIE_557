__author__ = 'Nalbert Tero'
__copyright__ = "Copyright 2023"
__version__ = "1.0"
__date__ = "04/21/2023"

import tkinter as tk
from tkinter import ttk
import tkcalendar as tkc
from datetime import datetime as dt
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
        alterrecord_CultivarEntry['values'] = cultivar_list
        alterrecord_CultivarEntry.set(cultivar_list[0])

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
    global Selected_Garden_Records
    list = event.widget
    selection = event.widget.curselection()
    selected_garden = list.get(selection)

    Selected_Garden_Records = selected_garden

    if selected_garden is not None:
        for item in records_treeview.get_children():
            records_treeview.delete(item)

    bedlist = ['Choose planting bed']
    num_rows, rows = gdf.load_database_results(con, f"SELECT * FROM plantingbeds WHERE plantingbeds.InGarden = '{selected_garden}';")
    for row in rows:
        records_treeview.insert('', 'end', row[0], text=f'Bed {row[0]} - {row[1]} sq. ft.')
        num_records, records = gdf.load_database_results(con, f"SELECT * FROM croprecord LEFT JOIN cultivar ON croprecord.cultivar = cultivar.CultivarName WHERE croprecord.Bed = '{row[0]}'")
        for record in records:
            records_treeview.insert(row[0], 'end', record[1], text='', values=(record[2], record[1], record[12], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[0]))
        bedlist.append(row[0])
        addrecord_BedEntry['values'] = bedlist
        addrecord_BedEntry.set(bedlist[0])
        alterrecord_BedEntry['values'] = bedlist
        alterrecord_BedEntry.set(bedlist[0])

def onRecordSelect(event):
    records = event.widget

    alterrecord_BedEntry.set('')
    alterrecord_YearEntry.delete(0, 'end')
    alterrecord_CultivarEntry.set('')
    alterrecord_AreaEntry.delete(0, 'end')
    alterrecord_PestEntry.set('')
    alterrecord_DiseaseEntry.set('')
    alterrecord_FailureEntry.set('')

    selected_record = records.focus()
    parent_bed = records.parent(selected_record)
    selected_values = records_treeview.item(selected_record)

    alterrecord_BedEntry.set(f'{parent_bed}')
    alterrecord_YearEntry.insert(0, selected_values['values'][0])
    alterrecord_CultivarEntry.set(selected_values['values'][1])
    alterrecord_AreaEntry.insert(0, selected_values['values'][3])
    alterrecord_PlantedEntry.set_date(dt.strptime(selected_values['values'][4], '%Y-%m-%d'))
    alterrecord_HarvestedEntry.set_date(dt.strptime(selected_values['values'][5], '%Y-%m-%d'))
    alterrecord_PulledEntry.set_date(dt.strptime(selected_values['values'][6], '%Y-%m-%d'))
    alterrecord_PestEntry.set(selected_values['values'][7])
    alterrecord_DiseaseEntry.set(selected_values['values'][8])
    alterrecord_FailureEntry.set(selected_values['values'][9])

def onAddButtonPress():
    addrecord_subframe.tkraise()

def onAlterButtonPress():
    alterrecord_subframe.tkraise()

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
    failure = addrecord_FailureEntry.get()

    sql = f"INSERT INTO croprecord " \
          f"(Cultivar, Year, Bed, SqFtPlanted, PlantingDate, HarvestDate, PullDate, DiseasePressure, PestPressure, Failure) VALUES" \
          f"('{cultivar}', {year}, {bed}, {area}, '{datePlant}', '{dateHarvest}', '{datePulled}', '{disease}', '{pest}', '{failure}')"

    gdf.insertIntoDatabase(con, sql)

def alterCropRecord():
    selected = records_treeview.focus()
    selected_item = records_treeview.item(selected)
    cropID = selected_item['values'][10]

    bed = alterrecord_BedEntry.get()
    year = alterrecord_YearEntry.get()
    cultivar = alterrecord_CultivarEntry.get()
    area = alterrecord_AreaEntry.get()
    datePlant = alterrecord_PlantedEntry.get_date()
    dateHarvest = alterrecord_HarvestedEntry.get_date()
    datePulled = alterrecord_PulledEntry.get_date()
    pest = alterrecord_PestEntry.get()
    disease = alterrecord_DiseaseEntry.get()
    failure = alterrecord_FailureEntry.get()

    sql = f"UPDATE croprecord " \
          f" SET Cultivar = '{cultivar}', Year = '{year}', Bed = '{bed}', SqFtPlanted = '{area}', PlantingDate = '{datePlant}', " \
          f"HarvestDate = '{dateHarvest}', PullDate = '{datePulled}', DiseasePressure = '{disease}', PestPressure = '{pest}', Failure = '{failure}'" \
          f"WHERE CropID = {cropID}"

    gdf.insertIntoDatabase(con, sql)

    if Selected_Garden_Records is not None:
        for item in records_treeview.get_children():
            records_treeview.delete(item)

    bedlist = ['Choose planting bed']
    num_rows, rows = gdf.load_database_results(con, f"SELECT * FROM plantingbeds WHERE plantingbeds.InGarden = '{Selected_Garden_Records}';")
    for row in rows:
        records_treeview.insert('', 'end', row[0], text=f'Bed {row[0]} - {row[1]} sq. ft.', open=True)
        num_records, records = gdf.load_database_results(con, f"SELECT * FROM croprecord LEFT JOIN cultivar ON croprecord.cultivar = cultivar.CultivarName WHERE croprecord.Bed = '{row[0]}'")
        for record in records:
            records_treeview.insert(row[0], 'end', record[1], text='', values=(record[2], record[1], record[12], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[0]))
        bedlist.append(row[0])
        alterrecord_BedEntry['values'] = bedlist
        alterrecord_BedEntry.set(bedlist[0])

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
            plans_treeview.insert(row[0], 'end', record[1], text='', values=(record[2], record[1], record[12], record[4], record[5], record[6], record[7], record[8], record[9], record[0]))


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

    tree_columns = ('Year', 'Cultivar', 'Family', 'Area', 'Planted', 'Harvested', 'Pulled', 'Pest', 'Disease', 'Failure', 'ID')
    records_treeview = ttk.Treeview(records_subframe, columns=tree_columns, height=25)
    for column in tree_columns[:-1]:
        records_treeview.column(column, width=75)
        records_treeview.heading(column, text=column)
    records_treeview.column('ID', width=0)
    records_treeview.bind("<<TreeviewSelect>>", onRecordSelect)
    records_treeview.grid(column=0, row=0)

    add_record_button = tk.Button(records_subframe, text='Add new record', command=onAddButtonPress)
    add_record_button.grid(column=0, row=2, sticky='w', pady=(6,0))

    alter_record_button = tk.Button(records_subframe, text='Alter selected record', command=onAlterButtonPress)
    alter_record_button.grid(column=0, row=2, pady=(6,0))

    delete_record_button = tk.Button(records_subframe, text='Delete selected record')
    delete_record_button.grid(column=0, row=2, sticky='e', pady=(6,0))

    # Declare subframe for altering crop records  ------------------
    alterrecord_subframe = ttk.Frame(records_tab)
    alterrecord_subframe.grid(column=2, row=0)

    alterrecord_Label = tk.Label(alterrecord_subframe, text="Alter record")
    alterrecord_Label.grid(column=0, row=0, pady=10)

    alterrecord_BedLabel = tk.Label(alterrecord_subframe, text='Bed')
    alterrecord_BedEntry = ttk.Combobox(alterrecord_subframe, state='readonly')
    alterrecord_BedLabel.grid(column=0, row=1, pady=(6,2), padx=10, sticky='w')
    alterrecord_BedEntry.grid(column=0, row=2, pady=0, padx=10)

    alterrecord_YearLabel = tk.Label(alterrecord_subframe, text='Year')
    alterrecord_YearEntry = tk.Entry(alterrecord_subframe)
    alterrecord_YearLabel.grid(column=0, row=3, pady=(6,2), padx=10, sticky='w')
    alterrecord_YearEntry.grid(column=0, row=4, pady=0, padx=10)

    alterrecord_CultivarLabel = tk.Label(alterrecord_subframe, text='Cultivar')
    alterrecord_CultivarEntry = ttk.Combobox(alterrecord_subframe, state='readonly')
    alterrecord_CultivarLabel.grid(column=0, row=5, pady=(6,2), padx=10, sticky='w')
    alterrecord_CultivarEntry.grid(column=0, row=6, pady=0, padx=10)

    alterrecord_AreaLabel = tk.Label(alterrecord_subframe, text='Area')
    alterrecord_AreaEntry = tk.Entry(alterrecord_subframe)
    alterrecord_AreaLabel.grid(column=0, row=7, pady=(6,2), padx=10, sticky='w')
    alterrecord_AreaEntry.grid(column=0, row=8, pady=0, padx=10)

    alterrecord_PlantedLabel = tk.Label(alterrecord_subframe, text='Date Planted')
    alterrecord_PlantedEntry = tkc.DateEntry(alterrecord_subframe)
    alterrecord_PlantedLabel.grid(column=0, row=9, pady=(6,2), padx=10, sticky='w')
    alterrecord_PlantedEntry.grid(column=0, row=10, pady=0, padx=10, sticky='w')

    alterrecord_HarvestedLabel = tk.Label(alterrecord_subframe, text='Date Harvested')
    alterrecord_HarvestedEntry = tkc.DateEntry(alterrecord_subframe)
    alterrecord_HarvestedLabel.grid(column=0, row=11, pady=(6,2), padx=10, sticky='w')
    alterrecord_HarvestedEntry.grid(column=0, row=12, pady=0, padx=10, sticky='w')

    alterrecord_PulledLabel = tk.Label(alterrecord_subframe, text='Date Pulled')
    alterrecord_PulledEntry = tkc.DateEntry(alterrecord_subframe)
    alterrecord_PulledLabel.grid(column=0, row=13, pady=(6,2), padx=10, sticky='w')
    alterrecord_PulledEntry.grid(column=0, row=14, pady=0, padx=10, sticky='w')

    alterrecord_PestLabel = tk.Label(alterrecord_subframe, text='Pest')
    alterrecord_PestEntry = ttk.Combobox(alterrecord_subframe, state='readonly', values=['None', 'Low', 'Medium', 'High'])
    alterrecord_PestEntry.set('None')
    alterrecord_PestLabel.grid(column=0, row=15, pady=(6,2), padx=10, sticky='w')
    alterrecord_PestEntry.grid(column=0, row=16, pady=0, padx=10)

    alterrecord_DiseaseLabel = tk.Label(alterrecord_subframe, text='Disease')
    alterrecord_DiseaseEntry = ttk.Combobox(alterrecord_subframe, state='readonly', values=['None', 'Low', 'Medium', 'High'])
    alterrecord_DiseaseEntry.set('None')
    alterrecord_DiseaseLabel.grid(column=0, row=17, pady=(6,2), padx=10, sticky='w')
    alterrecord_DiseaseEntry.grid(column=0, row=18, pady=0, padx=10)

    alterrecord_FailureLabel = tk.Label(alterrecord_subframe, text='Failed?')
    alterrecord_FailureEntry = ttk.Combobox(alterrecord_subframe, state='readonly', values=['Yes', 'No'])
    alterrecord_FailureEntry.set('No')
    alterrecord_FailureLabel.grid(column=0, row=19, pady=(6,2), padx=10, sticky='w')
    alterrecord_FailureEntry.grid(column=0, row=20, pady=0, padx=10)

    alterrecord_button = tk.Button(alterrecord_subframe, text='Alter', command=alterCropRecord)
    alterrecord_button.grid(column=0, row=21, pady=5, padx=10)

    # Declare subframe for adding crop records  ------------------
    addrecord_subframe = ttk.Frame(records_tab)
    addrecord_subframe.grid(column=2, row=0)

    addrecord_Label = tk.Label(addrecord_subframe, text="Add record")
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

    addrecord_button = tk.Button(addrecord_subframe, text='Add', command=addCropRecord)
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