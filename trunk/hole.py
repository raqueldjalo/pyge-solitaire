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
from utils import *

class Hole:
    
    empty = False
    apos = None
    pos = None #relative
    ver = 0
    possible_move = False
    selected = False
    
    def __init__(self, board, links={}, cord=(), empty=False):
        self.board = board
        self.cord = cord
        self.empty = empty
        
        if len(board.holes) == 0:
            #first hole
            self.pos = (0, 0)
            self.ver = 1
        else:
            self.prev = board.holes[-1]
            board.holes[-1].next = self
        
        #for each link given make sure there is an oposite link in place
        self.links = links
        for angle in links:
            links[angle].add_link(oposite(angle),self)
            
        board.holes.append(self)
        return None
    def add_link(self, angle, hole):
        
        if self == hole:
            raise Exception (self, angle, hole, "something's seriously fucked up")
        
        if angle not in self.links.keys():
            self.links[angle] = hole
            #add a link back
            self.links[angle].add_link(oposite(angle), self)
        
        return self
    def calculate_position(self):
        """
            Calculate the position of all connected nodes
        """
        
        ver = self.ver
        (x, y) = self.pos
        
        for angle in self.links.keys():
            
            linked_hole = self.links[angle]
            if linked_hole.ver < ver:
                try:
                    (xo, yo) = linked_hole.node_offset(oposite(angle))
                except:
                    continue
            
                linked_hole.pos = (x-xo, y-yo)
                linked_hole.ver = ver
                if linked_hole.pos[0] < 0 or linked_hole.pos[1] < 0:
                
                    start_hole = self.board.holes[0]
                    start_hole.pos = (
                        start_hole.pos[0] if linked_hole.pos[0] >= 0 else start_hole.pos[0] - linked_hole.pos[0],
                        start_hole.pos[1] if linked_hole.pos[1] >= 0 else start_hole.pos[1] - linked_hole.pos[1]
                    )
                    start_hole.ver = ver + 1
                    
                    print start_hole.pos, ver
                    
                    return start_hole.calculate_position()
                
                linked_hole.calculate_position()
        
        return self
    def node_offset(self, angle, distance=1):
        #trig comes in useful
        #I have a headache
        #fuck radians!!!
        from math import sin, cos, radians
        if angle >= 0 and angle <= 90:
            a = radians(angle)
            x = sin(a) *  distance
            y = cos(a) * -distance
        elif angle <= 180:
            a = radians(180 - angle)
            x = sin(a) * distance
            y = cos(a) * distance
        elif angle <= 270:
            a = radians(angle - 180)
            x = sin(a) * -distance
            y = cos(a) *  distance
        elif angle <= 360:
            a = radians(180 - (angle - 180))
            x = sin(a) * -distance
            y = cos(a) * -distance
        else:
            raise Exception
        
        return (x, y)
    
    def draw(self, surface):
       
        h = surface.get_height()
        w = surface.get_width()
        
        board = self.board
        
        if not self.pos:
            return
        
        (x, y) = self.pos
        x *= (board.bw / board.width)
        y *= (board.bh / board.height)
        
        self.radius = ((board.bh if board.bh < board.bw else board.bw) / board.width) / 4
        
        self.apos = (int(x+(self.radius*2)+board.offset[0]), int(y+(self.radius*2)+board.offset[1]))
        
        if self.selected and board.highlight_selected:
            color = (255, 80, 0)
            halo(surface, self.apos, self.radius, color, self.radius/2)
            
        elif self.possible_move and board.highlight_moves:
            color = (128, 255, 255)
            halo(surface, self.apos, self.radius, color, self.radius/2, False)
            
        elif self.empty:
            color = (128, 255, 255)
            circle(surface, self.apos, self.radius, color, 1)
            
        if not self.empty:
            color = (128, 255, 255)
            circle(surface, self.apos, self.radius, color)
        
        
        #draw links to other nodes
        if board.show_grid:
            from pygame.font import Font
            vera = Font('Resources\\fonts\\Vera.ttf',10)
            text_surface = vera.render(str(self.cord), True, (255, 255, 255))
            surface.blit(text_surface, (self.apos[0]+self.radius, self.apos[1]+self.radius))

            for n in self.links:
                if self.links[n].apos:
                    self.draw_link(surface, self.links[n])
        
        return self
    def draw_link(self, surface, link):
        from pygame.draw import aaline
        
        #TODO stop line at side of hole
        
        start = self.apos
        end = link.apos
        
        aaline(surface, (100, 50, 50), start, end)
        
        return self
    
    def __repr__(self):
        return str((
            self.cord,
            self.links.keys(),
            self.pos
        ))
    
    def select(self):
        if self.board.selected != None and self.empty == True:
            try:
                self.board.selected.move(self)
            except:
                #basically ignore
                return
        
        if self.empty == False:
            if self.board.selected:
                # If there was a selected we undo highlighting
                # TODO find a better way to do this
                if self.board.selected:
                    for hole in self.board.holes:
                        hole.possible_move = False
                        
                self.board.selected.selected = False
            self.board.selected = self
            self.selected = True
            self.highlight()
        
        return self
    
    def highlight(self):
        """highlight availible moves"""
        
        for i in self.links.keys():
            if self.links[i].empty == False \
                and i in self.links[i].links.keys() \
                and self.links[i].links[i].empty == True:
                
                self.links[i].links[i].possible_move = True
        return self
    
    def toggle(self):
        self.empty = not self.empty
        return self
    
    def move(self, peg):
        if self.empty == True or peg.empty == False:
            raise Exception('foo')
                        
        for i in self.links.keys():
            for j in peg.links.keys():
                if self.links[i] == peg.links[j]:
                    if i == oposite(j) \
                        and self.links[i].empty == False:
                    
                        self.empty = True #moved from
                        self.links[i].empty = True #jumped over
                        peg.empty = False #moved to
                        self.board.history.append((self, self.links[i], peg))
                        print self.board.history
                        return self
                    else:
                        break
        raise Exception('bla bla')

if __name__ == '__main__':
    import doctest
    doctest.testfile(__file__+'.test')