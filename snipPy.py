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
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QSystemTrayIcon,
    QMenu,
    QAction,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import pyperclip

# In order to preserve the order of the system clipboard, a deque is used.  However,
# in order to prevent long lines of text in the GUI, we truncate all clippings if
# they are greater in length than MAX_DISPLAY_CHAR_COUNT.  Since the deque can only
# contain these truncated strings, a dictionary is maintained in order to provide a
# mapping between such truncated display_text and the actual clipping from the system
# clipboard.
#
# CLIPPINGS_MAX_LEN indicates the maximum depth of the deque.
MAX_DISPLAY_CHAR_COUNT = 55
CLIPPINGS_MAX_LEN = 30
clippings = deque()
fullClippings = {}

class ClippingsListWidget( QListWidget ):
    '''
    Class for reacting to GUI keyclicks on entries in the QListWidget.

    The item text which is clicked is used as the key for lookup into the master
    dictionary of display_test to clippings.
    '''
    #pylint: disable=invalid-name
    def Clicked( self, item ):
        '''
        React to clicks on entries in the QListWidget.
        '''
        if str( item.text() ):
            val = fullClippings[ str( item.text() ) ]
            clippings.remove( str( item.text() ) )
            # The newly re-copied clipping will be re-added to the list (at the top)
            # the QTimer task of MainWindow.
            pyperclip.copy( val )

class MainWindow( QMainWindow ):
    '''
    Class for the main GUI window.

    This class contains a timer which polls the system cliboard every 200ms looking
    for new clipboard entries.  If a new entry is found, it is added to the deque and
    dictionary, and a (sometimes) truncated version of the clipped string is printed
    in the GUI for use later.
    '''
    def __init__( self, *args, **kwargs ):
        super( MainWindow, self ).__init__( *args, **kwargs )
        self.setWindowTitle( 'Clipboard' )
        self.setFixedWidth( 400 )
        self.clippings_widget = ClippingsListWidget()
        self.clippings_widget.setFixedWidth( 400 )

        for _ in range( CLIPPINGS_MAX_LEN ):
            self.clippings_widget.addItem( '' )

        self.clippings_widget.itemClicked.connect( self.clippings_widget.Clicked )
        self.clippings_widget.setSpacing( 4 )
        self.clippings_widget.setWordWrap( False )
        self.setCentralWidget( self.clippings_widget )
        self.resize( 400, 500 )

        self.timer = QTimer()
        self.timer.setInterval( 200 )
        self.timer.timeout.connect( self.update_clippings )
        self.timer.start()

        self.show()

    def show_or_hide( self ):
        '''
        Hide or show the main window, based on the value of self.visible.  This is
        essentially just a toggle.
        '''
        if not self.isVisible():
            self.show()
            self.raise_()
        else:
            self.hide()

    def create_clipping_widgets( self ):
        '''
        Populate the list of clippings.  The first clipping is also the current
        contents of the system clipboard, and are so indicated by a checkmark icon.
        All other clippings simply have a dash to visually itemize them.
        '''
        for i, clip in enumerate( clippings ):
            widget = QListWidgetItem( self.clippings_widget )
            widget.setText( clip )
            if not i:
                widget.setIcon( QIcon( 'images/firstClipping.png' ) )
            else:
                widget.setIcon( QIcon( 'images/clipping.png' ) )

    def add_new_clipping( self, clipping, display_text ):
        '''
        Add the passed clipping into the dictionary mapping of display_text to
        clippings, and add the display_text to the deque.

        Maintain the size of the deque and dictionary based on CLIPPINGS_MAX_LEN.

        Refresh the GUI so that the current contents of the deque are shown.
        '''
        if len( clippings ) == CLIPPINGS_MAX_LEN:
            key = clippings.pop()
            if key in fullClippings:
                del fullClippings[ key ]
        clippings.appendleft( display_text )
        fullClippings[ display_text ] = clipping
        self.clippings_widget.clear()
        self.create_clipping_widgets()

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
        if display_text not in clippings:
            self.add_new_clipping( new_paste, display_text )


app = QApplication( sys.argv )
app.setQuitOnLastWindowClosed(False)

window = MainWindow()
system_tray = QSystemTrayIcon()
system_tray.setIcon( QIcon( 'images/trayIcon.png' ) )
system_tray.setVisible( True )

menu = QMenu()

show_hide_action = QAction( 'Toggle Clipboard' )
show_hide_action.triggered.connect( window.show_or_hide )
menu.addAction( show_hide_action )

menu.addSeparator()

quit_action = QAction( 'Quit' )
quit_action.triggered.connect( app.quit )
menu.addAction( quit_action )

system_tray.setContextMenu( menu )

app.exec_()
sys.exit()
