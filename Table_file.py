from tkinter import *

class Table:

    def __init__(self, root,lst,width,text):
        total_rows = len(lst) + 1
        total_columns = len(lst[0])
        # code for creating table
        tokens_title = Label(master=root, text=text)
        tokens_title.grid(row=0)
        for i in range(total_rows - 1):
            for j in range(total_columns):
                self.e = Label(root, width=width,height=2, fg='blue',
                               text=lst[i][j],
                               font=('Arial', 8,),)

                self.e.grid(row=(i+1), column=j)
                print("done")


# take the data
# initially empty


# find total number of rows and
# columns in list


# create root window
# def token_window():
# root = Tk()
# t = Table(root)
# root.mainloop()
