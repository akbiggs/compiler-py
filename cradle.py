# cradle.py
# Boilerplate code for the compiler.

import sys
import pdb
from char_ops import getch, char_range

""" CONSTANTS """

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 

""" VARIABLES """

# lookahead character
look = ''

""" FUNCTIONS """

def get_char():
    """
    Read new character from the input stream.
    """
    global look
    look = getch()

def error(msg):
    """
    Report an error.
    Pre: msg {str} is an error message.
    """
    print "\aError: {}.".format(msg)

def abort(msg):
    """
    Report an error and halt.
    Pre: msg {str} is an error message.
    """
    error(msg)
    sys.exit()

def expected(expectee):
    """
    Report what was expected.
    Pre: expectee {str} is what was expected to be read by the compiler.
    """
    abort(expectee + " Expected")

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

def is_alpha(c):
    """
    Recognize an alpha character.
    Pre: c {char} is a character we've read.
    Post: Return true if x is alphabetical, false otherwise.
    """
    return c.upper() in char_range('A', 'Z')

def is_digit(c):
    """
    Recognize a decimal digit.
    """
    return c in DIGITS

def is_addop(c):
    return c in ['+', '-']

def get_name():
    """
    Get an identifier.
    """
    if not is_alpha(look):
        expected("Name")

    return look.upper()

def get_num():
    """
    Get a number.
    """
    if not is_digit(look):
        expected("Integer")

    return look

def emit(s):
    """
    Output a string with a tab.
    """
    print "\t%s" % s,

def emit_line(s):
    """
    Output a string with a tab and end of line character.
    """
    emit(s)
    print

def ident():
    """
    Parse and translate an identifier.
    """
    name = get_name()
    get_char()
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
        get_char()

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
    while look in ['*', '/']:
        emit_line("MOVE D0,-(SP)")
        if look == '*': multiply()
        elif look == '/': divide()
        else: expected("Mulop")

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
        else: expected('Addop')

def init():
    get_char()

""" MAIN PROGRAM """

if __name__ == "__main__":
    init()
    expression()
