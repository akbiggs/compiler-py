# cradle.py
# Various helper functions.

import sys
from char_ops import getch, char_range

# CONSTANTS

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 

# VARIABLES

# lookahead character
look = ''

# FUNCTIONS

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

def is_alnum(c):
    """
    Recognize an alphanumeric character.
    """
    return is_alpha(c) or is_digit(c)

def is_white(c):
    """
    Recognize white space.
    """
    return c in [' ', '\t']

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
