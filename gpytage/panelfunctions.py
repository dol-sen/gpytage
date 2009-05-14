#!/usr/bin/env python
#
# GPytage panelfunctions.py module
#
############################################################################
#    Copyright (C) 2008 by Kenneth Prugh                                   #
#    ken69267@gmail.com                                                    #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation under version 2 of the license.          #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                      ``````                                    #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import pygtk; pygtk.require("2.0")
import gtk
import datastore
from datastore import E_NAME, E_DATA, E_EDITABLE, E_PARENT, E_MODIFIED

def get_dragdestdata(treeview, context, x, y, selection, info, etime):
    iter, value = cselected(treeview,x,y)
    model = treeview.get_model()
    if value == True:
        ldata = data
        print"global data=", data
        drop_info = treeview.get_dest_row_at_pos(x,y)
        print "DROP INFO IS:"; print drop_info
        if drop_info:
            path, position = drop_info
            iteri = model.get_iter(path)
            if model.get_value(iteri, E_PARENT):
                if (position == gtk.TREE_VIEW_DROP_BEFORE or position == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE):
                    for row in ldata:
                        model.insert_before(iteri, row[:-1]) #0:4])
                else:
                    for row in reversed(ldata):
                        model.insert_after(iteri, row[:-1]) #0:4])
            else:
                return
            
        else:
            for row in ldata:
                model.append(row[:-1]) # 0:4])
            print 'end of treeview'
        #delete dragged rows
        for row in ldata:
            print row[-1]
            model.remove(model.get_iter(row[-1].get_path()))
        from window import title
        title("* GPytage")
        fileEdited()
        return
    else: # File to File dragging
        # rightpanel -> leftpanel logic goes here.
        ldata = data
        parent = model.get_value(iter,E_PARENT).strip('*')
        oldName = model.get_value(iter, E_NAME).strip('*')
        print "parent = ", parent
        if model.iter_children(iter):#has children [subfiles]
            print "has children"
        else: #doesn't have children
            newName = "*%s" % oldName
            model.set_value(iter, E_NAME, newName)
            model.set_value(iter, E_MODIFIED, True)
            # append the data
            print ldata,"DATA TO APPEND"
            for row in ldata:
                print "row=", row
                datastore.lists[oldName].append(row[:-1]) #0:4])
            #nuke what we moved
            for row in ldata:
                from rightpanel import rightview
                rmodel = rightview.get_model()
                rmodel.remove(rmodel.get_iter(row[-1].get_path()))
            from leftpanel import leftview
            lmodel = leftview.get_model()
            lselection.select_path(lmodel.get_path(lselected[1]))
            fileEdited()


def drag_begin_signal(treeview, dragcontext, *args):
    """ Grab model and data begin dragged """
    #global bmodel
    global data
    global lselection
    global lselected
    from leftpanel import leftview
    lselection = leftview.get_selection()
    lselected = lselection.get_selected()
    data = [] #master container
    #get the selected rows
    model = treeview.get_model()
    rows = treeview.get_selection().get_selected_rows()[1]
    for path in rows: #each line is a path to the row
        print "DRAG_BEGIN_SIGNAL_PATHS:"; print path
        cdata = [] #current data
        iter = model.get_iter(path)
        cdata.append(model.get_value(iter, E_NAME))
        cdata.append(model.get_value(iter, E_DATA))
        cdata.append(model.get_value(iter, E_EDITABLE))
        cdata.append(model.get_value(iter, E_PARENT))
        cdata.append(model.get_value(iter,E_MODIFIED))
        cdata.append(gtk.TreeRowReference(model, path))
        data.append(cdata)
    print "MASTER DATA CONTAINER:"
    print data

def drag_data_delete_signal(*args):
    """ Delete begin signals data """
    print "drag data delete signal"
    

def cselected(treeview, x, y):
    """ Return iter:value from current coordinates """
    try:
        selection = treeview.get_dest_row_at_pos(x,y) #tuple path,dropposition
        model = treeview.get_model()
        iter = model.get_iter(selection[0])
        try:
            value = model.get_value(iter,E_EDITABLE)
        except:
            value = False
        print model.get_value(iter,E_NAME)
        return iter,value
    except TypeError:
        model = treeview.get_model()
        iter = model[-1].iter
        try:
            value = model.get_value(iter,E_EDITABLE)
        except:
            value = False
        return iter,value


def selected(treeview): #helper function
    """ Return iter of currently selected row """
    selection = treeview.get_selection()
    model, iter = selection.get_selected()
    try:
        value = model.get_value(iter, E_EDITABLE)
    except:
        value = False
    return iter, value

def mselected(treeview):
    """ Return model and dictionary of iters:values from currently selected rows """
    selection = treeview.get_selection()
    model, iters = selection.get_selected_rows() #iters == paths
    iterdict = {}
    for i in iters:
        iref = gtk.TreeRowReference(model, i)
        iter = model.get_iter(i)
        try:
            iterdict[iter] = model.get_value(iter, E_EDITABLE)
        except:
            iterdict[iter] = False
    return model, iterdict

def switchListView(widget, drag_context, x, y, timestamp, *args):
    """ Hilights leftview drop target during drag operation """
    from leftpanel import leftview
    import rightpanel
    model = leftview.get_model()
    path = leftview.get_dest_row_at_pos(x, y)
    leftview.expand_row(path[0], True)
    #iter = model.get_iter(path[0])
    treeselection = leftview.get_selection()
    treeselection.select_path(path[0])
