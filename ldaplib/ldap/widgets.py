## ldap/widgets.py - GTK widgets for LDAP
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

import sys, re, string, ldap, _gtk
import connection, entry
from gtk import *
from ldap import LDAPError, canonical_dn


########################################################## GtkLDAPError ########

class GtkLDAPError(LDAPError):
    """Widgets raise this exception."""
    def __init__(self, desc):
        LDAPError.__init__(self, desc)


##################################################### GtkLDAPClassEntry ########

class GtkLDAPClassEntry(GtkCombo):
    """Simple widget to select an objectClass from a list.

       This widget can automagically update a GtkLDAPAttributeEntry widget
       every time a new class is selected, just set the attribute entry with
       the set_attribute_entry method.
    """
    def __init__(self, ocd):
        GtkCombo.__init__(self)
        self.ocd = ocd
        self.set_popdown_strings(ocd.keys())
        #self.menu = GtkMenu()
        #self.menu.set_title('objectClass entry')
        #self.menu.show()
        #for k in ocd.keys():
        #    child = GtkMenuItem(k); child.show()
        #    child.connect('activate-item', self.__activate_item, self)
        #    self.menu.append(child)
        #self.set_menu(self.menu)
        #self.attr_entry = None
        
    def __activate_item(child, self):
        print child, self
 
    def set_attribute_entry(self, entry):
        self.attr_entry = entry
        self.attr_entry.update()

    
        


################################################ the GtkLDAPEntry class ########

## class GtkLDAPEntry(GtkVBox):
##     "Rapresents a new LDAP directory entry, lets the user modify it."

##     def __init__(self, oclist):
##         GtkVBox.__init__(self)
##         self.oclist = oclist

##         table = GtkTable(2, 2, 0)
##         table.set_col_spacings(4)
##         table.set_row_spacings(4)
##         table.set_border_width(4)
##         table.show()
        
##         # build the objectClass selector
##         l = GtkLabel('objectClass'); l.show()
##         menu = GtkMenu()
##         menu.set_title('objectClass selector')
##         menu.show()
##         for k in oclist.keys():
##             child = GtkMenuItem(k); child.show()
##             menu.append(child)
##         self.ocselector = GtkOptionMenu()
##         self.ocselector.set_menu(menu)
##         self.ocselector.show()
##         table.attach(l, 0,1, 0,1, xoptions=FILL, yoptions=FILL)
##         table.attach(self.ocselector, 1,2, 0,1,
##                      xoptions=FILL+EXPAND, yoptions=FILL)

##         # build the attribute selector
##         l = GtkLabel('attribute'); l.show()
##         child = GtkMenuItem(""); child.show()
##         menu.append(child)
##         self.attrselector = GtkOptionMenu()
##         self.attrselector.set_menu(menu)
##         self.attrselector.show()
##         table.attach(l, 0,1, 1,2, xoptions=FILL, yoptions=FILL)
##         table.attach(self.attrselector, 1,2, 1,2,
##                      xoptions=FILL+EXPAND, yoptions=FILL)
        
##         # build the clist with the attribute values
##         self.attrlist = GtkCList(2, ['Attribute', 'Value'])
##         ctree.set_column_auto_resize(0, TRUE)
##         ctree.set_column_auto_resize(1, TRUE)
##         self.attrlist.show()

##         hbox = GtkHBox()
##         hbox.show()
##         hbox.pack_start(self.attrlist)
##         hbox.pack_start(table)
##         self.pack_start(hbox)

##     def set_data(self, data):
##         """Initialize the widget with data taken from the data dictionary.
##            The data dictionary entries keys are the LDAP attribute names,
##            the values are lists of attribute values (LDAP supports multiple
##            attributes with the same name.)"""
        
##         # clear the clist and the attribute menu (i.e., create a new menu)
##         self.attrlist.freeze(); self.attrlist.clear()
##         menu = GtkMenu(); menu.show()
##         menu.set_title('attribute selector')
##         self.attrselector.set_menu(menu)
        
##         # locate the distinguished name and insert it
##         v = data['dn']
##         self.attrlist.insert(0, ['dn', v])

##         # locate and insert the objectClasses (and builds the menu used in
##         # the attribute selector, much simplier to generate it here)
##         row = 1
##         a = data['objectClass']
##         for v in a:
##             self.attrlist.insert(row, ['objectClass', v])
##             row = row + 1
##             #for attr in self.oclist[v]

##         # insert all the other attributes 
##         for k in data.keys():
##             if k == 'dn' or k == 'objectClass': continue
##             for v in data[k]:
##                 self.attrlist.insert(row, [k, v])
##                 row = row + 1
        
        
        

######################################## the GtkLDAPDirectoryTree class ########

class GtkLDAPDirectoryTree(GtkCTree):
    """Rapresents an LDAP directory tree as a GtkCTree."""

    def __init__(self, connection, titles=None):
        if titles == None: titles = ['Info', 'Node', 'Value']
        self.__connection = connection
        self.__cols = len(titles)
        GtkCTree.__init__(self, self.__cols, 1, titles)

        self.base = connection.base
        self.use_rdn = 1
        self.search_default = 'objectclass=*'
        self.color_dn = self.get_colormap().alloc('black')
        self.color_dn_modified = self.get_colormap().alloc('red')
        self.color_dn_removed = self.get_colormap().alloc('grey')
        self.color_data = self.get_colormap().alloc('blue')
        self.color_data_modified = self.get_colormap().alloc('red')
        self.roots = []
        
        self.set_indent(8)
        self.set_column_auto_resize(1, TRUE)
        self.set_column_visibility(0, FALSE)

        self.expand_id = self.connect('tree-expand', self.__expand)
        self.collapse_id = self.connect('tree-collapse', self.__collapse)
        
        if self.base != None: self.set_browse_base(self.base)

    def __fill(self, node, entry):
        """Fill a node with information gathered from the LDAPEntry."""
        for key in entry.keys():
            for s in entry[key]:
                n = self.insert_node(node, None, [key, key, s], 0,
                                     None, None, None, None, TRUE, FALSE)
                self.node_set_foreground(n, self.color_data)
                self.node_set_row_data(n, entry)
        
    def __expand(self, tree, node):
        """Takes a GtkCTree and a node rapresenting a distinguished name and
           add to the tree the nodes rapresenting a one level browse and the
           leafs rapresenting all the attributes of the node.
        """
        base = tree.node_get_row_data(node)
        
        # grab dn from node text and search LDAP directory (but only
        # if the data has not already been gathered)
        if len(base.childrens) == 0: childs = base.browse(self.search_default)
        else: return

        # now add a non-leaf node for every children
        tree.freeze()
        for child in childs.values():
            if self.use_rdn: rdn = child.rdn
            else: rdn = child.dn
            cn = tree.insert_node(node, None, ['dn', rdn, ''], 0,
                                       None, None, None, None, FALSE, FALSE)
            self.__fill(cn, child)
            child.__gtk_expanded = 0
            tree.node_set_row_data(cn, child)
        tree.thaw()
        
    def __collapse(self, tree, node):
        """Collapse a tree node. 

           At now it does nothing, because we cache entry childrens and
           attributes. 
        """
        base = tree.node_get_row_data(node)
        tree.freeze()
        tree.thaw()
        
    def __check_base(self, dn):
        """Check self.base and dn and raise exception if are both None."""
        if dn == None and self.base == None:
            raise LDAPError, ({'desc':'base not set'},)
        elif dn == None:
            dn = self.base
        else:
            self.base = dn
        return dn

    def __recurse_post_2(self, starting_node, func1, func2, *args):
        """Recurse tree applying 2 different functions.

           This method does a recursive scan of the tree and applies two
           different functions: one one the non-leaf nodes and one on the
           leafs. The argument array is passed inalterated to both functions.
        """
        if starting_node.is_leaf:
            apply(func2, (self, starting_node) + args)
        else:
            for child in starting_node.children:
                apply(GtkLDAPDirectoryTree.__recurse_post_2,
                      (self, child, func1, func2) + args)
            apply(func1, (self, starting_node) + args)
            
    def set_search_base(self, dn=None, search='cn=*'):
        """Search the given dn and add found root nodes to the tree."""
        dn = self.__check_base(dn)
        nn = self.__connection.search(search, dn, ldap.SCOPE_SUBTREE)
        self.freeze() ; self.clear()
        self.roots = []
        for n in nn:
            node = self.insert_node(None, None, ['dn', n.dn, ''], 0,
                                    None, None, None, None, FALSE, FALSE)
            self.__fill(node, n)
            self.node_set_row_data(node, n)
            self.roots.append(node)
        self.thaw()
    
    def set_browse_base(self, dn=None):
        """Browse the given dn and add the only root node to the tree."""
        dn = self.__check_base(dn)
        base = self.__connection.root(dn)
        self.freeze() ; self.clear()
        basen = self.insert_node(None, None, ['dn', dn, ''], 0,
                               None, None, None, None, FALSE, FALSE)
        self.__fill(basen, base)
        self.node_set_row_data(basen, base)
        self.roots = [basen]
        self.thaw()

    def node_get_ldap_data(self, node):
        """Get node type and value (can be LDAP dn or plain attribute.)

           Return tuple formed of node type and value (note that when the
           node is of type dn, the fully qualified value is returned, not
           the reduced one.)
        """
        entry = self.node_get_row_data(node)
        k = self.node_get_text(node, 0)
        if k == 'dn': return ('dn', entry.dn)
        else: return (k, self.node_get_text(node, 2))

    def node_set_ldap_data(self, node, value):
        """Set LDAP data. Multiple attributes are treated correctly.

           If the node is a non-dn one, simply set the new data and colour
           the node in the `changed' color. If the node is a dn one, returns
           an error and leave it as it is.
        """
        entry = self.node_get_row_data(node)
        k = self.node_get_text(node, 0)
        old = self.node_get_text(node, 2)
        if value == old: return 0
        elif k == 'dn': return -1
        else:
            entry.replace(k, old, value)
            self.node_set_text(node, 2, value)
            self.node_set_foreground(node, self.color_data_modified)
            return 1

    def node_add_ldap_data(self, node, key, value):
        """Set LDAP by creating a new node.

           Node should be a dn one. A new sub-node is added and its attribute
           name and value are set respectively to key and value.
        """
        if self.node_get_text(node, 0) != 'dn':
            raise GtkLDAPError('not a dn node')
        entry = self.node_get_row_data(node)
        n = self.insert_node(node, None, [key, key, value], 0,
                             None, None, None, None, FALSE, TRUE)
        self.node_set_foreground(n, self.color_data)
        self.node_set_row_data(n, entry)       
        entry.set(key, value)

    def node_remove_ldap_data(self, node, key, value):
        """Remove an LDAP entry both from the tree and from the directory.

           Note that if the node corresponds to a dn, the entire entry is
           removed from the directory.
        """
        entry = self.node_get_row_data(node)
        if self.node_get_text(node, 0) == 'dn':
            entry.die()
            self.node_set_foreground(node, self.color_dn_removed)
        else:
            entry.delete(key, value)
            if node.parent:
                self.node_set_foreground(node.parent, self.color_dn_modified)
            self.remove_node(node)
        
    def node_add_ldap_entry(self, node, rdn):
        """Add new node to the tree."""
        entry = self.node_get_row_data(node)
        dn = canonical_dn(rdn, entry.dn)
        
    def node_commit_ldap_data(self, node):
        """Recursively commit entries to the direcory.

           This method also reset the color of the data nodes to the unchanged
           data status. If the node is not a dn one raise an exception.
        """
        def func_leaf(tree, node):
            tree.node_set_foreground(node, tree.color_data)
        def func_node(tree, node):
            entry = tree.node_get_row_data(node)
            entry.commit()
            tree.node_set_foreground(node, tree.color_dn)
        if self.node_get_text(node, 0) != 'dn':
            raise GtkLDAPError('not a dn node')
        else:
            self.__recurse_post_2(node, func_node, func_leaf) 




