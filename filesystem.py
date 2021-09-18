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

        if filepath != None:
            self.directory = directory

            try:
                self.name, child = filepath.split(DELIM, 1)
                self.children.append(File(filepath=child, directory=directory, parent=self, contents=contents))
                self.directory = True # If children, must be a directory
            except ValueError:
                self.name = filepath

            if not directory:
                self.contents = contents

    def __repr__(self) -> str:
        if self.directory:
            out_string = self.name + DELIM
        else:
            out_string = self.name

        return out_string

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

    def mkfile(self, filepath, **kwargs):
        if not self.directory:
            print("Cannot add subdirectory to a file")
            return

        target_dir, updated_path = self.resolve_path(filepath)
        target_dir.add_child(File(updated_path, parent=target_dir, **kwargs))

    def resolve_path(self, filepath):
        """
        For a given filepath, resolve whatever path exists and pass back two objects:
        - File object of the resolved path
        - filepath string of whatever if remaining

        For example, let's say this folder exists /foo/bar/, and we wish to resolve
        /foo/bar/baz/myfile, resolve_path() will return:
        - The File object associated with /foo/bar
        - Remaining string "baz/myfile"
        """
        if filepath == "":
            return self, ""

        dir_path = filepath.split(DELIM)

        # ----- Upward traversal -----
        if dir_path[0] == ROOT:
            # Absolute path. Traverse to top of tree and back down
            if self.parent == None:
                # Begin resolving down now
                return self.resolve_path(DELIM.join(dir_path[1:]))    
            else:
                # Keep going up
                return self.parent.resolve_path(filepath)
        elif dir_path[0] == '..':
            # Resolve from parent directory
            return self.parent.resolve_path(DELIM.join(dir_path[1:]))

        elif dir_path[0] == '.':
            # Current directory
            return self.resolve_path(DELIM.join(dir_path[1:]))
            
        # ----- Downward traversal -----
        else:
            for child in self.get_children():
                if child.name == dir_path[0]:
                    if (len(dir_path) > 1) and not child.directory:
                        # We've come across a file of the same name. Ignore.
                        continue
                    return child.resolve_path(DELIM.join(dir_path[1:]))
            
            # If child not found, we've reached end of traversal
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


if __name__=="__main__":
    myfs = File(filepath=ROOT, directory=True)

    myfs.mkfile('bin/bash', contents="Hello, world!")
    myfs.mkfile('boot', directory=True)
    # myfs.mkfile('etc', directory=True)
    # myfs.mkfile('home', directory=True)
    # myfs.mkfile('var', directory=True)

    children = myfs.get_children()
    bin = children[0]
    boot = children[1]
    # print(bin.get_children())

    print(bin.resolve_path("/boot/leg"))
    print(bin.resolve_path("../boot/leg"))
    print(boot.resolve_path("./leg"))
    bin.mkfile("/boot/leg")
    print(bin.resolve_path("/boot/leg"))
    print(bin.resolve_path("../boot/leg"))
    print(boot.resolve_path("./leg"))
    myfs.printFileTree()