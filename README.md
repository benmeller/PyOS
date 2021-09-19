# PyOS

Simple dummy operating system created in Python using only standard library modules and existing entirely in memory.

Long-term goal is to have this somewhat mimick a Unix-like OS with kernel modules that can be dynamically created and loaded at runtime, a file system, users and permissions. The intent is for this to become a good starting platform to write simple priv-esc style CTF challenges

This current system is centred around Python's cmd.Cmd, meaning the prompt is everything. It was a quicker way to get up and running, and should be fairly easy to remove later on to better simulate an operating system.

## Currently implemented
At the moment, we have a working prompt, filesystem, basic commands (cd, ls, cat), a text editor, and a way to load "kernel modules" that exist as Python code

## To do

* Load kernel modules from files
* Users
* Permissions
* Boot/reboot
* Remove cmd.Cmd `cmdloop()` as central point of OS