import tkinter as tk
import DFA
import Table_file
import stack_tree
import main_parser
import tekonizer
import treeFile

main_parser.helper()


def dfa_helper():
    DFA.DFACheck(tekonizer.tok(editor.get("1.0", "end-1c"))[1])


def tokens_map(list_tokens):
    string_token = ""
    for i in range(len(list_tokens)):
        string_token += list_tokens[i][1]
        string_token += " "
    return string_token


def Take_input():
    INPUT = editor.get("1.0", "end-1c")
    tokens = tekonizer.tok(INPUT)[0]
    treeFile.tree(tokens)

accepted = False
def handler(e):
    global accepted
    INPUT = editor.get("1.0", "end-1c")
    tokens = tekonizer.tok(INPUT)[0]
    string_tokens = tokens_map(tokens)
    act = main_parser.process_input(string_tokens)[4]
    if act[-1]:
        accepted = True
        status.delete('1.0', tk.END)
        status.insert(tk.END, "ACCEPTED")
        status.configure(bg='green')
    elif act[-1] != "accepted":
        accepted = False
        status.delete('1.0', tk.END)
        status.insert(tk.END, "REJECTED")
        status.configure(bg='red')


window = tk.Tk()
frame = tk.Frame(
    master=window,
    relief=tk.FLAT,
)
window.title("tiny language compiler")
frame.pack()

frame.columnconfigure(6, weight=1, minsize=100)
frame.rowconfigure(3, weight=1, minsize=100)

# text editor for typing the code
editor_frame = tk.Frame(
    master=frame,
    relief=tk.GROOVE,
    borderwidth=3
)

editor_frame.grid(row=1, column=1, pady=10, padx=0)
guide_text = tk.Label(master=editor_frame, text="Enter your code here")
editor = tk.Text(master=editor_frame)
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
run_button = tk.Button(master=run_frame, text="Tokens", width=10, borderwidth=5, command=Take_input)
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


# parse table

def parse_table_helper():
    main_parser.view_parsing()


parse_table_frame = tk.Frame(
    master=buttons_frame,
    relief=tk.RAISED,
    borderwidth=3
)
parse_table_frame.grid(row=0, column=2)
parse_table_button = tk.Button(master=parse_table_frame, text="Parse table", width=10, borderwidth=5,
                               command=parse_table_helper)
parse_table_button.pack()


# parse tree

def parse_tree_helper():
    if accepted:
        INPUT = editor.get("1.0", "end-1c")
        tokens = tekonizer.tok(INPUT)[0]
        string_tokens = tokens_map(tokens)
        stack = main_parser.process_input(string_tokens)[2]
        main_parser.parse_tree_generator(stack)
    else:
        root = tk.Tk()
        root.geometry("500x70")
        error = tk.Label(master=root, text="   please enter valid syntax  ", font=('Arial', 20,),
                         fg="red", bg="black")
        error.pack()
        root.title("Warning!!")
        root.mainloop()


parse_tree_frame = tk.Frame(
    master=buttons_frame,
    relief=tk.RAISED,
    borderwidth=3
)
parse_tree_frame.grid(row=0, column=3)
parse_tree_button = tk.Button(master=parse_tree_frame, text="Parse tree", width=10, borderwidth=5,
                              command=parse_tree_helper)
parse_tree_button.pack()


# SLR Diagram
def slr_helper():
    main_parser.view_lr()


SLR_frame = tk.Frame(
    master=buttons_frame,
    relief=tk.RAISED,
    borderwidth=3
)
SLR_frame.grid(row=0, column=4)
SLR_button = tk.Button(master=SLR_frame, text="SLR Diagram", width=10, borderwidth=5, command=slr_helper)
SLR_button.pack()


# Stack

def stack_helper():
    INPUT = editor.get("1.0", "end-1c")
    tokens = tekonizer.tok(INPUT)[0]
    string_tokens = tokens_map(tokens)
    row, ste, sta, inp, act = main_parser.process_input(string_tokens)
    stack_list = []
    for i in range(len(sta)):
        stack_list.append([sta[i], inp[i], act[i]])
    stack_tree.tree(stack_list)



stack_input = tk.Frame(
    master=buttons_frame,
    relief=tk.RAISED,
    borderwidth=3
)
stack_input.grid(row=0, column=5)
stack_button = tk.Button(master=stack_input, text="Stack", width=10, borderwidth=5, command=stack_helper)
stack_button.pack()

# status
status_frame = tk.Frame(
    master=buttons_frame,
    relief=tk.RAISED,
    borderwidth=3
)
status_frame.grid(row=0, column=6)
status = tk.Text(status_frame, width=8, height=1, bg="light blue", fg="navy")
status.insert(tk.END, "status")
status.pack(padx=5)

window.bind('<Any-KeyPress>', handler)
# regular expression
regular_expression_frame = tk.Frame(
    master=frame,
    relief=tk.GROOVE,
    borderwidth=3
)
regular_expression_text = "Regular Expression: (repeat)((ID)(:=)(ID|(num)+)(;))*(until)(num+|((ID)(=|<|>|<=|>=)(num+|ID)))"
regular_expression_frame.grid(row=3, column=1)
regular_expression = tk.Label(master=regular_expression_frame, text=regular_expression_text, borderwidth=5,
                              font=('Arial', 11,))
regular_expression.pack(pady=5, padx=5)

# DFA hint
DFA_hint_frame = tk.Frame(
    master=frame,
    relief=tk.GROOVE,
    borderwidth=3,
    height=100,
)
DFA_hint_frame.grid(row=1, column=2, padx=0, pady=10, sticky='N')
DFA_hint_lst = [('R', '-->', 'repeat'),
                ('I', '-->', 'Identifier'),
                ('A', '-->', 'Assignment'),
                ('N', '-->', 'Number'),
                ('S', '-->', 'SemiColon'),
                ('U', '-->', 'Until'),
                ('E', '-->', 'Equal'),
                ('G', '-->', 'GreaterThan'),
                ('L', '-->', 'LessThan'),
                ('P', '-->', 'PROHIBITED')]

DFA_table = Table_file.Table(DFA_hint_frame, DFA_hint_lst, 10, "DFA hint list")

# our grammar
grammar_frame = tk.Frame(
    master=frame,
    relief=tk.GROOVE,
    borderwidth=3,
    height=100,
)
grammar_frame.grid(row=1, column=3, padx=0, pady=10, sticky='N')
grammar_lst = [('STMT-SEQ', '-->', 'STMT-SEQ STATEMENT | STATEMENT'),
               ('STATEMENT', '-->', 'REPEAT-STMT | ASSIGN-STMT'),
               ('REPEAT-STMT', '-->', 'repeat STMT-SEQ until id'),
               ('ASSIGN-STMT', '-->', 'id assign FACTOR semicolon'),
               ('FACTOR', '-->', 'id | number'),
               ]
grammar_table = Table_file.Table(grammar_frame, grammar_lst, 23, "Grammar")

#
# # stack
# view_stack_frame = tk.Frame(
#     master=frame,
#     relief=tk.GROOVE,
#     borderwidth=3,
#     height=100,
# )
# view_stack_frame.grid(row=2,column=3)
# adjusted_tree.tree(view_stack_frame,DFA_hint_lst)


window.mainloop()
