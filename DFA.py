import ply.lex as lex
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from visual_automata.fa.dfa import VisualDFA
from visual_automata.fa.nfa import VisualNFA
from sympy import true
from tkinter import *
import time
# from tkinter import *
from PIL import ImageTk, Image
import cv2

def DFACheck(input):
    dfac = NFA(
        states={'Begin', 'Repeat', 'ID', 'Assign', 'Id', 'Num', 'Until', 'ID-Cond', 'Num-Cond', 'Compare', 'Equal',
                'Final-ID-Cond', 'Final-Num-Cond', },
        input_symbols={'R', 'I', 'A', 'N', 'S', 'U', 'E', 'G', 'L'},
        transitions={
            'Begin': {'R': {'Repeat'}},
            'Repeat': {'I': {'ID'}, 'U': {'Until'}},
            'ID': {'A': {'Assign'}},
            'Assign': {'I': {'Id'}, 'N': {'Num'}},
            'Id': {'S': {'Repeat'}},
            'Num': {'S': {'Repeat'}, 'N': {'Num'}},
            'Until': {'I': {'ID-Cond'}, 'N': {'Num-Cond'}},
            'ID-Cond': {"G": {'Compare'}, 'L': {'Compare'}, 'E': {'Equal'}},
            'Num-Cond': {'G': {'Compare'}, 'L': {'Compare'}, 'E': {'Equal'}},
            'Compare': {'I': {'Final-ID-Cond'}, 'N': {'Final-Num-Cond'}, 'E': {'Equal'}},
            'Equal': {'I': {'Final-ID-Cond'}, 'N': {'Final-Num-Cond'}},
            'Final-ID-Cond': {},
            'Final-Num-Cond': {'N': {'Final-Num-Cond'}},
        },
        initial_state='Begin',
        final_states={'ID-Cond', 'Num-Cond', 'Final-ID-Cond', 'Final-Num-Cond'}
    )
    theDFA = VisualNFA(dfac)
    theDFA.show_diagram(input_str=input, format_type="png", filename="DFA",)

    image = cv2.imread('DFA.png', 1)
    im = cv2.resize(image, (900, 450))
    cv2.imshow("DFA", im,)
    cv2.waitKey()
    cv2.destroyAllWindows()

