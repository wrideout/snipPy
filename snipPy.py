#!/usr/bin/env python3
#pylint: disable=invalid-name

'''
clipboard_mgr_qt.py

A simple clipboard manager leveraging pyQt5.

Will Rideout
william.rideout@gmail.com
10/18/2020
'''

from collections import deque
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QAction,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import pyperclip

MAX_DISPLAY_CHAR_COUNT = 30
CLIPPINGS_MAX_LEN = 30

class SystemTray( QSystemTrayIcon ):
    '''
    Class for the main GUI.  snipPy lives in the system tray, and populates a context
    menu based on the last CLIPPINGS_MAX_LEN enties copied to the system clipboard.

    This class contains a timer which polls the system cliboard every 200ms looking
    for new clipboard entries.  If a new entry is found, it is added to the deque and
    dictionary, and a (sometimes) truncated version of the clipped string is printed
    in the GUI for use later.

    In order to preserve the order of the system clipboard, a deque is used.
    However, in order to prevent long lines of text in the GUI, we truncate all
    clippings if they are greater in length than MAX_DISPLAY_CHAR_COUNT.  Since the
    deque can only contain these truncated strings, a dictionary is maintained in
    order to provide a mapping between such truncated display_text and the actual
    clipping from the system clipboard.

    CLIPPINGS_MAX_LEN indicates the maximum depth of the deque.
    '''
    def __init__( self, parent_app, *args, **kwargs ):
        super( SystemTray, self ).__init__( *args, **kwargs )

        self.clippings = deque()
        self.full_clippings = {}

        self.app = parent_app
        self.setIcon( QIcon( 'images/trayIcon.png' ) )
        self.setVisible( True )

        self.actions = []

        # Initial menu contents
        self.menu = QMenu()
        self.menu.addSeparator()
        quit_action = QAction( 'Quit' )
        quit_action.triggered.connect( app.quit )
        self.menu.addAction( quit_action )

        self.timer = QTimer()
        self.timer.setInterval( 200 )
        self.timer.timeout.connect( self.update_clippings )
        self.timer.start()

        self.show()

    def update_context_menu( self ):
        '''
        Populate the list of clippings.  The first clipping is also the current
        contents of the system clipboard, and are so indicated by a checkmark icon.
        All other clippings simply have a dash to visually itemize them.
        '''
        for i, clip in enumerate( self.clippings ):
            action = QAction( clip )
            if not i:
                action.setIcon( QIcon( 'images/firstClipping.png' ) )
            else:
                action.setIcon( QIcon( 'images/clipping.png' ) )
            action.triggered.connect( lambda checked, clip=clip:
                    self.recopy( clip ) )
            self.actions.append( action )

        # Always append static menu items, after a separator.
        separator = QAction()
        separator.setSeparator( True )
        self.actions.append( separator )
        quit_action = QAction( 'Quit' )
        quit_action.triggered.connect( self.app.quit )
        self.actions.append( quit_action )
        self.menu.addActions( self.actions )

    def add_new_clipping( self, clipping, display_text ):
        '''
        Add the passed clipping into the dictionary mapping of display_text to
        clippings, and add the display_text to the deque.

        Maintain the size of the deque and dictionary based on CLIPPINGS_MAX_LEN.

        Refresh the GUI so that the current contents of the deque are shown in the
        context menu.
        '''
        if len( self.clippings ) == CLIPPINGS_MAX_LEN:
            key = self.clippings.pop()
            if key in self.full_clippings:
                del self.full_clippings[ key ]
        self.clippings.appendleft( display_text )
        self.full_clippings[ display_text ] = clipping
        self.menu.clear()
        self.actions.clear()
        self.update_context_menu()

    def update_clippings( self ):
        '''
        React to new clippings found by the QTimer of this class, format the
        display_text if needed, and add the display_text and clipping if they
        do not already exist in the deque and dictionary.
        '''
        new_paste = pyperclip.paste().lstrip().rstrip()
        display_text = new_paste
        if '\n' in display_text:
            display_text = new_paste.split( '\n' )[ 0 ].rstrip() + '...'
        if len( display_text ) >= MAX_DISPLAY_CHAR_COUNT:
            display_text = display_text[ 0:MAX_DISPLAY_CHAR_COUNT ].rstrip() + '...'
        if display_text not in self.clippings:
            self.add_new_clipping( new_paste, display_text )

    def recopy( self, display_text ):
        '''
        Re-insert the full clipping indexed by the passed display_test to the system
        clipboard, and remove it from the clippings.  The newly re-copied clipping
        will be re-added to the list (at the top) the QTimer task of this class.
        '''
        val = self.full_clippings[ display_text ]
        self.clippings.remove( display_text )
        pyperclip.copy( val )

if __name__ == '__main__':
    app = QApplication( sys.argv )
    app.setQuitOnLastWindowClosed(False)

    system_tray = SystemTray( app )
    system_tray.setContextMenu( system_tray.menu )

    app.exec_()
