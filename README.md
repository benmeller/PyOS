# PyOS

Simple dummy operating system created in Python using only standard library modules and existing entirely in memory.

Long-term goal is to have this somewhat mimick a Unix-like OS with kernel modules that can be dynamically created and loaded at runtime, a file system, users and permissions. The intent is for this to become a good starting platform to write simple priv-esc style CTF challenges

This current system is centred around Python's cmd.Cmd, meaning the prompt is everything. It was a quicker way to get up and running, and should be fairly easy to remove later on to better simulate an operating system.

## Currently implemented
At the moment, we have a working prompt, filesystem, basic commands (cd, ls, cat, etc.)and a text editor. We also have a way to dynamically add and remove functionality to and from the OS at runtime.

To add functionality at runtime, you must create a PyOS file in the `/lib` directory (`$ edit filename`). The module data is structured like a python dictionary and must have values for `name` and `function`. Values for `help` and `usage` are recommended. As such, a module file may look like this:

```python
{
"name": "helloworld",
"help": "Prints hello world",
"usage": "helloworld",
"function": """
    print('hello', end=' ')
    print('world')
"""
}
```

But as a bare minimum, must be something like
```python
{
"name": "helloworld",
"function": "print('hello world')"
}
```

Once the file exists, simply call `module_load helloworld` (assuming the file is of the same name) to have the module compiled and available for use.

Do note that since this program only exists in memory, upon exit any modules created will be lost. At this stage, persistence is not something I am after.

## To do

* Users
* Permissions
* Remove cmd.Cmd `cmdloop()` as central point of OS

## Next Steps
Introduce the concept of users (which will be the gateway to adding permissions on file objects)