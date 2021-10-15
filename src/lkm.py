"""Loadable Kernel Modules
A bunch of simulated loadable kernel modules to be added to PyOS.

Currently in this file for readability's sake. For later compilation and obfuscation, may be moved over into the main file

Below are the essential modules needed in order to build the system. Once they are in place, all other modules can simply be written as 'files' in pyos and loaded. Again, inspiration taken from Alan Robertson
"""
import ast
import code

def module_loader(self, filename: str, *args, **kwargs):
    """
    Compile loadable modules from PyOS files. The filename argument should either be reference a pre-existing file that exists in the /lib directory or it should be an absolute file path.

    Usage: module_load filename 
    """
    if filename.startswith("/"):
        # Allows for absolute paths on boot
        file, _ = self.resolve_path(self.fs, f"{filename}", directory=False)
    else:
        file, _ = self.resolve_path(self.fs, f"/lib/{filename}", directory=False)


    if _ != '':
        print(f"File '{filename}' was not found!")
        return False

    mod = ast.literal_eval(file.contents)

    try:
        mod['name']
    except:
        print(f"Module in file {filename} has no name! Module build failed")
        return False

    if mod['name'] != filename.split("/")[-1]:
        # This allows unloading with assumption that modname == filename
        print(mod['name'])
        print(filename)
        print("Filename must be the same as module name. Module build failed")
        return False

    help_string = f"""
    {mod['help'] if ('help' in mod.keys()) else "No info available"}
    
    Usage: {mod['usage'] if ('usage' in mod.keys()) else "No usage info available"}
    """

    func_string = f"""def {mod['name']}(self, args):
    '''{help_string}'''
    {mod['function']}"""
    

    binary = compile(func_string, mod['name'], 'exec')
    try:
        exec(binary)
    except:
        print("Module execution failed")
        return False
    self.mkfile(self.fs, f"/bin/{mod['name']}", contents=locals()[mod['name']].__code__.co_code)

    # We inject func into globals to allow for recursive calls at the very least
    globals()[mod['name']] = locals()[mod['name']] 

    # Add executable to module data
    mod['exec'] = globals()[mod['name']]

    # Add module to OS
    self.load_lkm(mod, *args, **kwargs)

def module_unloader(self, module: str):
    # We keep this here so reboot doesn't accidentally unload this too
    # 
    # Note that we unload at shutdown so there aren't any remnant modules 
    # lying around after reboot which technically shouldn't be loaded in to 
    # the OS
    """
    Given a module name, unload from OS

    Usage: module_unload modulename 
    """
    if not self.unload_lkm(module):
        return False
    file, _ = self.resolve_path(self.fs, f"/bin/{module}", directory=False)
    bin = file.parent
    bin.children.remove(file)
    del file
    return True


# TODO: Technically the functions resolve_path() and mkfile() should exist here before being added to the OS object
# 
# This would help clarify the distinction between layers of the "OS" - underlying code to make things work (e.g. being 
# able to dynamically mount functions to the object) and provide a bare bones interface for us to start adding in 
# specific functionality relevant to the os-side of the OS object
#
# i.e. the OS object should be bare bones, providing the smallest interface necessary for us to then start adding 
# modules to it to allow it to do our work. At least from a loadable modules vs essential pre-defined methods pov