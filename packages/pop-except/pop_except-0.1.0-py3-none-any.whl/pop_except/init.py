def __init__(hub):
    hub.pop.sub.add(dyne_name="except", omit_class=False)
    hub.pop.sub.load_subdirs(hub["except"], recurse=True)
    # Read OS vars and defaults for an initial configuration of exceptions
    # This will need be done again by an app that wants to configure exceptions based on a config file
    hub.pop.config.load(["pop_except"], "pop_except", parse_cli=False)
    hub.exc.init.configure()
