import sys


def __init__(hub):
    # Save the system exception hook before it gets overridden
    hub.exc.hook.default.SYS_EXCEPTHOOK = sys.excepthook


def hook(hub, exc_type, exc_value, exc_traceback):
    """
    Handle an exception by displaying it with a traceback on sys.stderr
    """
    hub.exc.hook.default.SYS_EXCEPTHOOK(exc_type, exc_value, exc_traceback)
