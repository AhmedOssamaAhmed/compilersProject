# Import the required libraries
from tkinter import *
from tkinter import ttk

def tree(lst = [(1,'no tokens',''," "),]):
    # Create an instance of tkinter frame
    win= Tk()
    win.title("Stack List")

    # Set the size of the tkinter window
    # win.geometry("1400x700")
    w, h = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry("%dx%d+0+0" % (w, h))

    # Create an instance of Style widget
    style= ttk.Style()
    style.theme_use('clam')

    # Add a Treeview widget and set the selection mode
    tree= ttk.Treeview(win, column=("c1", "c2","c3","c4"), show='headings',height=31, selectmode="browse")
    tree.column("#1", anchor=CENTER, stretch= NO,width=50)
    tree.heading("#1", text="S.N")
    tree.column("#2", anchor=CENTER, stretch=YES,width=300)
    tree.heading("#2", text="Stack")
    tree.column("#3", anchor=CENTER, stretch=YES,width=900)
    tree.heading("#3", text="Input")
    tree.column("#4", anchor=CENTER, stretch=NO,width=50)
    tree.heading("#4", text="Action")
    # Insert the data in Treeview widget

    # lst = [(1,'no tokens',''),]
    total_rows = len(lst)
    total_columns = len(lst[0])
    for i  in range(total_rows):
        tree.insert('', 'end', text= "0",values=(i,lst[i][0], lst[i][1],lst[i][2]))

    # Adding a vertical scrollbar to Treeview widget
    treeScroll = ttk.Scrollbar(win)
    xScroll = ttk.Scrollbar(win,orient=HORIZONTAL)
    treeScroll.configure(command=tree.yview)
    xScroll.configure(command=tree.xview)
    tree.configure(yscrollcommand=treeScroll.set,xscrollcommand=xScroll.set)
    treeScroll.pack(side= RIGHT, fill= BOTH)
    xScroll.pack(side=BOTTOM)
    tree.pack()


    win.mainloop()