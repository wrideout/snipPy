# snipPy

## Summary
snipPy is a lightweight system tray utility for making the last 30 entries of the
system clipboard available for re-use in a simple UI.  snipPy does not
support networking of any kind, and the contents of the system clipboard are not
saved outside the host device.  The contents of snipPy are recorded
internally and are cleared at application restart.

## Dependencies and Installation
snipPy is written in Python v3.8.5, and relies on the following Python
libraries for GUI
support and access to the system clipboard:

- [pyperclip v1.8.1](https://pypi.org/project/pyperclip/)
- [PyQt5 v5.15.1](https://pypi.org/project/PyQt5/)

The both pyperclip and PyQt5 are available within the libraries of PyPi, and may be
installed via the `pip3` command.  It is recommended that all all `pip3` commands are
run from within a virtual environment.

```bash
$ pip3 install pyperclip
$ pip3 install PyQt5
```

Alternatively, the user may use the following command to install all dependencies
through the `requirements.txt` file.

```bash
$ pip3 install -r requirements.txt
```

Installation instructions for Python3 may be found
[here](https://www.python.org/downloads/).

Running snipPy may be accomplished several different ways, the most basic
of which is simply invoking the command from the CLI as a background task:

```bash
$ python3 snipPy.py&
```

Although not already completed, instructions for creating standalone executables for
Apple macOS, MS Windows, and Linux are below.  The creation of such binaries is left
as an excersise for the user.
- Apple macOS, via [py2app](https://py2app.readthedocs.io/en/latest/tutorial.html)
- MS Windows, via [py2exe](https://www.py2exe.org/index.cgi/Tutorial)
- Linux, via [pyinstaller](https://www.pyinstaller.org/)

py2app, py2exe, and pyinstaller are available for download and installation via pypi.

An icon for use with standalone binaries created from this project is included in
this repository, and is available for use via the MIT license.  The icon and others
in the icon set were designed by [Cole Bemis](https://colebemis.com/), and may be
viewed [here](https://www.iconfinder.com/icons/2561366/paperclip_icon).

## Basic Usage
Once running, snipPy waits for new text to be copied to the system
clipboard.  Once a text snippet is copied, it is displayed in the context menu of the
snipPy system tray icon.  Up to 30 snippets may be stored.  Displayed snippets may be
re-selected for use by simply clicking on an entry.  This causes the selected text
snippet to be placed at the top of the system clipboard so it may be immediately
used.  The current contents of the system clipboard are indicated in the context menu
of snipPy are indicated by a checkmark icon.

## License
This software is available for free use via the terms of the GNU General Public
License (GPL).  See LICENSE for more details.
