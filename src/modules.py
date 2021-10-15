touch='''{
"name": "touch",
"help": "Create a new, empty file, or multiple files",
"usage": "touch filename1 ...",
"function": """
    args = args.split()
    if len(args) > 1:
        for newdir in args:
            touch(self, newdir)
    elif len(args) == 1:
        print("Creating File", args)
        self.mkfile(self.current_dir, args[0], directory=False)
"""}'''

cat='''{
"name": "cat",
"help": "Print contents of a single file to stdout",
"usage": "cat filename",
"function": """
    args = args.split()
    if len(args) != 1:
        print("Usage: cat [filename]")
        return 
    file, path = self.resolve_path(self.current_dir, args[0], directory=False)
    if path != '':
        print(args[0], "does not exist!")
        return
    print(file.contents)
"""}'''

exit = '''{
"name": "exit",
"help": "Exits PyOS",
"usage": "exit",
"function": """
    print("Goodbye!")
    raise SystemExit
"""}'''

mkdir = '''{
"name": "mkdir",
"help": "Create one or multiple directories",
"usage": "mkdir directory ...",
"function": """
    args = args.split()
    if len(args) > 1:
        # Call current method for each folder individually
        for newdir in args:
            mkdir(self, newdir)
    elif len(args) == 1:
        print("Creating directory", args)
        self.mkfile(self.current_dir, args[0], directory=True)
"""}'''

ls = '''{
"name": "ls",
"help": "Prints out the contents of a given directory",
"usage": "ls directory",
"function": """
    args = args.split()

    if len(args) > 1:
        print("Usage: ls [directory]")
        return
    elif len(args) == 1:
        dir, path = self.resolve_path(self.current_dir, args[0], directory=True)
        if path != '':
            print(args[0], "is not a directory!")
            return
    else:
        dir = self.current_dir

    print("Directory:", dir.filepath)
    for i in sorted(dir.get_children(), key=lambda x: x.name):
            print(i, end="\t")
    print()
"""}'''

cd = '''{
"name": "cd",
"help": "Move to a given directory",
"usage": "cd directory",
"function": """
    args = args.split()
    if len(args) != 1:
        print("Usage: cd [directory]")
        return
    new_dir, path = self.resolve_path(self.current_dir, args[0], directory=True)
    if path != '':
        print(args[0], "is not a directory!")
        return
    self.current_dir = new_dir
"""}'''

clear = '''{
"name": "clear",
"help": "Clears the screen",
"usage": "clear",
"function": """
    import os
    os.system("clear")
"""}'''

edit = '''{
"name": "edit",
"help": "Open a pyos file in the text editor. If the file does not exist, a new file is created implicitly (even if changes aren't written to the new file)",
"usage": "edit filename",
"function": """
    import curses
    import texteditor
    args = args.split()
    if len(args) != 1:
        print("Usage: edit [filename]")
        return
    file, path = self.resolve_path(self.current_dir, args[0], directory=False)
    if path != '':
        # If file does not exist, implicitly create it
        self.mkfile(file, args[0], directory=False)
        file, path = self.resolve_path(file, path, directory=False)
    curses.wrapper(texteditor.edit_file, file=file)
"""}'''

reboot = '''{
"name": "reboot",
"help": "Restarts the computer",
"usage": "reboot",
"function": """
    import time
    print("Rebooting...")
    time.sleep(2)
    bin, _ = self.resolve_path(self.fs, "/bin", directory=True)
    modules = bin.get_children().copy()
    for mod in modules:
        self.do_module_unload(mod.name)
    bin, _ = self.resolve_path(self.fs, "/bin", directory=True)
    self.boot(args)
"""}'''

LIB_MODULES = {
    "touch": touch,
    "cat": cat,
    "exit": exit,
    "ls": ls,
    "cd": cd,
    "mkdir": mkdir,
    "clear": clear,
    "edit": edit,
    "reboot": reboot,
}


# --------------------------------------------------------

boot = r'''{
"name": "boot",
"function": """
    import time
    print("Starting up...")
    time.sleep(1)
    lib, _ = self.resolve_path(self.fs, "/lib", directory=True)
    modules = lib.get_children()
    for mod in modules:
        print(f" Loading {mod.name}", ' '*15, end="\\r")
        self.do_module_load(f"/lib/{mod.name}")
        time.sleep(0.15)
    print(" "*30, end="\\r")
    print(self.intro_str)
"""}'''

BOOT_MODULES = {
    "boot": boot,
}