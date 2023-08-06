import sys

__sub_alias__ = ["exc", "except_"]


def configure(hub, **config):
    """
    Configure exceptions and hooks based on hub.OPT.pop_except values
    """
    if not config:
        config = dict(hub.OPT.pop_except)

    # Set the traceback limit
    traceback_limit = config.get("traceback_limit")
    if traceback_limit is not None:
        sys.tracebacklimit = int(traceback_limit)

    # set the excpetion hook based on the configured plugin
    except_hook_plugin = config.get("hook_plugin")
    if except_hook_plugin:
        sys.excepthook = hub.exc.hook[except_hook_plugin].hook


class PopException(Exception):
    ...
