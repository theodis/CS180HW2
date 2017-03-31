import math
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from Classes.Game import Game

class MoveListWidget(Gtk.ScrolledWindow):
    def __init__(self, game):
        super().__init__()
        self.set_size_request(128, 16)

        self.liststore = Gtk.ListStore(str, int)
        self.treeview = Gtk.TreeView(self.liststore)
        self.treeview.append_column(Gtk.TreeViewColumn("Possible Moves", Gtk.CellRendererText(), text=0))
        self.set_vexpand(True)
        self.add(self.treeview)

        self.game = game
        self.update()
    def update(self):
        self.liststore.clear()
        self.moves = self.game.generateMoves()
        for move in self.moves:
            self.liststore.append(list([str(move),0]))
