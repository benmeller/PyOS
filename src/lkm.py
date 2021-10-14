"""Loadable Kernel Modules
A bunch of simulated loadable kernel modules to be added to PyOS.

Currently in this file for readability's sake. For later compilation and obfuscation, may be moved over into the main file

Below are the essential modules needed in order to build the system. Once they are in place, all other modules can simply be written as 'files' in pyos and loaded. Again, inspiration taken from Alan Robertson
"""
import ast

def module_loader(self, filename: str):
    """
    Compile loadable modules from PyOS files. The filename argument should reference a pre-existing file that exists in the /lib directory.

    Usage: module_load filename 
    """
    file, _ = self.resolve_path(self.fs, f"/lib/{filename}", directory=False)
    if _ != '':
        print(f"File '{filename}' was not found in /lib!")
        return False

    mod = ast.literal_eval(file.contents)

    try:
        mod['name']
    except:
        print(f"Module in file f{filename} has no name! Module build failed")
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
    self.load_lkm(mod['name'], globals()[mod['name']])