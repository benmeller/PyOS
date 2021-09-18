"""
A bunch of simulated loadable kernel modules to be added to PyOS.

Currently in this file for readability's sake. For later compilation and obfuscation, may be moved over into the main file

*Eventually* (For now, writing all modules as code just to get it working)
Below are the essential modules needed in order to build the system. Once they are in place, all other modules can simply be written as 'files' in pyos and loaded. Again, inspiration taken from Alan Robertson
"""
import os

def exit(self, args):
    """Exits PyOS"""
    print("Goodbye!")
    raise SystemExit

def mkdir(self, args):
    """Create one or multiple directories
    
    Usage: mkdir directory[ directory]
    """
    args = args.split()

    if len(args) > 1:
        # Call current method for each folder individually
        for newdir in args:
            mkdir(self, newdir)
    elif len(args) == 1:
        print("Creating directory", args)
        self.current_dir.mkfile(args[0], directory=True)

def touch(self, args):
    """Create a new, empty file, or multiple

    Usage: touch filename
    """
    args = args.split()

    if len(args) > 1:
        # Call current method for each file individually
        for newdir in args:
            touch(self, newdir)
    elif len(args) == 1:
        print("Creating Files", args)
        self.current_dir.mkfile(args[0], directory=False)

def cat(self, args):
    """Print contents of a single file to stdout
    
    Usage: cat filename"""
    args = args.split()

    if len(args) != 1:
        print("Usage: cat [filename]")
        return 

    file, path = self.current_dir.resolve_path(args[0], directory=False)
    if path != '':
        print(args[0], "does not exist!")
        return

    print(file.contents)

def ls(self, args):
    """
    Prints out the contents of a given directory

    Usage: ls [directory]"""
    args = args.split()

    if len(args) > 1:
        print("Usage: ls [directory]")
        return
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

def cd(self, args):
    """
    Move to a given directory.

    Usage: cd [directory]
    """
    args = args.split()

    if len(args) != 1:
        print("Usage: cd [directory]")
        return

    new_dir, path = self.current_dir.resolve_path(args[0], directory=True)
    if path != '':
        print(args[0], "is not a directory!")
        return

    self.current_dir = new_dir

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