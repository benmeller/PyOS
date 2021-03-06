from cmd import Cmd
import types
import getpass

import curses

from lkm import *
from filesystem import *
from modules import LIB_MODULES, BOOT_MODULES

DELIM = "/"
ROOT = ""

class PyOS(Cmd):
    """
    Currently only designed for a single user
    """

    def __init__(self, root_name="", delim="/", completekey='tab', intro_str="") -> None:
        super().__init__(completekey)

        # TODO: Make the delimiter and root location modifiable. Low priority
        # self.delim = delim 
        # self.root = root_name 

        self.fs = File(filepath=ROOT, directory=True)
        self.current_dir = self.fs

        self.modules = {}

        self.username = getpass.getuser()
        self.compname = "pyos"
        self.prompt = "\033[92m{user}@{hostname}\033[0m:\033[94m{dir}\033[0m$ ".format(
            user=self.username,
            hostname=self.compname,
            dir=(self.current_dir.filepath)
        )

        self.intro_str = intro_str
        if self.intro_str == "":
            self.intro_str = """Welcome to PyOS!\nType 'help' to view a list of available commands"""

    # --------------- Cmd Overrides --------------------
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

    def get_names(self) -> list[str]:
        """
        Override Cmd.get_names so that dynamically loaded kernel modules show
        up in help menu
        """
        return dir(self)

    # --------------- Filesystem --------------------
    def mkfile(self, current_dir, filepath, **kwargs) -> None:
        """
        Makes a file at the specified location in relation to current_directory
        (which is technically just a file where directory=True).

        If you want to create a file with the same name as a pre-existing 
        directory, need to specify directory=False in kwargs. Seems dodgy. 
        Can't think of a better way to do it at the moment
        """
        if not current_dir.directory:
            print("Cannot add subdirectory to a file")
            return

        target_dir, updated_path = self.resolve_path(self.current_dir, filepath, **kwargs)
        target_dir.add_child(File(updated_path, parent=target_dir, **kwargs))

    def resolve_path(self, current_file, filepath, **kwargs):
        """
        For a given filepath, resolve whatever path exists and pass back two objects:
        - File object of the resolved path
        - filepath string of whatever is remaining

        For example, let's say this folder exists /foo/bar/, and we wish to resolve
        /foo/bar/baz/myfile, resolve_path() will return:
        - The File object associated with /foo/bar
        - Remaining string "baz/myfile"

        In the situation where a file and directory may exist with the same name,
        you can specify which to look for by directory=<boolean> in **kwargs

        TODO: Incorporate permissions
        """
        if filepath == "":
            # Catch recursive case at root
            return current_file, ""

        dir_path = filepath.split(DELIM)

        # ----- Upward traversal -----
        # Absolute path
        if dir_path[0] == ROOT:
            # Traverse to top of tree and back down
            if current_file.parent == None:
                # Reached root. Begin resolving down now
                return self.resolve_path(current_file, DELIM.join(dir_path[1:]), **kwargs)    
            else:
                # Keep going up
                return self.resolve_path(current_file.parent, filepath)
        
        # Parent directory
        elif dir_path[0] == '..':
            return self.resolve_path(current_file.parent, DELIM.join(dir_path[1:]), **kwargs)

        # Current directory
        elif dir_path[0] == '.':
            # Current directory
            return self.resolve_path(current_file, DELIM.join(dir_path[1:]), **kwargs)
            
        # ----- Downward traversal -----
        else:
            for child in current_file.get_children():
                if child.name == dir_path[0]:
                    if len(dir_path) > 1 and not child.directory:
                        # Dir path clearly referencing a directory, not a file
                        # Pass over file and continue searching for dir
                        continue
                    elif 'directory' in kwargs:
                        if (len(dir_path) <= 1) and (kwargs['directory'] != child.directory):
                            # We've come across a file/dir of same name
                            # Can ignore if they're different (dir vs folder)
                            continue
                    return self.resolve_path(child, DELIM.join(dir_path[1:]), **kwargs)
            
            # If child not found, we've reached end of traversal, can return
            target_dir = current_file 
            new_path = DELIM.join(dir_path)

        return target_dir, new_path

    # --------------------------------------
    def load_lkm(self, lkm, *args, **kwargs):
        """
        Loadable kernel module. Dynamically add a 'binary' to PyOS by promoting 
        a func to a method

        Immeasurable thanks to Alan Robertson for insights into this problem
        """
        name, exec = lkm['name'], lkm['exec']


        name = "do_"+name
        if 'hidden' in kwargs:
            if kwargs['hidden'] == True:
                # Hidden allows us to load modules into the OS whilst not having them 
                # show in the cmd.Cmd prompt. 
                name = name.lstrip("do_")

        self.__setattr__(name, types.MethodType(exec, self))

        self.modules[name] = lkm

    def unload_lkm(self, name):
        """
        Given a module name, remove it from the OS
        """
        name = "do_"+name
        if name not in self.modules.keys():
            return False

        # Remove method from OS object
        self.__delattr__(name)
        # Remove record
        del self.modules[name]
        return True


def linux_fs(pyos):
    pyos.mkfile(pyos.fs, 'bin', directory=True)
    pyos.mkfile(pyos.fs, 'home', directory=True)
    pyos.mkfile(pyos.fs, 'etc', directory=True)
    pyos.mkfile(pyos.fs, 'lib', directory=True)
    pyos.mkfile(pyos.fs, 'boot', directory=True)
    pyos.mkfile(pyos.fs, 'root', directory=True)

    for mod in LIB_MODULES.keys():
        pyos.mkfile(pyos.fs, f'/lib/{mod}', contents=LIB_MODULES[mod])
    
    for mod in BOOT_MODULES.keys():
        pyos.mkfile(pyos.fs, f'/boot/{mod}', contents=BOOT_MODULES[mod])
    

def os_setup(pyos):
    linux_fs(pyos)
    comp.load_lkm({"name": "module_load", "exec": module_loader})
    comp.load_lkm({"name": "module_unload", "exec": module_unloader})

    lib, _ = pyos.resolve_path(pyos.fs, "/lib", directory=True)
    
    comp.do_module_load(f"/boot/boot", hidden=True)
    comp.boot([])


if __name__=="__main__":
    comp = PyOS()
    os_setup(comp)
    comp.cmdloop()