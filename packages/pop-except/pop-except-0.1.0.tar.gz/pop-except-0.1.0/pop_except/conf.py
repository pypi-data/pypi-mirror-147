CONFIG = {
    "traceback_limit": {
        "os": "POP_TRACEBACK_LIMIT",
        "help": "The length of python tracebacks on exception",
        "type": int,
        "default": None,
    },
    "hook_plugin": {
        "os": "POP_EXCEPTION_HOOK_PLUGIN",
        "help": "The exception hook plugin to use",
        "type": str,
        "default": "default",
    },
}

CLI_CONFIG = {}

DYNE = {"except": ["except"]}
