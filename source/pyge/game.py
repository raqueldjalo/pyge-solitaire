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

"""

import board

class Pyge:
    """
        Pronounced Pyj
        "py" as in "pie" and "j" as in "jack"
    """
    
    def __init__(self, settings):
        
        
        # TODO Pyge class should handle all drawing
        # leaving board and hole to do none graphical stuff only
        
        self.board_styles = board.Board.__subclasses__()
        self.settings = settings
        
        return None
    
    def create_game(self):
    
        size                = self.settings.get('board_size')
        style               = self.settings.get('board_style')
        highlight_selected  = self.settings.get('highlight_selected')
        highlight_moves     = self.settings.get('highlight_moves')
        show_grid           = self.settings.get('show_grid')
        
        for board in self.board_styles:
            if board.title == style:
                board_class = board
        
        self.board = board_class(size=size, show_grid=show_grid, highlight_moves=highlight_moves, highlight_selected=highlight_selected)
        
        return self

if __name__ == '__main__':
    import doctest
    doctest.testfile(__file__+'.test')