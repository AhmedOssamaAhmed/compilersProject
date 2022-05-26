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
    tree= ttk.Treeview(win, column=("c1", "c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","c12","c13"), show='headings',height=31, selectmode="browse")
    tree.column("#1", anchor=CENTER, stretch= NO,width=80)
    tree.heading("#1", text="States")
    tree.column("#2", anchor=CENTER, stretch=YES,width=80)
    tree.heading("#2", text="repeat")
    tree.column("#3", anchor=CENTER, stretch=YES,width=80)
    tree.heading("#3", text="until")
    tree.column("#4", anchor=CENTER, stretch=NO,width=80)
    tree.heading("#4", text="id")
    tree.column("#5", anchor=CENTER, stretch=NO, width=80)
    tree.heading("#5", text="assign")
    tree.column("#6", anchor=CENTER, stretch=NO, width=80)
    tree.heading("#6", text="semicolon")
    tree.column("#7", anchor=CENTER, stretch=NO, width=80)
    tree.heading("#7", text="number")
    tree.column("#8", anchor=CENTER, stretch=NO, width=80)
    tree.heading("#8", text="$")
    tree.column("#9", anchor=CENTER, stretch=NO, width=80)
    tree.heading("#9", text="STMT-SEQ")
    tree.column("#10", anchor=CENTER, stretch=NO, width=80)
    tree.heading("#10", text="STATMENT")
    tree.column("#11", anchor=CENTER, stretch=NO, width=120)
    tree.heading("#11", text="REPEAT-STATEMENT")
    tree.column("#12", anchor=CENTER, stretch=NO, width=100)
    tree.heading("#12", text="ASSIGN-STMT")
    tree.column("#13", anchor=CENTER, stretch=NO, width=80)
    tree.heading("#13", text="FACTOR")

    # Insert the data in Treeview widget

    # lst = [(1,'no tokens',''),]
    total_rows = len(lst)
    total_columns = len(lst[0])
    for i  in range(total_rows):
        tree.insert('', 'end', text= "0",values=(i,
                                                 lst[i][0],
                                                 lst[i][1],
                                                 lst[i][2],
                                                 lst[i][3],
                                                 lst[i][4],
                                                 lst[i][5],
                                                 lst[i][6],
                                                 lst[i][7],
                                                 lst[i][8],
                                                 lst[i][9],
                                                 lst[i][10],
                                                 lst[i][11],))

    print(f"the lsssst {lst}")
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

