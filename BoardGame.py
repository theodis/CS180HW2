#!/usr/bin/python
from Morph import Morph
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from BoardWidget import *
from MoveListWidget import MoveListWidget
from MoveHistoryWidget import MoveHistoryWidget

def playedMove(game, move):
    moveList.update()

game = Morph()
game.addMoveCallback(playedMove)
win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)
board = BoardWidget(game)
moveHistory = MoveHistoryWidget()
moveList = MoveListWidget(game)

box = Gtk.Box(spacing=2)
box.pack_start(moveHistory, False, False, 0)
box.pack_start(board, True, True, 0)
box.pack_start(moveList, False, False, 0)
win.add(box)

win.show_all()
Gtk.main()
