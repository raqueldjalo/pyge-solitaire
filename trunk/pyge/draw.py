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

"""
Some graphical functions that pyge uses.
"""

from pygame.gfxdraw import aacircle, filled_circle

def circle(surface, pos, radius, color, width=0):
    if width == 0:    
        # we need the aacircle even when the hole is filled
        # because filled circles look like shit
        aacircle(surface, pos[0], pos[1], radius, color)
        filled_circle(surface, pos[0], pos[1], radius, color)
    elif width == 1:
        aacircle(surface, pos[0], pos[1], radius, color)
    else:
        for i in range(1, width):
            aacircle(surface, pos[0], pos[1], radius-i, color)
    return
        
def halo(surface, pos, radius, color, width, outwards=True):
    
    if width == 0:
        width = radius
    
    for i in range(1, width):
        direction = 1 if outwards else -1
        color_difference = (255-(i*(255/width)),)
        circle(surface, pos, radius+(i*direction), color + color_difference, 1)
    return

if __name__ == '__main__':
    import doctest
    doctest.testfile(__file__+'.test')