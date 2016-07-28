
from clint.textui import puts, colored, indent
import sys, linecache 

def print_exception(e, full=True, cause=False, tb=None):
    """
    Prints the exception with nice colors and such.
    """
    def format(e):
        return '%s%s: %s' % (colored.red('Caused by ') if cause else '', colored.red(e.__class__.__name__, bold=True), colored.red(str(e)))

    puts(format(e))
    if full:
        if cause:
            if tb:
                print_traceback(tb)
        else:
            print_traceback()
    if hasattr(e, 'cause') and e.cause:
        tb = e.cause_tb if hasattr(e, 'cause_tb') else None
        print_exception(e.cause, full=full, cause=True, tb=tb)

def print_traceback(tb=None):
    """
    Prints the traceback with nice colors and such.
    """
    
    if tb is None:
        _, _, tb = sys.exc_info()
    while tb is not None:
        frame = tb.tb_frame
        lineno = tb.tb_lineno
        code = frame.f_code
        filename = code.co_filename
        name = code.co_name
        with indent(2):
            puts('File "%s", line %s, in %s' % (colored.blue(filename), colored.cyan(lineno), colored.cyan(name)))
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, frame.f_globals)
            if line:
                with indent(2):
                    puts(colored.black(line.strip()))
        tb = tb.tb_next
