from tkinter import messagebox
import GM_db_functions as gdf

def acknowledgeConnectionError():
    quit()

def on_tab_selected(event):

    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "View Existing Records":

        messagebox.showinfo("This tab is not yet implemented...")
        gdf.load_database_results(con, )

    if tab_text == "Add New Records":

        messagebox.showinfo("This tab is not yet implemented...")

    if tab_text == "View Existing Plans":

        messagebox.showinfo("This tab is not yet implemented...")

    if tab_text == "Create New Plan":

        messagebox.showinfo("This tab is not yet implemented...")