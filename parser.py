# parser.py
# Boilerplate code for the compiler.

import sys
import pdb
from cradle import *

# lookahead char
look = ''

def get_char():
    """
    Read new character from the input stream.
    """
    global look
    look = getch()

def match(x):
    """
    Match a specific input character.
    Pre: x {char} is an input character that is expected to be read.
    Post: Gets a character if we matched x, otherwise abort.
    """
    if look == x:
        get_char()
    else:
        expected("'{}'".format(x))

def is_addop(c):
    return c in ['+', '-']

def is_mulop(c):
    return c in ['*', '/']

def get_name():
    """
    Get an identifier.
    """
    token = ""
    if not is_alpha(look):
        expected("Name")
    
    while is_alnum(look):
        token += look.upper()
        get_char()

    return token

def get_num():
    """
    Get a number.
    """
    value = ""
    if not is_digit(look):
        expected("Integer")
    
    while is_digit(look):
        value += look
        get_char()

    return value

def ident():
    """
    Parse and translate an identifier.
    """
    name = get_name()
    if look == '(':
        match('(')
        match(')')
        emit_line("BSR " + name)
    else:
        emit_line("MOVE " + name + "(PC),D0")

    return name

def factor():
    """
    Parse and translate a math factor.
    """
    if look == '(':
        match('(')
        expression()
        match(')')
    elif is_alpha(look):
        ident()
    else:
        emit_line("MOVE {},DO".format(get_num()))

def multiply():
    """
    Recognize and translate a multiply.
    """
    match('*')
    factor()
    emit_line("MULS (SP)+,D0")

def divide():
    """
    Recognize and translate a divide.
    """
    match('/')
    factor()
    emit_line("MOVE (SP)+,D1")
    emit_line("DIVS D1,D0")

def term():
    factor()
    while is_mulop(look):
        emit_line("MOVE D0,-(SP)")
        if look == '*': multiply()
        elif look == '/': divide()

def add():
    match('+')
    term()
    emit_line("ADD (SP)+,D0")

def subtract():
    match('-')
    term()
    emit_line("SUB (SP)+,D0")
    emit_line("NEG D0")

def expression():
    if is_addop(look):
        emit_line("CLR DO")
    else:
        term()
    while is_addop(look):
        emit_line("MOVE D0,-(SP)")
        if look == '+': add()
        elif look == '-': subtract()

def assignment():
    name = get_name()
    match('=')
    expression()
    emit_line("LEA " + name + "(PC),A0")
    emit_line("MOVE D0,(A0)")

def init():
    get_char()

""" MAIN PROGRAM """

if __name__ == "__main__":
    init()
    assignment()

    # TODO: Make this platform independent.
    if look != '\r':
        expected("Newline")
