# Import the required libraries
from tkinter import *
from tkinter import ttk

def tree(lst = [(1,'no tokens',''," "),]):
    win= Tk()
    win.title("Stack List")

    w, h = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry("%dx%d+0+0" % (w, h))

    style= ttk.Style()
    style.theme_use('clam')

    tree= ttk.Treeview(win, column=("c1", "c2","c3","c4"), show='headings',height=31, selectmode="browse")
    tree.column("#1", anchor=CENTER, stretch= NO,width=50)
    tree.heading("#1", text="S.N")
    tree.column("#2", anchor=CENTER, stretch=YES,width=300)
    tree.heading("#2", text="Stack")
    tree.column("#3", anchor=CENTER, stretch=YES,width=900)
    tree.heading("#3", text="Input")
    tree.column("#4", anchor=CENTER, stretch=NO,width=50)
    tree.heading("#4", text="Action")

    total_rows = len(lst)
    total_columns = len(lst[0])
    for i  in range(total_rows):
        tree.insert('', 'end', text= "0",values=(i,lst[i][0], lst[i][1],lst[i][2]))

    treeScroll = ttk.Scrollbar(win)
    xScroll = ttk.Scrollbar(win,orient=HORIZONTAL)
    treeScroll.configure(command=tree.yview)
    xScroll.configure(command=tree.xview)
    tree.configure(yscrollcommand=treeScroll.set,xscrollcommand=xScroll.set)
    treeScroll.pack(side= RIGHT, fill= BOTH)
    xScroll.pack(side=BOTTOM)
    tree.pack()


    win.mainloop()