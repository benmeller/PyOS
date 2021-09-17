"""
A bunch of simulated loadable kernel modules to be added to PyOS.

Currently in this file for readability's sake. For later compilation and obfuscation, may be moved over into the main file

Below are the essential modules needed in order to build the system. Once they are in place, all other modules can simply be written as 'files' in pyos and loaded. Again, inspiration taken from Alan Robertson
"""
import os

def hello():
    print("Hello, World!")

def mkdir():
    pass 

def mkfile():
    pass

def ls(self, *args):
    """
    Prints out the contents of a directory
    """
    print("args:", *args)
    print("Directory:", self.root + self.delim.join(self.current_dir))
    # for i in self.get_current_directory():
    #         print(i)

def cd(self, *args):
    pass

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