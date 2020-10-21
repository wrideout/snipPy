# clipboardManager

## Summary
clipboardManager is a lightweight utility for making the last 30 entries of the system clipboard available for re-use in a simple UI.  clipboardManager does not support networking of any kind, and the contents of the system clipboard are not saved outside the host device.  The contents of clipboardManager are recorded internally and are cleared at application restart.

## Dependencies and Installation
clipboardManager is written in Python v3.8.5, and relies on the following Python libraries for GUI support and access to the system clipboard:

- [pyperclip v1.8.1](https://pypi.org/project/pyperclip/)
- [PyQt5 v5.15.1](https://pypi.org/project/PyQt5/)

The both pyperclip and PyQt5 are available within the libraries of PyPi, and may be installed via the `pip3` command.

```
$ pip3 install pyperclip
$ pip3 install PyQt5
```

Installation instructions for Python3 may be found [here](https://www.python.org/downloads/).

Running clipboardManager may be accomplished several different ways, the most basic of which is simply invoking the command from the CLI as a background task:

```
$ python3 clipboard_mgr_qt.py&
```

Alternatively, this project has been packaged via py2app (more info [here](https://py2app.readthedocs.io/en/latest/index.html)) to be runnable as a standalone application for Apple macOS.  The executable for this application may be found in the `dist` directory of this repository, and may be copied to an appropriate location by the user.

Although not already completed, instructions for creating standalone executables for MS Windows and Linux are below.  This is left as an excersise for the user.
- MS Windows, via [py2exe](https://pypi.org/project/py2exe/)
- Linux, via [pyinstaller](https://pypi.org/project/pyinstaller/)

An icon for use with standalone binaries created from this project is included in this repository, and is available for use via the MIT license.  The icon and others in the icon set may be viewed [here](https://www.iconfinder.com/icons/2561366/paperclip_icon).  The icon is 512x512 pixels in size.

## Basic Usage
Once run, clipboardManager waits for new text to be copied to the system clipboard.  Once a text snippet is copied, it is displayed in the main window of clipboardManager.  Up to 30 snippets may be stored.  Displayed snippets may be re-selected for use by simply clicking on an entry.  This causes the selected text snippet to be placed at the top of the system clipboard so it may be immediately used.

Note that this application exits if the main window of clipboardManager is closed.

## License
This software is available for free use via the terms of the GNU General Public License (GPL).  See LICENSE for more details.