# Import the required libraries
from tkinter import *
from tkinter import ttk

def tree(lst = [(1,'no tokens',''),]):
    # Create an instance of tkinter frame
    win= Tk()
    win.title("list of tokens")

    # Set the size of the tkinter window
    win.geometry("700x350")

    # Create an instance of Style widget
    style= ttk.Style()
    style.theme_use('clam')

    # Add a Treeview widget and set the selection mode
    tree= ttk.Treeview(win, column=("c1", "c2","c3"), show='headings', height= 16, selectmode="browse")
    tree.column("#1", anchor=CENTER, stretch= NO)
    tree.heading("#1", text="Number")
    tree.column("#2", anchor=CENTER, stretch=NO)
    tree.heading("#2", text="Token Type")
    tree.column("#3", anchor=CENTER, stretch=NO)
    tree.heading("#3", text="Token value")
    # Insert the data in Treeview widget

    # lst = [(1,'no tokens',''),]
    total_rows = len(lst)
    total_columns = len(lst[0])
    for i  in range(total_rows):
        tree.insert('', 'end', text= "0",values=(lst[i][0], lst[i][1],lst[i][2]))

    # Adding a vertical scrollbar to Treeview widget
    treeScroll = ttk.Scrollbar(win)
    treeScroll.configure(command=tree.yview)
    tree.configure(yscrollcommand=treeScroll.set)
    treeScroll.pack(side= RIGHT, fill= BOTH)
    tree.pack()

    win.mainloop()