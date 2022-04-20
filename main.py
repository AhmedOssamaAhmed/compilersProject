import tkinter as tk
import DFA
import Table_file
import tekonizer
import treeFile

def dfa_helper():
    DFA.DFACheck(tekonizer.tok(editor.get("1.0", "end-1c"))[1])

def Take_input():
    INPUT = editor.get("1.0", "end-1c")
    print(INPUT)
    tokens = tekonizer.tok(INPUT)[0]
    print(tokens)
    treeFile.tree(tokens)

window = tk.Tk()
frame = tk.Frame(
    master=window,
    relief=tk.FLAT,
)
window.title("tiny language compiler")
frame.pack()


frame.columnconfigure(2, weight=1, minsize=100)
frame.rowconfigure(3, weight=1, minsize=100)

# text editor for typing the code

editor_frame = tk.Frame(
    master=frame,
    relief=tk.GROOVE,
    borderwidth=3
)
editor_frame.grid(row=1, column=1, pady=10, padx=10)
guide_text = tk.Label(master=editor_frame, text="Enter your code here")
editor = tk.Text(master=editor_frame, )
guide_text.pack()
editor.pack()

# buttons for run & DFA & parse tree
buttons_frame = tk.Frame(
    master=frame,
    relief=tk.FLAT,
    borderwidth=3
)
buttons_frame.grid(row=2, column=1, padx=1, pady=1)
buttons_frame.rowconfigure(1, minsize=10, weight=1)
buttons_frame.columnconfigure(3, minsize=10, weight=1)

# Run button
run_frame = tk.Frame(
    master=buttons_frame,
    relief=tk.RAISED,
    borderwidth=3
)
run_frame.grid(row=0, column=0)
run_button = tk.Button(master=run_frame, text="Run", width=10, borderwidth=5, command=Take_input)
run_button.pack()

# DFA button

DFA_frame = tk.Frame(
    master=buttons_frame,
    relief=tk.RAISED,
    borderwidth=3
)
DFA_frame.grid(row=0, column=1)
DFA_button = tk.Button(master=DFA_frame, text="DFA", width=10, borderwidth=5, command=dfa_helper)
DFA_button.pack()

# parse tree

parse_frame = tk.Frame(
    master=buttons_frame,
    relief=tk.RAISED,
    borderwidth=3
)
parse_frame.grid(row=0, column=2)
parse_button = tk.Button(master=parse_frame, text="Parse tree", width=10, borderwidth=5)
parse_button.pack()

# regular expression
regular_expression_frame=tk.Frame(
    master=frame,
    relief=tk.GROOVE,
    borderwidth=3
)
regular_expression_text ="Regular Expression: (repeat)((ID)(:=)(ID|(num)+)(;))*(until)(num+|((ID)(=|<|>|<=|>=)(num+|ID)))"
regular_expression_frame.grid(row=3,column=1)
regular_expression = tk.Label(master=regular_expression_frame,text=regular_expression_text,borderwidth=5,
                              font=('Arial', 11,))
regular_expression.pack(pady=5,padx=5)

# DFA hint
DFA_hint_frame = tk.Frame(
    master=frame,
    relief=tk.GROOVE,
    borderwidth=3,
    height=100,
)
DFA_hint_frame.grid(row=1, column=2, padx=10,pady=10,sticky='N')
table = Table_file.Table(DFA_hint_frame)


window.mainloop()
