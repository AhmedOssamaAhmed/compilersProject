from tkinter import *

# import main
# import tekonizer
# import main

# root = Tk()
# container = Frame(root)
# canvas = Canvas(container)
# scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
# scrollable_frame = Frame(canvas)


class Table:

    def __init__(self, root):

        # code for creating table
        tokens_title = Label(master=root, text="DFA hint list")
        tokens_title.grid(row=0)
        for i in range(total_rows - 1):
            for j in range(total_columns):
                self.e = Label(root, width=10,height=2, fg='blue',
                               text=lst[i][j],
                               font=('Arial', 9,),)

                self.e.grid(row=(i+1), column=j)
                print("done")


# take the data
# initially empty
lst = [('R','-->','repeat'),
       ('I','-->','Identifier'),
       ('A','-->','Assignment'),
       ('N','-->','Number'),
       ('S','-->','SemiColon'),
       ('U','-->','Until'),
       ('E','-->','Equal'),
       ('G','-->','GreaterThan'),
       ('L','-->','LessThan'),]
# print(lst)

# find total number of rows and
# columns in list
total_rows = len(lst) + 1
total_columns = len(lst[0])

# create root window
# def token_window():
# root = Tk()
# t = Table(root)
# root.mainloop()
