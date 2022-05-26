from tkinter import *
# from tkinter import Tk
# import tkinter as tk
# import random
# import time
# import os
from tkinter import Canvas, Label, Frame, Button, Tk, Entry, Toplevel

import matplotlib.pyplot as plt
import networkx as nx
from graphviz import Digraph
from networkx.drawing.nx_pydot import graphviz_layout

import Parse_table

grammars = open("grammer.txt")
G = {}
C = {}
I = {}
J = {}

inputstring = ""

start = ""
terminals = []
nonterminals = []
symbols = []
error = 0
relation = []
r1 = []


def parse_grammar():
    global G, start, terminals, nonterminals, symbols
    for line in grammars:  # read productions from grammar.txt
        line = " ".join(line.split())
        if line == '\n':
            break
        head = line[:line.index("->")].strip()  # symbols to left of arrow
        prods = [l.strip().split(' ') for l in
                 ''.join(line[line.index("->") + 2:]).split('|')]  # symbols to right of arrow
        if not start:
            start = head + "'"  # augmenting the grammar i.e S'->S
            G[start] = [[head]]
            nonterminals.append(start)
        if head not in G:
            G[head] = []
        if head not in nonterminals:  # add left symbols to non terminals
            nonterminals.append(head)
        for prod in prods:
            G[head].append(prod)  # associate rules to correspoding non terminals
            for char in prod:
                if not char.isupper() and char not in terminals:  # check terminal or non terminal and add
                    terminals.append(char)
                elif char.isupper() and char not in nonterminals:
                    nonterminals.append(char)
                    G[char] = []  # non terminals dont produce other symbols

    symbols = terminals + nonterminals
    print(f"defined terminal {terminals}")


first_seen = []


def FIRST(X):
    global first_seen
    first = []
    first_seen.append(X)
    if X in terminals:  # CASE 1
        first.append(X)
    elif X in nonterminals:
        for prods in G[X]:  # CASE 2
            if prods[0] in terminals and prods[0] not in first:
                first.append(prods[0])
            else:  # CASE 3
                for nonterm in prods:
                    if nonterm not in first_seen:
                        for terms in FIRST(nonterm):
                            if terms not in first:
                                first.append(terms)
    first_seen.remove(X)
    return first


follow_seen = []


def FOLLOW(A):
    global follow_seen
    follow = []
    follow_seen.append(A)
    if A == start:  # CASE 1
        follow.append('$')
    for heads in G.keys():
        for prods in G[heads]:
            follow_head = False
            if A in prods:
                next_symbol_pos = prods.index(A) + 1
                if next_symbol_pos < len(prods):  # CASE 2
                    for terms in FIRST(prods[next_symbol_pos]):
                        if terms not in follow:
                            follow.append(terms)
                else:  # CASE 3
                    follow_head = True
                if follow_head and heads not in follow_seen:
                    for terms in FOLLOW(heads):
                        if terms not in follow:
                            follow.append(terms)
    follow_seen.remove(A)
    return follow


def closure(I):
    J = I
    while True:
        item_len = len(J) + sum(len(v) for v in J.values())
        for heads in list(J.keys()):
            for prods in J[heads]:
                dot_pos = prods.index('.')
                if dot_pos + 1 < len(prods):  # checks if final item or not
                    prod_after_dot = prods[dot_pos + 1]
                    if prod_after_dot in nonterminals:  # check symbol after dot terminal or not
                        for prod in G[prod_after_dot]:
                            item = ["."] + prod  # add dot to rules of new non terminal (i.e finding closure)
                            if prod_after_dot not in J.keys():
                                J[prod_after_dot] = [item]
                            elif item not in J[prod_after_dot]:
                                J[prod_after_dot].append(item)  # if more rules then append
        if item_len == len(J) + sum(len(v) for v in J.values()):  # check any more closure possible
            return J


def GOTO(I, X):
    goto = {}
    for heads in I.keys():  # for all left symbols of I
        for prods in I[heads]:  # for all productions of above sumbols
            for i in range(len(prods) - 1):
                if "." == prods[i] and X == prods[i + 1]:  # if .S
                    temp_prods = prods[:]
                    temp_prods[i], temp_prods[i + 1] = temp_prods[i + 1], temp_prods[
                        i]  # swap dot and symbol after dot i.e. shift
                    prod_closure = closure({heads: [temp_prods]})  # again calculate closure
                    for keys in prod_closure:
                        if keys not in goto.keys():
                            goto[keys] = prod_closure[keys]
                        elif prod_closure[keys] not in goto[keys]:
                            for prod in prod_closure[keys]:
                                goto[keys].append(prod)
    return goto  # return new state


def items():
    # form all LR(0) items
    global C
    i = 1
    C = {'I0': closure({start: [['.'] + G[start][0]]})}  # represents all LR items
    while True:
        item_len = len(C) + sum(len(v) for v in C.values())
        for I in list(C.keys()):
            for X in symbols:
                if GOTO(C[I], X) and GOTO(C[I], X) not in C.values():
                    C['I' + str(i)] = GOTO(C[I], X)  # store constructed items
                    i += 1
        if item_len == len(C) + sum(len(v) for v in C.values()):  # check any more items possible
            return


def ACTION(i, a):
    global error
    for heads in C['I' + str(i)]:
        for prods in C['I' + str(i)][heads]:
            for j in range(len(prods) - 1):
                if prods[j] == '.' and prods[j + 1] == a:
                    for k in range(len(C)):
                        if GOTO(C['I' + str(i)], a) == C['I' + str(k)]:
                            if a in terminals:
                                if "r" in parse_table[i][terminals.index(a)]:
                                    if error != 1:
                                        print("ERROR: Shift-Reduce Conflict at State " + str(i) + ", Symbol \'" + str(
                                            terminals.index(a)) + "\'")
                                    error = 1
                                    if "s" + str(k) not in parse_table[i][terminals.index(a)]:
                                        parse_table[i][terminals.index(a)] = parse_table[i][
                                                                                 terminals.index(a)] + "/s" + str(k)
                                    return parse_table[i][terminals.index(a)]
                                else:
                                    parse_table[i][terminals.index(a)] = "s" + str(k)  # assign Ii,a=sk  eg I2,= => I6
                            else:
                                parse_table[i][len(terminals) + nonterminals.index(a)] = str(k)
                            return "s" + str(k)
    for heads in C['I' + str(i)]:
        if heads != start:
            for prods in C['I' + str(i)][heads]:
                if prods[-1] == '.':  # final item
                    k = 0
                    for head in G.keys():
                        for Gprods in G[head]:
                            if head == heads and (Gprods == prods[:-1]) and (a in terminals or a == '$'):
                                for terms in FOLLOW(heads):
                                    if terms == '$':
                                        index = len(terminals)
                                    else:
                                        index = terminals.index(terms)
                                    if "s" in parse_table[i][index]:
                                        if error != 1:
                                            print("ERROR: Shift-Reduce Conflict at State " + str(
                                                i) + ", Symbol \'" + str(terms) + "\'")
                                        error = 1
                                        if "r" + str(k) not in parse_table[i][index]:
                                            parse_table[i][index] = parse_table[i][index] + "/r" + str(k)
                                        return parse_table[i][index]
                                    elif parse_table[i][index] and parse_table[i][index] != "r" + str(k):
                                        if error != 1:
                                            print("ERROR: Reduce-Reduce Conflict at State " + str(
                                                i) + ", Symbol \'" + str(terms) + "\'")
                                        error = 1
                                        if "r" + str(k) not in parse_table[i][index]:
                                            parse_table[i][index] = parse_table[i][index] + "/r" + str(k)
                                        return parse_table[i][index]
                                    else:
                                        parse_table[i][index] = "r" + str(k)
                                return "r" + str(k)
                            k += 1
    if start in C['I' + str(i)] and G[start][0] + ['.'] in C['I' + str(i)][start]:
        parse_table[i][len(terminals)] = "acc"
        return "acc"
    return ""

#
# def print_info():
#     print("GRAMMAR:")
#     for head in G.keys():
#         if head == start:
#             continue
#         print("{:>{width}} ->".format(head, width=len(max(G.keys(), key=len)))),
#         num_prods = 0
#         for prods in G[head]:
#             if num_prods > 0:
#                 print("|"),
#             for prod in prods:
#                 print(prod),
#             num_prods += 1
#         print()
#     print("\nAUGMENTED GRAMMAR:")
#     i = 0
#     for head in G.keys():
#         for prods in G[head]:
#             for prod in prods:
#                 print(prod),
#             print()
#             i += 1
#     for head in G:
#         num_terms = 0
#         for terms in FIRST(head):
#             if num_terms > 0:
#                 print(", "),
#             print(terms),
#             num_terms += 1
#
#     for head in G:
#         num_terms = 0
#         for terms in FOLLOW(head):
#             if num_terms > 0:
#                 print(", "),
#             print(terms),
#             num_terms += 1
#         print("}")
#
#     print("\nITEMS:")
#     for i in range(len(C)):
#         print('I' + str(i) + ':')
#         for keys in C['I' + str(i)]:
#             for prods in C['I' + str(i)][keys]:
#                 print("{:>{width}} ->".format(keys, width=len(max(G.keys(), key=len)))),
#                 for prod in prods:
#                     print(prod),
#                 print()
#         print()
#
#     for i in range(len(parse_table)):  # len gives number of states
#         for j in symbols:
#             ACTION(i, j)
#
#
#     for terms in terminals:
#         print("{:^7}|".format(terms)),
#     print("{:^7}|".format("$")),
#     for nonterms in nonterminals:
#         if nonterms == start:
#             continue
#         print("{:^7}|".format(nonterms)),
#     print("\n+" + "--------+" * (len(terminals) + len(nonterminals) + 1))
#     for i in range(len(parse_table)):
#         print("|{:^8}|".format(i)),
#         for j in range(len(parse_table[i]) - 1):
#             print("{:^7}|".format(parse_table[i][j])),
#         print()
#     print("+" + "--------+" * (len(terminals) + len(nonterminals) + 1))


def construct_dfa():
    Z = []
    pd = []
    print("\nITEMS:")
    for i in range(len(C)):
        I[i] = 'I' + str(i)
        Z = ""
        for keys in C['I' + str(i)]:
            Y = ""
            for prods in C['I' + str(i)][keys]:
                # print(G)
                zzz = "{:>{width}} ->".format(keys, width=len(max(G.keys(), key=len)))
                pd = ""

                Z = Z + zzz
                for prod in prods:
                    pd = pd + prod
                Z = Z + pd + "\r\n"
                print()
            Y = Y + Z
        print()
        J[i] = Y
    for i in range(len(parse_table)):
        for j in symbols:
            ACTION(i, j)
    global dot

    dot = Digraph(node_attr={'shape':'box','height':'3'})

    for i in range(len(C)):
        for a in symbols:
            rel = parse_table[i][symbols.index(a)]

            if rel:
                # print rel
                if (len(rel) == 1):
                    r = int(rel)
                else:
                    if (rel == 'acc') or (rel[0] == 'r'):
                        continue
                    elif '/' in rel:
                        spos = rel.index('s')
                        rel = rel[spos:spos + 2]
                        r = int(rel[1:3])
                    elif 's' in rel:
                        # print rel
                        r = int(rel[1:3])
                    else:
                        r = int(rel)

                relation.append(chr(i + 97) + chr(r + 97))
                r1.append(a)


    M = [v for v in I.values()]
    N = [v for v in J.values()]

    for i in range(len(C)):
        dot.node(chr(97 + i), N[i], xlabel=M[i])

    for i in range(len(relation)):
        dot.edge(relation[i][0], relation[i][1], label=r1[i])
    # nx.draw(dot)
    # plt.show()


def process_input(inputX):
    ste = []
    sta = []
    inp = []
    act = []
    get_input = inputX
    to_parse = " ".join((get_input + " $").split()).split(" ")
    pointer = 0
    stack = ['0']


    step = 1
    while True:
        curr_symbol = to_parse[pointer]
        top_stack = int(stack[-1])
        stack_content = ""
        input_content = ""

        for i in stack:
            stack_content += i
            stack_content += " "
        stck = "{:27}|".format(stack_content)
        stckx = "{:27}".format(stack_content)

        sta.append(stckx)
        i = pointer
        while i < len(to_parse):
            input_content += to_parse[i]
            i += 1
            input_content += " "
        inpt = "{:>26} | ".format(input_content)
        inptx = "{:>26}".format(input_content)

        inp.append(inptx)
        # print step
        step += 1

        get_action = ACTION(top_stack, curr_symbol)
        act.append(get_action)
        if "/" in get_action:
            conf = "{:^26}|".format(get_action + ". So conflict")
            confx = "{:^26}".format(get_action + ". So conflict")

            act[-1] = confx
            break
        if "s" in get_action:
            stack.append(curr_symbol)
            stack.append(get_action[1:])
            pointer += 1
        elif "r" in get_action:
            i = 0
            for head in G.keys():
                for prods in G[head]:
                    if i == int(get_action[1:]):
                        for j in range(2 * len(prods)):
                            stack.pop()
                        state = stack[-1]
                        stack.append(head)
                        stack.append(parse_table[int(state)][len(terminals) + nonterminals.index(head)])
                    i += 1

        elif get_action == "acc":
            print("{:^26}|".format("ACCEPTED"))
            break
        else:
            print("ERROR: Unrecognized symbol", curr_symbol, "|")
            break

    return step, ste, sta, inp, act


def view_lr():
    dot.render('test.gv.svg', view=True,format='png')


def view_parsing():

    Parse_table.tree(parse_table)



def helper():
    parse_grammar()
    items()
    global parse_table
    parse_table = [["" for c in range(len(terminals) + len(nonterminals) + 1)] for r in range(len(C))]
    construct_dfa()

def remove_numbers(lst):
        major_list = []
        for i in range(len(lst)):
            sublist = lst[i].split()
            for j in range(0, len(sublist), 2):
                sublist[j] = int(sublist[j])
            no_integers = [x for x in sublist if not isinstance(x, int)]
            major_list.append(no_integers)
        nodeCount = 0
        i = 1
        while i < len(major_list):
            minLength = min(len(major_list[i]), len(major_list[i-1]))
            for j in range(minLength):
                if major_list[i][j] == major_list[i-1][j].split(".")[0]:
                    major_list[i][j] += "." + major_list[i-1][j].split(".")[1]
                else:
                    major_list[i][j] += "." + str(nodeCount)
                    nodeCount += 1
            if len(major_list[i]) > len(major_list[i-1]):
                j = minLength
                while j < len(major_list[i]):
                    major_list[i][j] += "." + str(nodeCount)
                    nodeCount += 1
                    j+=1
            i+=1
        return major_list

def parse_tree_generator(lst):
    stack = remove_numbers(lst)
    G = nx.DiGraph()
    i = 1
    print(stack)
    while i < len(stack):
        # add rightmost entry in stack
        G.add_node(stack[i][len(stack[i]) - 1])
        myChildren = []
        minLength = min(len(stack[i]), len(stack[i-1]))
        for j in range(minLength):
            if stack[i][j] != stack[i-1][j]:
                myChildren.append(stack[i-1][j])
        if len(stack[i-1]) > len(stack[i]):
            myChildren += stack[i-1][minLength:]
        for child in myChildren:
            G.add_edge(stack[i][len(stack[i]) - 1], child)
        i += 1
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, node_size=500, with_labels=True, node_color="white")
    plt.show()
    # return G

