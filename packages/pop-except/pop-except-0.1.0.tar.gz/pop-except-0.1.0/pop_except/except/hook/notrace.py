import sys
from traceback import format_exception_only


def hook(hub, exc_type, exc_value, exc_traceback):
    """
    Handle an exception by displaying it with a traceback on sys.stderr
    """
    lines = format_exception_only(exc_type, value=exc_value)
    sys.stderr.write("\n".join(lines))
