__author__ = 'Nalbert Tero'
__copyright__ = "Copyright 2023"
__version__ = "1.0"
__date__ = "04/21/2023"

import tkinter as tk
from tkinter import ttk
import tkcalendar as tkc
from datetime import datetime as dt

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
                record[1], record[3], record[2], record[10], record[5], record[11], record[6], record[7], record[8], record[0]))

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
        alter_record_frame.setRecordEntryValues(parent_bed, selected_values)
    else:
        selected_values = plans_treeview.item(selected_record)
        alter_plan_frame.setPlanEntryValues(parent_bed, selected_values)

def onAddRecordPress():
    add_record_frame.tkraise()

def onAlterRecordPress():
    alter_record_frame.tkraise()

def onDeleteRecordPress():
    values = alter_record_frame.getEntryValues()

    sql = f"DELETE FROM croprecord " \
          f"WHERE CropID = {values['ID']}"

    gdf.insertIntoDatabase(con, sql)

    x = refreshTrees(Selected_Garden_Records)

def onAddPlanPress():
    add_plan_frame.tkraise()

def onAlterPlanPress():
    alter_plan_frame.tkraise()

def onDeletePlanPress():
    values = alter_plan_frame.getEntryValues()
    print(values)
    sql = f"DELETE FROM cropplan " \
          f"WHERE CropPlanID = {values['ID']}"

    gdf.insertIntoDatabase(con, sql)

    x = refreshTrees(Selected_Garden_Records)

def addCropRecord():
    values = add_record_frame.getEntryValues()

    sql = f"INSERT INTO croprecord " \
          f"(Cultivar, Year, Bed, SqFtPlanted, PlantingDate, HarvestDate, PullDate, DiseasePressure, PestPressure, Failure) VALUES" \
          f"('{values['Cultivar']}', {values['Year']}, {values['Bed']}, {values['Area']}, '{values['PlantDate']}', '{values['HarvestDate']}', " \
          f"'{values['PullDate']}', '{values['Disease']}', '{values['Pest']}', '{values['Failure']}')"

    gdf.insertIntoDatabase(con, sql)

    x = refreshTrees(Selected_Garden_Records)

def alterCropRecord():
    values = alter_record_frame.getEntryValues()

    sql = f"UPDATE croprecord " \
          f" SET Cultivar = '{values['Cultivar']}', Year = '{values['Year']}', Bed = '{values['Bed']}', SqFtPlanted = '{values['Area']}', PlantingDate = '{values['PlantDate']}', " \
          f"HarvestDate = '{values['HarvestDate']}', PullDate = '{values['PullDate']}', DiseasePressure = '{values['Disease']}', PestPressure = '{values['Pest']}', Failure = '{values['Failure']}'" \
          f"WHERE CropID = {values['ID']}"

    gdf.insertIntoDatabase(con, sql)

    x = refreshTrees(Selected_Garden_Records)

def addCropPlan():
    values = add_plan_frame.getEntryValues()

    sql = f"INSERT INTO cropplan " \
          f"(PlanID, Cultivar, Year, Bed, SqFtPlanted, TargetPlanting, TargetHarvest, TargetPull) VALUES" \
          f"('{values['CropID']}','{values['Cultivar']}', {values['Year']}, {values['Bed']}, {values['Area']}, '{values['PlantDate']}', '{values['HarvestDate']}', " \
          f"'{values['PullDate']}')"

    gdf.insertIntoDatabase(con, sql)

    x = refreshTrees(Selected_Garden_Records)

def alterCropPlan():
    values = alter_plan_frame.getEntryValues()

    sql = f"UPDATE cropplan " \
          f" SET PlanID = '{values['PlanID']}', Cultivar = '{values['Cultivar']}', Year = '{values['Year']}', Bed = '{values['Bed']}', SqFtPlanted = '{values['Area']}', " \
          f"TargetPlanting = '{values['PlantDate']}', TargetHarvest = '{values['HarvestDate']}', TargetPull = '{values['PullDate']}' " \
          f"WHERE CropPlanID = {values['ID']}"

    gdf.insertIntoDatabase(con, sql)

    x = refreshTrees(Selected_Garden_Records)

class EntryFrame(ttk.Frame):
    def __init__(self, container, name, function):
        super().__init__(container)
        self.ID = ''
        self.__create_widgets(name, function)

    def __create_widgets(self, name, function):
        frame_Label = tk.Label(self, text=f'{name}')
        frame_Label.grid(column=0, row=0, pady=(12, 6))

        PlanLabel = tk.Label(self, text='Plan:')
        self.PlanEntry = ttk.Combobox(self, state='normal', justify='right', width=10)
        PlanLabel.grid(column=0, row=1, sticky='w', padx=10)
        self.PlanEntry.grid(column=0,row=1, sticky='e', padx=10)

        frame_BedLabel = tk.Label(self, text='Bed:')
        self.frame_BedEntry = ttk.Combobox(self, state='readonly', justify='right', width=10)
        frame_BedLabel.grid(column=0, row=2, pady=(8, 2), padx=10, sticky='w')
        self.frame_BedEntry.grid(column=0, row=2, pady=0, padx=10, sticky='e')

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

        if function == addCropPlan or function == alterCropPlan:
            frame_PlantedLabel.config(text = 'Target plant date')
            frame_HarvestedLabel.config(text='Target harvest date')
            frame_PulledLabel.config(text='Target pull date')

            self.frame_PestEntry['state'] = 'disabled'
            self.frame_PestEntry.set('N/A')
            self.frame_DiseaseEntry['state'] = 'disabled'
            self.frame_DiseaseEntry.set('N/A')
            self.frame_FailureEntry['state'] = 'disabled'
            self.frame_FailureEntry.set('N/A')
        else:
            PlanLabel.grid_remove()
            self.PlanEntry.grid_remove()
            frame_button.grid(column=0, row=21, pady=(20,0), padx=10)

    def setCultivarList(self, list):
        self.frame_CultivarEntry['values'] = list
        self.frame_CultivarEntry.set(list[0])

    def setBedList(self, list):
        self.frame_BedEntry['values'] = list
        self.frame_BedEntry.set(list[0])

    def setPlanList(self, list):
        self.PlanEntry['values'] = list

    def setRecordEntryValues(self, parent_bed, selected_values):
        self.PlanEntry.set('')
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
        self.ID = selected_values['values'][10]

    def setPlanEntryValues(self, parent_bed, selected_values):
        self.PlanEntry.set('')
        self.frame_BedEntry.set('')
        self.frame_YearEntry.delete(0, 'end')
        self.frame_CultivarEntry.set('')
        self.frame_AreaEntry.delete(0, 'end')
        self.frame_PestEntry.set('')
        self.frame_DiseaseEntry.set('')
        self.frame_FailureEntry.set('')

        self.PlanEntry.set(selected_values['values'][0])
        self.frame_BedEntry.set(f'{parent_bed}')
        self.frame_YearEntry.insert(0, selected_values['values'][1])
        self.frame_CultivarEntry.set(selected_values['values'][2])
        self.frame_AreaEntry.insert(0, selected_values['values'][4])
        self.frame_PlantedEntry.set_date(dt.strptime(selected_values['values'][6], '%Y-%m-%d'))
        self.frame_HarvestedEntry.set_date(dt.strptime(selected_values['values'][7], '%Y-%m-%d'))
        self.frame_PulledEntry.set_date(dt.strptime(selected_values['values'][8], '%Y-%m-%d'))
        self.ID = selected_values['values'][9]

    def getEntryValues(self):
        values = {}
        values['PlanID'] = self.PlanEntry.get()
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
        values['ID'] = self.ID

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

    add_garden_Label = tk.Label(garden_subframe, text='Add new garden')
    add_garden_Entry = tk.Entry(garden_subframe)
    add_garden_Button = tk.Button(garden)

    # Declare subframe for crop record & plan treeview  ------------------
    records_subframe = ttk.Frame(program)
    records_subframe.grid(column=1, row=0)

    record_columns = ('Year', 'Cultivar', 'Family', 'Area', 'Planted', 'Harvested', 'Pulled', 'Pest', 'Disease', 'Failure', 'ID')

    records_treeview = ttk.Treeview(records_subframe, columns=record_columns, height=12)
    for column in record_columns[:-1]:
        records_treeview.column(column, width=75)
        records_treeview.heading(column, text=column)
    records_treeview.column('ID', width=0)
    records_treeview.bind("<<TreeviewSelect>>", onRecordSelect)
    records_treeview.grid(column=0, row=0)

    add_record_button = tk.Button(records_subframe, text='Add new record', command=onAddRecordPress)
    add_record_button.grid(column=0, row=2, sticky='w', pady=(0,6))

    alter_record_button = tk.Button(records_subframe, text='Alter selected record', command=onAlterRecordPress)
    alter_record_button.grid(column=0, row=2, pady=(0,6))

    delete_record_button = tk.Button(records_subframe, text='Delete selected record', command=onDeleteRecordPress)
    delete_record_button.grid(column=0, row=2, sticky='e', pady=(0,6))

    plan_columns = ('Plan', 'Year', 'Cultivar', 'Family', 'Area', 'Method', 'Plant', 'Harvest', 'Pull', 'ID')

    plans_treeview = ttk.Treeview(records_subframe, columns=plan_columns, height=12)
    for column in plan_columns[:-1]:
        plans_treeview.column(column, width=75)
        plans_treeview.heading(column, text=column)
    plans_treeview.column('ID', width=0)
    plans_treeview.bind("<<TreeviewSelect>>", onRecordSelect)
    plans_treeview.grid(column=0, row=3)

    add_plan_button = tk.Button(records_subframe, text='Add new plan', command=onAddPlanPress)
    add_plan_button.grid(column=0, row=4, sticky='w', pady=(0,6))

    alter_plan_button = tk.Button(records_subframe, text='Alter selected plan', command=onAlterPlanPress)
    alter_plan_button.grid(column=0, row=4, pady=(0,6))

    delete_plan_button = tk.Button(records_subframe, text='Delete selected plan', command=onDeletePlanPress)
    delete_plan_button.grid(column=0, row=4, sticky='e', pady=(0,6))

    # Declare subframes for working with crop records and plans.  ------------------
    alter_record_frame = EntryFrame(program, 'Alter  crop record', alterCropRecord)
    alter_record_frame.grid(column=2, row=0)

    alter_plan_frame = EntryFrame(program, 'Alter crop plan', alterCropPlan)
    alter_plan_frame.grid(column=2, row=0)

    add_plan_frame = EntryFrame(program, 'Add crop plan', addCropPlan)
    add_plan_frame.grid(column=2, row=0)

    add_record_frame = EntryFrame(program, 'Add crop record', addCropRecord)
    add_record_frame.grid(column=2, row=0)

    program.pack(expand=1, fill='both')
    # ======== main loop ============ #
    root.mainloop()