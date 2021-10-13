"""
A bunch of simulated loadable kernel modules to be added to PyOS.

Currently in this file for readability's sake. For later compilation and obfuscation, may be moved over into the main file

Below are the essential modules needed in order to build the system. Once they are in place, all other modules can simply be written as 'files' in pyos and loaded. Again, inspiration taken from Alan Robertson
"""

def module_loader(self, func_name: str, func_string: str):
    """
    Compile loadable modules from PyOS files. For now, just loading the executable
    from a string while we get the basics working
    """
    binary = compile(func_string, func_name, 'exec')
    try:
        exec(binary)
    except:
        print("Module execution failed")
        return False
    self.mkfile(self.fs, f"/bin/{func_name}", contents=locals()[func_name].__code__.co_code)

    # Inject func into globals and add to os
    globals()[func_name] = locals()[func_name] 
    self.load_lkm(func_name, globals()[func_name])