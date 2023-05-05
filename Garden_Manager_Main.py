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
def loadGardens():
    existing_gardens_listbox.delete(0,'end')
    num_rows, rows = gdf.load_database_results(con, "SELECT * FROM gardens")
    for index, row in enumerate(rows):
        existing_gardens_listbox.insert(index, row[1])

    cultivar_list = ['Choose cultivar']
    num_cults, cults = gdf.load_database_results(con, "SELECT cultivar.CultivarName FROM cultivar")
    for c in cults:
        cultivar_list.append(c[0])

    alter_record_frame.setCultivarList(cultivar_list)
    add_record_frame.setCultivarList(cultivar_list)
    alter_plan_frame.setCultivarList(cultivar_list)
    add_plan_frame.setCultivarList(cultivar_list)

def refreshTrees(selected_garden):
    if selected_garden is not None:
        for item in records_treeview.get_children():
            records_treeview.delete(item)
        for item in plans_treeview.get_children():
            plans_treeview.delete(item)

    bed_list = ['Choose planting bed']
    num_rows, rows = gdf.load_database_results(con, f"SELECT * FROM plantingbeds WHERE plantingbeds.InGarden = '{selected_garden}';")
    for row in rows:
        records_treeview.insert('', 'end', row[0], text=f'Bed {row[0]} - {row[1]} sq. ft.')
        num_records, records = gdf.load_database_results(con, f"SELECT * FROM croprecord LEFT JOIN cultivar ON croprecord.cultivar = cultivar.CultivarName WHERE croprecord.Bed = '{row[0]}'")
        for record in records:
            records_treeview.insert(row[0], 'end', iid=None, text='', values=(record[2], record[1], record[12], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[0]))
        bed_list.append(row[0])

    num_rows, rows = gdf.load_database_results(con,
                                               f"SELECT * FROM plantingbeds WHERE plantingbeds.InGarden = '{selected_garden}';")
    for row in rows:
        plans_treeview.insert('', 'end', row[0], text=f'Bed {row[0]} - {row[1]} sq. ft.')
        num_records, records = gdf.load_database_results(con, f"SELECT * FROM cropplan LEFT JOIN cultivar ON cropplan.cultivar = cultivar.CultivarName WHERE cropplan.Bed = '{row[0]}'")
        for record in records:
            plans_treeview.insert(row[0], 'end', iid=None, text='', values=(
            record[2], record[1], record[12], record[4], record[5], record[6], record[7], record[8], record[9],
            record[0]))

    return bed_list

def onGardenSelect(event):
    global Selected_Garden_Records
    list = event.widget
    selection = event.widget.curselection()
    selected_garden = list.get(selection)

    Selected_Garden_Records = selected_garden

    bed_list = refreshTrees(selected_garden)

    alter_record_frame.setBedList(bed_list)
    add_record_frame.setBedList(bed_list)
    alter_plan_frame.setBedList(bed_list)
    add_plan_frame.setBedList(bed_list)

def onRecordSelect(event):
    records = event.widget
    selected_record = records.focus()
    parent_bed = records.parent(selected_record)

    if records == records_treeview:
        selected_values = records_treeview.item(selected_record)
        alter_record_frame.setEntryValues(parent_bed, selected_values)
    else:
        selected_values = plans_treeview.item(selected_record)
        alter_plan_frame.setEntryValues(parent_bed, selected_values)

def onAddRecordPress():
    add_record_frame.tkraise()

def onAlterRecordPress():
    alter_record_frame.tkraise()

#def onDeleteRecordPress():

def onAddPlanPress():
    add_record_frame.tkraise()

def onAlterPlanPress():
    alter_record_frame.tkraise()

#def onDeletePlanPress():

def addCropRecord():

    values = add_record_frame.getEntryValues()

    sql = f"INSERT INTO croprecord " \
          f"(Cultivar, Year, Bed, SqFtPlanted, PlantingDate, HarvestDate, PullDate, DiseasePressure, PestPressure, Failure) VALUES" \
          f"('{values['Cultivar']}', {values['Year']}, {values['Bed']}, {values['Area']}, '{values['PlantDate']}', '{values['HarvestDate']}', " \
          f"'{values['PullDate']}', '{values['Disease']}', '{values['Pest']}', '{values['Failure']}')"

    gdf.insertIntoDatabase(con, sql)

    selection = existing_gardens_listbox.curselection()
    existi
    x = refreshTrees

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

def addCropPlan():
    pass

def alterCropPlan():
    pass

class EntryFrame(ttk.Frame):
    def __init__(self, container, name, function):
        super().__init__(container)

        self.__create_widgets(name, function)

    def __create_widgets(self, name, function):
        frame_Label = tk.Label(self, text=f'{name}')
        frame_Label.grid(column=0, row=0, pady=10)

        frame_BedLabel = tk.Label(self, text='Bed')
        self.frame_BedEntry = ttk.Combobox(self, state='readonly')
        frame_BedLabel.grid(column=0, row=1, pady=(6, 2), padx=10, sticky='w')
        self.frame_BedEntry.grid(column=0, row=2, pady=0, padx=10)

        frame_YearLabel = tk.Label(self, text='Year')
        self.frame_YearEntry = tk.Entry(self)
        frame_YearLabel.grid(column=0, row=3, pady=(6, 2), padx=10, sticky='w')
        self.frame_YearEntry.grid(column=0, row=4, pady=0, padx=10)

        frame_CultivarLabel = tk.Label(self, text='Cultivar')
        self.frame_CultivarEntry = ttk.Combobox(self, state='readonly')
        frame_CultivarLabel.grid(column=0, row=5, pady=(6, 2), padx=10, sticky='w')
        self.frame_CultivarEntry.grid(column=0, row=6, pady=0, padx=10)

        frame_AreaLabel = tk.Label(self, text='Area')
        self.frame_AreaEntry = tk.Entry(self)
        frame_AreaLabel.grid(column=0, row=7, pady=(6, 2), padx=10, sticky='w')
        self.frame_AreaEntry.grid(column=0, row=8, pady=0, padx=10)

        frame_PlantedLabel = tk.Label(self, text='Date Planted')
        self.frame_PlantedEntry = tkc.DateEntry(self)
        frame_PlantedLabel.grid(column=0, row=9, pady=(6, 2), padx=10, sticky='w')
        self.frame_PlantedEntry.grid(column=0, row=10, pady=0, padx=10, sticky='w')

        frame_HarvestedLabel = tk.Label(self, text='Date Harvested')
        self.frame_HarvestedEntry = tkc.DateEntry(self)
        frame_HarvestedLabel.grid(column=0, row=11, pady=(6, 2), padx=10, sticky='w')
        self.frame_HarvestedEntry.grid(column=0, row=12, pady=0, padx=10, sticky='w')

        frame_PulledLabel = tk.Label(self, text='Date Pulled')
        self.frame_PulledEntry = tkc.DateEntry(self)
        frame_PulledLabel.grid(column=0, row=13, pady=(6, 2), padx=10, sticky='w')
        self.frame_PulledEntry.grid(column=0, row=14, pady=0, padx=10, sticky='w')

        frame_PestLabel = tk.Label(self, text='Pest')
        self.frame_PestEntry = ttk.Combobox(self, state='readonly',
                                             values=['None', 'Low', 'Medium', 'High'])
        self.frame_PestEntry.set('None')
        frame_PestLabel.grid(column=0, row=15, pady=(6, 2), padx=10, sticky='w')
        self.frame_PestEntry.grid(column=0, row=16, pady=0, padx=10)

        frame_DiseaseLabel = tk.Label(self, text='Disease')
        self.frame_DiseaseEntry = ttk.Combobox(self, state='readonly',
                                                values=['None', 'Low', 'Medium', 'High'])
        self.frame_DiseaseEntry.set('None')
        frame_DiseaseLabel.grid(column=0, row=17, pady=(6, 2), padx=10, sticky='w')
        self.frame_DiseaseEntry.grid(column=0, row=18, pady=0, padx=10)

        frame_FailureLabel = tk.Label(self, text='Failed?')
        self.frame_FailureEntry = ttk.Combobox(self, state='readonly', values=['Yes', 'No'])
        self.frame_FailureEntry.set('No')
        frame_FailureLabel.grid(column=0, row=19, pady=(6, 2), padx=10, sticky='w')
        self.frame_FailureEntry.grid(column=0, row=20, pady=0, padx=10)

        frame_button = tk.Button(self, text=f'{name}', command=function)
        frame_button.grid(column=0, row=21, pady=5, padx=10)

    def setCultivarList(self, list):
        self.frame_CultivarEntry['values'] = list
        self.frame_CultivarEntry.set(list[0])

    def setBedList(self, list):
        self.frame_BedEntry['values'] = list
        self.frame_BedEntry.set(list[0])

    def setEntryValues(self, parent_bed, selected_values):
        self.frame_BedEntry.set('')
        self.frame_YearEntry.delete(0, 'end')
        self.frame_CultivarEntry.set('')
        self.frame_AreaEntry.delete(0, 'end')
        self.frame_PestEntry.set('')
        self.frame_DiseaseEntry.set('')
        self.frame_FailureEntry.set('')

        self.frame_BedEntry.set(f'{parent_bed}')
        self.frame_YearEntry.insert(0, selected_values['values'][0])
        self.frame_CultivarEntry.set(selected_values['values'][1])
        self.frame_AreaEntry.insert(0, selected_values['values'][3])
        self.frame_PlantedEntry.set_date(dt.strptime(selected_values['values'][4], '%Y-%m-%d'))
        self.frame_HarvestedEntry.set_date(dt.strptime(selected_values['values'][5], '%Y-%m-%d'))
        self.frame_PulledEntry.set_date(dt.strptime(selected_values['values'][6], '%Y-%m-%d'))
        self.frame_PestEntry.set(selected_values['values'][7])
        self.frame_DiseaseEntry.set(selected_values['values'][8])
        self.frame_FailureEntry.set(selected_values['values'][9])

    def getEntryValues(self):
        values = {}
        values['Bed'] = self.frame_BedEntry.get()
        values['Year'] = self.frame_YearEntry.get()
        values['Cultivar'] = self.frame_CultivarEntry.get()
        values['Area'] = self.frame_AreaEntry.get()
        values['PlantDate'] = self.frame_PlantedEntry.get_date()
        values['HarvestDate'] = self.frame_HarvestedEntry.get_date()
        values['PullDate'] = self.frame_PulledEntry.get_date()
        values['Pest'] = self.frame_PestEntry.get()
        values['Disease'] = self.frame_DiseaseEntry.get()
        values['Failure'] = self.frame_FailureEntry.get()

        return values


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

    # Create the root program.
    # --------------------------------------------------
    root = tk.Tk()
    root.title('Garden Manager 1.0')
    root.geometry('1250x640')
    s = ttk.Style(root)
    s.theme_use('clam')

    # Declare main frame.
    # --------------------------------------------------
    program = ttk.Frame(root)

    # Declare subframe for garden list ------------------
    garden_subframe = ttk.Frame(program, borderwidth=2)
    garden_subframe.grid(column=0, row=0)

    gardens_load_button = tk.Button(garden_subframe, text='Load Gardens', command=loadGardens)
    gardens_load_button.grid(column=0, row=0, sticky='n')

    existing_gardens_list_label = tk.Label(garden_subframe, text='Choose Garden', pady=5)
    existing_gardens_list_label.grid(column=0, row=1)

    existing_gardens_scrollbar = tk.Scrollbar(garden_subframe, orient="vertical")

    existing_gardens_listbox = tk.Listbox(garden_subframe, yscrollcommand=existing_gardens_scrollbar.set)
    existing_gardens_listbox.grid(column=0, row=2, padx=(0,4))
    existing_gardens_listbox.bind("<<ListboxSelect>>", onGardenSelect)

    existing_gardens_scrollbar.config(command=existing_gardens_listbox.yview)
    existing_gardens_scrollbar.grid(column=0, row=2)

    # Declare subframe for crop record & plan treeview  ------------------
    records_subframe = ttk.Frame(program)
    records_subframe.grid(column=1, row=0)

    tree_columns = ('Year', 'Cultivar', 'Family', 'Area', 'Planted', 'Harvested', 'Pulled', 'Pest', 'Disease', 'Failure', 'ID')

    records_treeview = ttk.Treeview(records_subframe, columns=tree_columns, height=12)
    for column in tree_columns[:-1]:
        records_treeview.column(column, width=75)
        records_treeview.heading(column, text=column)
    records_treeview.column('ID', width=0)
    records_treeview.bind("<<TreeviewSelect>>", onRecordSelect)
    records_treeview.grid(column=0, row=0)

    add_record_button = tk.Button(records_subframe, text='Add new record', command=onAddRecordPress)
    add_record_button.grid(column=0, row=2, sticky='w', pady=(0,6))

    alter_record_button = tk.Button(records_subframe, text='Alter selected record', command=onAlterRecordPress)
    alter_record_button.grid(column=0, row=2, pady=(0,6))

    delete_record_button = tk.Button(records_subframe, text='Delete selected record')
    delete_record_button.grid(column=0, row=2, sticky='e', pady=(0,6))

    plans_treeview = ttk.Treeview(records_subframe, columns=tree_columns, height=12)
    for column in tree_columns[:-1]:
        plans_treeview.column(column, width=75)
        plans_treeview.heading(column, text=column)
    plans_treeview.column('ID', width=0)
    plans_treeview.bind("<<TreeviewSelect>>", onRecordSelect)
    plans_treeview.grid(column=0, row=3)

    add_plan_button = tk.Button(records_subframe, text='Add new plan', command=onAddPlanPress)
    add_plan_button.grid(column=0, row=4, sticky='w', pady=(0,6))

    alter_plan_button = tk.Button(records_subframe, text='Alter selected plan', command=onAlterPlanPress)
    alter_plan_button.grid(column=0, row=4, pady=(0,6))

    delete_plan_button = tk.Button(records_subframe, text='Delete selected plan')
    delete_plan_button.grid(column=0, row=4, sticky='e', pady=(0,6))

    # Declare subframe for altering crop records  ------------------

    alterrecord_subframe = ttk.Frame(program)
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
    addrecord_subframe = ttk.Frame(program)
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

    alter_record_frame = EntryFrame(program, 'Alter record', alterCropRecord)
    alter_record_frame.grid(column=2, row=0)

    add_record_frame = EntryFrame(program, 'Add record', addCropRecord)
    add_record_frame.grid(column=2, row=0)

    alter_plan_frame = EntryFrame(program, 'Alter plan', alterCropPlan)
    alter_plan_frame.grid(column=2, row=0)

    add_plan_frame = EntryFrame(program, 'Add plan', addCropPlan)
    add_plan_frame.grid(column=2, row=0)

    program.pack(expand=1, fill='both')
    # ======== main loop ============ #
    root.mainloop()