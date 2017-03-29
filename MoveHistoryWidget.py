import math
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from Game import Game

#class MoveHistoryWidget(Gtk.ListBox):
#    def __init__(self):
#        super().__init__()
#        lbr = Gtk.ListBoxRow()
#        lbr.add(Gtk.Label(label="Start"))
#        self.add(lbr)

class MoveHistoryWidget(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.set_size_request(128, 16)

        self.liststore = Gtk.ListStore(str, int)
        self.treeview = Gtk.TreeView(self.liststore)
        self.treeview.append_column(Gtk.TreeViewColumn("History", Gtk.CellRendererText(), text=0))
        self.set_vexpand(True)
        self.add(self.treeview)

        self.update()
    def update(self):
        self.liststore.clear()
        self.liststore.append(list(["Start",0]))
