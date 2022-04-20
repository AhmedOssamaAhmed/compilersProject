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
        states={'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13',},
        input_symbols={'R', 'I', 'A', 'N', 'S', 'U', 'E', 'G', 'L'},
        transitions={
            'S1': {'R': {'S2'}},
            'S2': {'I': {'S3'}, 'U': {'S7'}},
            'S3': {'A': {'S4'}},
            'S4': {'I': {'S5'}, 'N': {'S6'}},
            'S5': {'S': {'S2'}},
            'S6': {'S': {'S2'}, 'N': {'S6'}},
            'S7': {'I': {'S8'}, 'N': {'S9'}},
            'S8': {"G": {'S10'}, 'L': {'S10'}, 'E': {'S11'}},
            'S9': {'G': {'S10'}, 'L': {'S10'}, 'E': {'S11'}},
            'S10': {'I': {'S12'}, 'N': {'S13'},'E': {'S11'}},
            'S11': {'I': {'S12'}, 'N': {'S13'}},
            'S12': {},
            'S13': {'N': {'S13'},'R':{'S2'}},
        },
        initial_state='S1',
        final_states={'S8', 'S9', 'S12', 'S13'}
    )
    theDFA = VisualNFA(dfac)
    theDFA.show_diagram(input_str=input, format_type="png", filename="DFA")

    image = cv2.imread('DFA.png', 1)
    cv2.imshow("DFA", image)
    cv2.waitKey()
    cv2.destroyAllWindows()

