## widget_test.py - test the various classes defined in the Gtk/ldap module
## Copyright (C) 2000  Federico Di Gregorio <fog@debian.org>
## Copyright (C) 2000  MIXAD LIVE [http://www.mixadlive.com]
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 2 of the License, or
##   (at your option) any later version.
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.
##
##   You should have received a copy of the GNU General Public License
##   along with this program; if not, write to the Free Software
##   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
## -*- Mode: python -*-

import sys, _gtk
import ldap, ldap.connection
from ldap import LDAPError
from ldap.widgets import *
from gtk import *

if len(sys.argv) != 3:
    print "usage: %s host base_dn" % sys.argv[0]
    sys.exit()

# create a connection to the ldap directory without authenticating
c = ldap.connection.LDAPConnection(sys.argv[1])

# set the base dn for following search and get root object
c.base = sys.argv[2]

# build the gui
_gtk.gtk_init()
win = GtkWindow()
win.set_title('GtkLDAP test')
win.connect("destroy", mainquit)
win.connect("delete_event", mainquit)

tree = GtkLDAPDirectoryTree(c)
tree.set_search_base(sys.argv[2], '(!(dn=*))')
tree.show()

## def clicked(button, tree):
##     tree.ldap_commit()
    
## button = GtkButton('Save')
## button.connect('clicked', clicked, tree)
## button.show()

## ocs = ldap_utils.load_all_d(sys.argv[2])
## dirent = GtkLDAPDirectoryEntry(ocs)
## dirent.show()
    
vbox = GtkVBox()
vbox.pack_start(tree)
## vbox.pack_start(dirent)
## vbox.pack_start(button)
vbox.show()

win.add(vbox)
win.show()
mainloop()





