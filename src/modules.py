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
    for i in dir.get_children():
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

MODULES = {
    "touch": touch,
    "cat": cat,
    "exit": exit,
    "ls": ls,
    "cd": cd,
    "mkdir": mkdir,
    "clear": clear,
    "edit": edit,
}