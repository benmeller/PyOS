"""
According to the Linux way of thinking, we'll make everything a file.

Code inspired by: https://stackoverflow.com/a/35072003
"""

# Need a better way to make this constant available such that it is dynamically configurable. 
# Low priority, and this works for now, so...
DELIM = "/"

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
        out_string = self.name
        if self.directory:
            out_string += DELIM
        return out_string

    def get_children(self):
        if self.directory:
            return self.children
        else:
            print("A file cannot have children")

    def add_child(self, filepath):
        if not self.directory:
            print("Cannot add children to a file")
            return 
        self.children.append(filepath)

    def printFileTree(self, depth = -1):
        depth += 1
        print("  "*depth + str(self))
        if len(self.children) > 0:
            for child in self.children:
                child.printFileTree(depth)