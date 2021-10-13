"""
Need to make a tree structure.

Every non-leaf is a directory. Every leaf can either be a directory or a file.

According to the Linux way of thinking, we'll make everything a file.

Code inspired by: https://stackoverflow.com/a/35072003
"""

DELIM = "/"
ROOT = ""

class File(object):
    def __init__(self, filepath=None, directory=False, contents="", parent=None) -> None:
        self.children = []
        self.parent = parent
        
        try:
            parentfilepath = parent.filepath
        except AttributeError:
            parentfilepath = ''

        if filepath != None:
            self.directory = directory

            try:
                self.name, child = filepath.split(DELIM, 1)
                self.filepath = parentfilepath + repr(self)
                self.children.append(File(filepath=child, directory=directory, parent=self, contents=contents))
                self.directory = True # If children, must be a directory
            except ValueError:
                self.name = filepath
                self.filepath = parentfilepath + repr(self)

            if not directory:
                self.contents = contents

    def __repr__(self) -> str:
        if self.directory:
            out_string = self.name + DELIM
        else:
            out_string = self.name

        return out_string


    # --------------------------------------
    def get_children(self):
        if self.directory:
            return self.children
        else:
            print("A file cannot have children")

    # --------------------------------------
    def add_child(self, filepath):
        if not self.directory:
            print("Cannot add children to a file")
            return 
        self.children.append(filepath)

    def mkfile(self, filepath, **kwargs) -> None:
        """
        Makes a file at the specified location.

        If you want to create a file with the same name as a pre-existing 
        directory, need to specify directory=False in kwargs. Seems dodgy. 
        Can't think of a better way to do it at the moment
        """
        if not self.directory:
            print("Cannot add subdirectory to a file")
            return

        target_dir, updated_path = self.resolve_path(filepath, **kwargs)
        target_dir.add_child(File(updated_path, parent=target_dir, **kwargs))

    def resolve_path(self, filepath, **kwargs):
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
            return self, ""

        dir_path = filepath.split(DELIM)

        # ----- Upward traversal -----
        # Absolute path
        if dir_path[0] == ROOT:
            # Traverse to top of tree and back down
            if self.parent == None:
                # Reached root. Begin resolving down now
                return self.resolve_path(DELIM.join(dir_path[1:]), **kwargs)    
            else:
                # Keep going up
                return self.parent.resolve_path(filepath)
        
        # Parent directory
        elif dir_path[0] == '..':
            return self.parent.resolve_path(DELIM.join(dir_path[1:]), **kwargs)

        # Current directory
        elif dir_path[0] == '.':
            # Current directory
            return self.resolve_path(DELIM.join(dir_path[1:]), **kwargs)
            
        # ----- Downward traversal -----
        else:
            for child in self.get_children():
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
                    return child.resolve_path(DELIM.join(dir_path[1:]), **kwargs)
            
            # If child not found, we've reached end of traversal, can return
            target_dir = self 
            new_path = DELIM.join(dir_path)

        return target_dir, new_path


    # --------------------------------------
    def printFileTree(self, depth = -1):
        depth += 1
        print("  "*depth + str(self))
        if len(self.children) > 0:
            for child in self.children:
                child.printFileTree(depth)

def fs_setup():
    fs = File(filepath=ROOT, directory=True)

    fs.mkfile('bin', directory=True)
    fs.mkfile('home', directory=True)
    fs.mkfile('etc', directory=True)
    fs.mkfile('lib', directory=True)
    fs.mkfile('boot', directory=True)
    fs.mkfile('root', directory=True)

    fs.mkfile('/etc/shadow', contents="Very secure passwords be here")

    fs.mkfile('/lib/ls', contents="I am ls")
    fs.mkfile('/lib/echo', contents="I am echo")
    fs.mkfile('/lib/cd', contents="I am cd")
    
    fs.mkfile('bin', directory=False)

    fs.mkfile('boot/leg/candy', directory=True)
    return fs

def test_fs(myfs):
    children = myfs.get_children()
    bin = children[0]
    boot = children[2]

    # print(bin.resolve_path("/boot/leg"))
    # print(bin.resolve_path("../boot/leg"))
    # print(boot.resolve_path("./leg"))
    # bin.mkfile("/boot/leg")
    # print(bin.resolve_path("/boot/leg"))
    # print(bin.resolve_path("../boot/leg"))
    # print(boot.resolve_path("./leg"))

    print("=====")
    print(myfs.resolve_path('/bin/bash'))
    print("Find file")
    print(myfs.resolve_path('/bin')) # Only because file was made before directory
    print(myfs.resolve_path('/bin', directory=False))
    print("Find dir")
    print(myfs.resolve_path('/bin/'))
    print(myfs.resolve_path('/bin', directory=True))

if __name__=="__main__":
    myfs = fs_setup()

    test_fs(myfs)

    # print("Finished filesystem:")
    # myfs.printFileTree()
    # print("==================\n")