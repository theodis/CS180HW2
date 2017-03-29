import math
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from Game import Game

class BoardWidget(Gtk.DrawingArea):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.wtile = GdkPixbuf.Pixbuf.new_from_file("Morph/wtile.png")
        self.btile = GdkPixbuf.Pixbuf.new_from_file("Morph/btile.png")
        self.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_clicked)
        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.pieceMap = {
            "K" : GdkPixbuf.Pixbuf.new_from_file("Morph/bking.svg"),
            "N" : GdkPixbuf.Pixbuf.new_from_file("Morph/bknight.svg"),
            "B" : GdkPixbuf.Pixbuf.new_from_file("Morph/bbishop.svg"),
            "R" : GdkPixbuf.Pixbuf.new_from_file("Morph/brook.svg"),
            "P" : GdkPixbuf.Pixbuf.new_from_file("Morph/bpawn.svg"),
            "k" : GdkPixbuf.Pixbuf.new_from_file("Morph/wking.svg"),
            "n" : GdkPixbuf.Pixbuf.new_from_file("Morph/wknight.svg"),
            "b" : GdkPixbuf.Pixbuf.new_from_file("Morph/wbishop.svg"),
            "r" : GdkPixbuf.Pixbuf.new_from_file("Morph/wrook.svg"),
            "p" : GdkPixbuf.Pixbuf.new_from_file("Morph/wpawn.svg")
        }

        self.board = game.boardState()
        self.set_size_request(16 * self.game.width, 16 * self.game.height)

        self.highlight = []
        self.arrow = []
        
        self.sx = -1
        self.sy = -1

    def on_clicked(self, widget, event):
        bh = self.game.height
        bw = self.game.width

        xoff = 0
        yoff = 0
        width = self.width
        height = self.height

        if width // bw < height // bh:
            tileSize = width // bw
        else:
            tileSize = height // bh

        xoff = (width - tileSize * bw) // 2
        yoff = (height - tileSize * bh) // 2

        cx = (event.x - xoff) // tileSize
        cy = (event.y - yoff) // tileSize

        moved = False
        if(cx >= 0 and cx < bw and cy >= 0 and cy < bh):
            for move in self.highlight:
                if(move[0] == cx and move[1] == cy and (cx != self.sx or cy != self.sy)):
                    self.game.playMove([int(self.sx),int(self.sy),int(cx),int(cy)])
                    self.board = self.game.boardState()
                    self.sx = -1
                    self.sy = -1
                    self.highlight = []
                    self.queue_draw()
                    moved = True
                    break
            if(moved != True):
                moves = self.game.generateMoves()
                self.highlight = [[cx,cy]]
                self.sx = cx
                self.sy = cy
                for move in moves:
                    if(cx == move[0] and cy == move[1]):
                        self.highlight.append([move[2], move[3]])
                self.queue_draw()

    def on_draw(self, wid, cr):
        bh = self.game.height
        bw = self.game.width

        xoff = 0
        yoff = 0
        width = self.width
        height = self.height

        if width // bw < height // bh:
            tileSize = width // bw
        else:
            tileSize = height // bh

        xoff = (width - tileSize * bw) // 2
        yoff = (height - tileSize * bh) // 2

        #draw board
        for y in range(0, bh):
            for x in range(0, bw):
                cr.save()
                cr.translate(xoff + x * tileSize, yoff + y * tileSize)
                cr.scale(tileSize/32,tileSize/32)
                if (x + y % 2) % 2 == 0:
                    Gdk.cairo_set_source_pixbuf(cr, self.wtile, 0, 0)
                else:
                    Gdk.cairo_set_source_pixbuf(cr, self.btile, 0, 0)
                cr.paint()

                #draw piece on tile if there is one
                if self.board[y][x] in self.pieceMap.keys():
                    pix = self.pieceMap[self.board[y][x]]
                    cr.scale(32/pix.get_width(),32/pix.get_height())
                    Gdk.cairo_set_source_pixbuf(cr, pix, 0, 0)
                    cr.paint()

                cr.restore()

        #draw highlights
        cr.set_line_width(3)
        cr.set_source_rgb(255,0,0)
        for loc in self.highlight:
            x = loc[0] * tileSize + xoff
            y = loc[1] * tileSize + yoff
            cr.rectangle(x,y,tileSize,tileSize)
            cr.stroke()

        #draw arrows
        for loc in self.arrow:
            x1 = loc[0] * tileSize + xoff + tileSize // 2
            y1 = loc[1] * tileSize + yoff + tileSize // 2
            x2 = loc[2] * tileSize + xoff + tileSize // 2
            y2 = loc[3] * tileSize + yoff + tileSize // 2

            #build vector for arrow side
            vx = x2 - x1
            vy = y2 - y1
            vlen = math.sqrt(vx * vx + vy * vy)
            vx /= vlen
            vy /= vlen
            vx *= tileSize / 2
            vy *= tileSize / 2
            angle = math.pi * 4 / 5
            lx = vx * math.cos(angle) - vy * math.sin(angle)
            ly = vx * math.sin(angle) + vy * math.cos(angle)
            rx = vx * math.cos(-angle) - vy * math.sin(-angle)
            ry = vx * math.sin(-angle) + vy * math.cos(-angle)

            #draw main line
            cr.move_to(x1,y1)
            cr.line_to(x2,y2)
            cr.stroke()

            #draw left side
            cr.move_to(x2,y2)
            cr.line_to(x2+lx,y2+ly)
            cr.stroke()

            #draw right side
            cr.move_to(x2,y2)
            cr.line_to(x2+rx,y2+ry)
            cr.stroke()

    @property
    def width(self):
        return self.get_allocation().width

    @property
    def height(self):
        return self.get_allocation().height
