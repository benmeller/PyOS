from cmd import Cmd
import types
import getpass

from lkm import *
from filesystem import *

class PyOS(Cmd):
    """
    Currently only designed for a single user
    """

    def __init__(self, root="", delim="/", completekey='tab') -> None:
        super().__init__(completekey)

        # Temporary setup for now
        self.fs = fs_setup()
        # self.fs = File(filepath=root, directory=True, delim=delim)

        # self.delim = delim 
        # self.root = root 
        self.current_dir = self.fs

        self.modules = {}

        self.username = getpass.getuser()
        self.compname = "pyos"
        self.prompt = "\033[92m{user}@{hostname}\033[0m:\033[94m{dir}\033[0m$ ".format(
            user=self.username,
            hostname=self.compname,
            dir=(self.current_dir.filepath)
        )

    def postcmd(self, *args):
        # Dynamically update prompt. Useful for when cd command is used
        self.prompt = "\033[92m{user}@{hostname}\033[0m:\033[94m{dir}\033[0m$ ".format(
            user=self.username,
            hostname=self.compname,
            dir=(self.current_dir.filepath)
        )


    def load_lkm(self, lkm_name, lkm):
        """
        Loadable kernel module. Dynamically add a 'binary' to PyOS by promoting 
        a func to a method

        Immeasurable thanks to Alan Robertson for insights into this problem
        """
        self.__setattr__("do_"+lkm_name, types.MethodType(lkm, self))

        # TODO: Replace lkm with some lkm data object. 
        self.modules[lkm_name] = lkm

    def get_names(self) -> list[str]:
        """
        Override Cmd.get_names so that dynamically loaded kernel modules show
        up in help menu
        """
        return dir(self)

modules = {
    "exit":exit,
    "ls": ls,
    "cd": cd,
    "mkdir": mkdir,
    "touch": touch,
    "clear": clear,
    "cat": cat,
}

intro_str = """Welcome to PyOS!
Type 'help' to view a list of available commands"""

if __name__=="__main__":
    comp = PyOS()
    for name in modules.keys():
        comp.load_lkm(name, modules[name])
    comp.cmdloop(intro=intro_str)