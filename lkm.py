"""
A bunch of simulated loadable kernel modules to be added to PyOS.

Currently in this file for readability's sake. For later compilation and obfuscation, may be moved over into the main file

Below are the essential modules needed in order to build the system. Once they are in place, all other modules can simply be written as 'files' in pyos and loaded. Again, inspiration taken from Alan Robertson
"""
import os

def hello(self, *args):
    print("Hello, World!")

def mkdir(self, *args):
    pass 

def mkfile(self, *args):
    pass

def ls(self, args):
    """
    Prints out the contents of a given directory

    Usage: ls [directory]
    """
    args = args.split()

    if len(args) > 1:
        print("Usage: ls [directory]")
    elif len(args) == 1:
        dir, path = self.current_dir.resolve_path(args[0], directory=True)
        if path != '':
            print(args[0], "is not a directory!")
            return
    else:
        dir = self.current_dir

    print("Directory:", dir.filepath)
    for i in dir.get_children():
            print(i, end="\t")
    print()

def cd(self, *args):
    """
    Move to a given directory.

    Usage: cd [directory]
    """
    if len(args) > 1:
        print("Usage: cd [directory]")
    elif len(args) == 1:
        dir, path = self.current_dir.resolve_path(args[0], directory=True)
        if path != '':
            print(args[0], "is not a directory!")
            return

    self.current_dir = dir

def clear(self, *args):
    """
    Clears the screen
    """
    os.system("clear")

def lkm_loader():
    """
    Compile LKMs from PyOS files
    """
    # As nice as this is, not a priority to get a basic OS going.
    # Will be needed for later privesc
    pass