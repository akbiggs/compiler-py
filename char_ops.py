# char_ops.py
# Various useful operations on characters.

class _Getch:
    """
    Gets a single character from standard input.  Does not echo to the screen.
    Taken from: http://code.activestate.com/recipes/134892/
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def char_range(c1, c2):
    """
    Generates the characters from `c1` to `c2`, inclusive.
    Taken from http://stackoverflow.com/questions/7001144
    """
    for c in xrange(ord(c1), ord(c2)+1):
        yield chr(c)

getch = _Getch()
