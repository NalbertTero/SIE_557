__author__ = 'silvianittel'

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pymysql
import db_config_file
import db_functions as db

rows = None
num_of_rows = None
row_counter =0


# === defining an event  ===============

def on_tab_selected(event):

    global blank_textboxes_tab_two

    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")
    if tab_text == "All Records":

        load_database_results()

    if tab_text == "Add New Record":
        blank_textboxes_tab_two = True


# == load database result =======

def load_database_results():
    global rows
    global num_of_rows

    try:
        con = db.open_database()
    except db.DatabaseError as e:
        messagebox.showinfo("Database connection error", e)
        exit()
    messagebox.showinfo("Connected to Database", "DB Connection OK")

    return True

# === scroll through records


#======================== MAIN APPLICATION =======================
# ==== form code ============

form = tk.Tk()
form.title("Student Database Form")
form.geometry("500x280")
tab_parent = ttk.Notebook(form)

tab1= ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)

tab_parent.bind("<<NotebookTabChanged>>", on_tab_selected)

tab_parent.add(tab1, text="All records")
tab_parent.add(tab2, text="Add new record")

##### CODE FOR TAB 1 ############################################
# ====== SET UP STRING VARS FOR TAB 1=========

fName = tk.StringVar()
fam = tk.StringVar()
id = tk.StringVar()

# === widgets for TAB ONE
firstLabelTabOne = tk.Label(tab1, text="First Name: ")
familyLabelTabOne = tk.Label(tab1, text="Last Name: ")
idLabelTabOne = tk.Label(tab1, text="Student ID: ")

firstEntryTabOne = tk.Entry(tab1, textvariable=fName)
familyEntryTabOne = tk.Entry(tab1, textvariable=fam)
idEntryTabOne = tk.Entry(tab1, textvariable=id)

buttonForward = tk.Button(tab1, text="Forward")
buttonBack = tk.Button(tab1, text="Back")


#=============== Add Widgets to GRID on TAB ONE

firstLabelTabOne.grid(row=0, column=0, padx=15, pady=15)
firstEntryTabOne.grid(row=0, column=1, padx=15, pady=15)

familyLabelTabOne.grid(row=1, column=0, padx=15, pady=15)
familyEntryTabOne.grid(row=1, column=1, padx=15, pady=15)

idLabelTabOne.grid(row=2, column=0, padx=15, pady=15)
idEntryTabOne.grid(row=2, column=1, padx=15, pady=15)

buttonBack.grid(row=3, column=0, rowspan=3, padx=15, pady=15)
buttonForward.grid(row=3, column=2, rowspan=3, padx=15, pady=15)

##### CODE FOR TAB 2 ############################################
# === WIDGETS FOR TAB TWO ========

fNameTabTwo = tk.StringVar()
famTabTwo = tk.StringVar()
gradeTabTwo = tk.StringVar()

firstLabelTabTwo = tk.Label(tab2, text="First Name: ")
familyLabelTabTwo = tk.Label(tab2, text="Last Name: ")
gradeLabelTabTwo = tk.Label(tab2, text="Grade: ")

firstEntryTabTwo = tk.Entry(tab2, textvariable=fNameTabTwo)
familyEntryTabTwo = tk.Entry(tab2, textvariable=famTabTwo)
gradeEntryTabTwo = tk.Entry(tab2, textvariable=gradeTabTwo)
buttonCommit = tk.Button(tab2, text="Add Record to Database")

# === LAYOUT OF WIDGETS TO GRID ON TAB TWO
firstLabelTabTwo.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
firstEntryTabTwo.grid(row=0, column=1, padx=10, pady=10)

familyLabelTabTwo.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
familyEntryTabTwo.grid(row=1, column=1, padx=10, pady=10)

gradeLabelTabTwo.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
gradeEntryTabTwo.grid(row=2, column=1, padx=10, pady=10)

buttonCommit.grid(row=4, column=1, padx=15, pady=15, sticky=tk.W)


#================ main code


tab_parent.pack(expand=1, fill='both')
form.mainloop()