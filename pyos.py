from cmd import Cmd
import types
import getpass
from lkm import *

class PyOS(Cmd):
    def __init__(self, root="/", delim="/", completekey='tab') -> None:
        super().__init__(completekey)

        self.fs = {}

        self.delim = delim 
        self.root = root 

        self.current_dir = []

        self.modules = {}

        self.username = getpass.getuser()
        self.compname = "pyos"
        self.prompt = "\033[92m{user}@{hostname}\033[0m:\033[94m{dir}\033[0m$ ".format(
            user=self.username,
            hostname=self.compname,
            dir=(self.root + self.delim.join(self.current_dir))
        )

    def load_lkm(self, lkm_name, lkm):
        """
        Loadable kernel module. Add command dynamically to PyOS by promoting 
        a func to a method.

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
    "hello": hello,
    "ls": ls,
    "mkdir": mkdir,
    "mkfile": mkfile,
    "clear": clear
}

if __name__=="__main__":
    comp = PyOS()
    for name in modules.keys():
        comp.load_lkm(name, modules[name])

    comp.cmdloop()