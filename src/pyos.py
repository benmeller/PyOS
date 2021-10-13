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

    def cmdloop(self, intro=None):
        """Overriding super.cmdloop() to allow for (a) escaping to create a new
        prompt and (b) exiting on EOF
        
        Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.
        """

        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline
                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                readline.parse_and_bind(self.completekey+": complete")
            except ImportError:
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro)+"\n")
            stop = None
            while not stop:
                try:
                    if self.cmdqueue:
                        line = self.cmdqueue.pop(0)
                    else:
                        if self.use_rawinput:
                            line = input(self.prompt)
                        else:
                            self.stdout.write(self.prompt)
                            self.stdout.flush()
                            line = self.stdin.readline()
                            if not len(line):
                                raise EOFError
                            else:
                                line = line.rstrip('\r\n')
                    line = self.precmd(line)
                    stop = self.onecmd(line)
                    stop = self.postcmd(stop, line)
                    self.postloop()
                except KeyboardInterrupt:
                    print("^C")
        except EOFError:
            print("EOF received. Goodbye!")
            raise SystemExit
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass

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
    "edit": edit,
}

intro_str = """Welcome to PyOS!
Type 'help' to view a list of available commands"""

if __name__=="__main__":
    comp = PyOS()
    for name in modules.keys():
        comp.load_lkm(name, modules[name])
    comp.cmdloop(intro=intro_str)