#! /usr/bin/env python
################################################################################
##
## Copyright 2010 Annan Fay Yearian
##
## This file is part of Pyge.
## 
## Pyge is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Pyge is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with Pyge.  If not, see <http://www.gnu.org/licenses/>.
##
################################################################################


from draw import *
from hole import *
from utils import *


class Board(object):
    """
        Base game board
    """
    
    title = "Base"
    
    def __init__(self, size, show_grid, highlight_moves, highlight_selected):
        """
            Initiates the board settings.
            Actual hole generation and positioning is done in Board.build
        """
        
        self.height             = size
        self.width              = size
        self.show_grid          = show_grid
        self.highlight_moves    = highlight_moves
        self.highlight_selected = highlight_selected
        
        self.holes              = []
        self.history            = []
        self.selected           = None
        
        self.build()
        self.position_holes()
        
        
        return None
        
    def build(self):
        pass
    
    def solve(self):
        pass
    
    def position_holes(self):
        """
            Calculates the relative positions for holes
            Positions are relative to the top and left side of the board
            The space between holes is 1
            Start at the initial hole and work outwards
        """
        
        self.holes[0].calculate_position()
        
        return self
    
    def undo(self):
        if len(self.history) > 0:
            #TODO refactor
            movement = self.history.pop()
            movement[0].empty = False
            movement[1].empty = False
            movement[2].empty = True
            movement[0].select()
        return
    
    def add_hole(self, links={}, cord=(), empty=False):
        
        hole = Hole(self, links=links, cord=cord, empty=empty)
            
        #print hole, cord, self.holes
        
        return self

    def draw(self, surface):
        from pygame.draw import rect
        
        #surface dimensions
        w = surface.get_width()
        h = surface.get_height()
        
        padding = 0.05 #decimal percent
        
        #calculate the exact board height
        (self.bw, self.bh) = fit((self.height, self.width), (h, w))
        
        
        #calculate the offsets to centre everything
        self.offset = ((w/2)-(self.bw/2), (h/2)-(self.bh/2))
        
        #draw board outline
        rect(surface, (128, 200, 255), (self.offset[0], self.offset[1], self.bw, self.bh), 5)
        
        #loop round holes drawing each of them
        #print self.holes
        for hole in self.holes:
            hole.draw(surface)
        
        return self
        
    def __repr__(self):
        output = ''
        for hole in self.holes:
            output += 'hole' + str(hole) + ':\t' + str(hole.links.keys()) + '\t' + str(hole.pos)+ '\n'
        return output
        
    def get_hole(self, cord):
        """returns a hole given it's cord or None"""
        
        for hole in self.holes:
            if hole.cord == cord:
                return hole
        return None
        
    def mouse_down(self, event):
        print event
        #loop round all holes
        (x, y) = event.local
        
        for hole in self.holes:
            #check if point clicked is withing radius of hole
            if hole.apos and abs(x - hole.apos[0]) < hole.radius and abs(y - hole.apos[1]) < hole.radius:
                #if it is then toggle
                if event.button == 1:
                    hole.select()
                elif event.button == 2:
                    hole.toggle()
                elif event.button == 3:
                    hole.toggle()
                return
        #no hole found
        
    def mouse_up(self, event):
        #event
        pass
        
    def mouse_move(self, event):
        #event
        pass

class TriangleBoard(Board):
    
    title = "Triangular"
    
    def build(self):
        for y in range(self.height):
            for x in range(y+1):

                links = {}
                
                #link to the left
                if self.get_hole((x-1,y)):
                    links[270] = self.get_hole((x-1,y))
                
                #link up and backward
                if self.get_hole((x-1,y-1)):
                    links[330] = self.get_hole((x-1,y-1))
                    
                #link up and forward
                if self.get_hole((x,y-1)):
                    links[30] = self.get_hole((x,y-1))
                
                        
                if y == (self.height / 2) + 1 and x == (self.width - y) - 1:
                    empty = True
                else:
                    empty = False
                    
                self.add_hole(links=links, cord=(x,y), empty=empty)

class BritishBoard(Board):
    
    title = "British"
    
    def build(self):
        #check to see if the size is legal
        #TODO implament validation in the settings gui
        if (self.width-3)%2 != 0 or (self.height-3)%2 != 0 :
            raise Exception ("Invalid board size")
        
        h = self.height #for brevity
        w = self.width 
        we = (w-3)/2
        he = (h-3)/2
        
        for y in range(h):
            for x in range(w):
                links = {}
                #decide if there should be a node
                if (x>=we and x<w-we) or (y>=he and y<h-he):
                    #decide links for nodes
                    if self.get_hole((x-1,y)):
                        links[270] = self.get_hole((x-1,y))
                    if self.get_hole((x,y-1)):
                        links[0] = self.get_hole((x,y-1))
                        
                    if x == w / 2 and y == h / 2:
                        empty = True
                    else:
                        empty = False
                        
                    self.add_hole(links=links, cord=(x,y), empty=empty)

class EuropeanBoard(Board):
    
    title = "European"
    
    def build(self):

        #check to see if the size is legal
        if self.width%3 != 1 or self.height != self.width:
            raise Exception ("Invalid board size")
        
        h = self.height #for brevity
        w = self.width 
        we = (w-1)/3
        he = (h-1)/3
        
        print we, he
        
        for y in range(h):
            for x in range(w):
                links = {}
                #decide if there should be a node
                if y<= he:
                    margin = we - y
                elif y < self.height - he:
                    margin = 0
                else:
                    margin = we - (we - (y - (h-he))) + 1
                
                print margin
                
                if (x>=margin and x<w-margin):
                    #decide links for nodes
                    if self.get_hole((x-1,y)):
                        links[270] = self.get_hole((x-1,y))
                    if self.get_hole((x,y-1)):
                        links[0] = self.get_hole((x,y-1))
                        
                    if x == w / 2 and y == h / 2:
                        empty = True
                    else:
                        empty = False
                        
                    self.add_hole(links=links, cord=(x,y), empty=empty)
        
class SquareBoard(Board):
    
    title = "Square"
    
    def build(self):
        
        h = self.height #for brevity
        w = self.width 
        
        for y in range(self.height):
            for x in range(self.width):
                links = {}
                
                if x != 0:
                    links[270] = self.holes[-1]
                if y != 0:
                    links[0] = self.holes[-self.width]
                    
                
                if x == w / 2 and y == h / 2:
                    empty = True
                else:
                    empty = False
                    
                self.add_hole(links=links, cord=(x,y), empty=empty)

class DiamondBoard(Board):
    
    title = "Diamond"
    
    def build(self):
        
        h = self.height #for brevity
        w = self.width 
        
        for y in range(h):
            for x in range(w):
                if (x<=(y*2) and y<h/2+1) or (x>=w-1-(h-y-1)*2 and y>=h/2):
                
                    links = {}
                    
                    if self.get_hole((x-1,y)):
                        links[270] = self.get_hole((x-1,y))
                    if self.get_hole((x-1,y-1)):
                        links[0] = self.get_hole((x-1,y-1))
                        
                    if self.get_hole((x,y-1)):
                        links['back up'] = self.get_hole((x,y-1))
                    if self.get_hole((x-2,y-1)):
                        links['front up'] = self.get_hole((x-2,y-1))
                    
                    if x == w / 2 and y == h / 2:
                        empty = True
                    else:
                        empty = False
                        
                    self.add_hole(links=links, cord=(x,y), empty=empty)


if __name__ == '__main__':
    import doctest
    doctest.testfile(__file__+'.test')