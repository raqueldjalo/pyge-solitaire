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
    Theme for Pyge using Albow
    I must say that theming in Albow is FUCKING CONFUSING!!!
"""

#--------------------------------------------------------------------------------
#
#   Theme
#
#--------------------------------------------------------------------------------

from albow.theme import root, Theme

header_font = 'BENNB___.TTF'
body_font = 'POP.1280.TTF'

#root.font = (13, body_font)
root.Button.font = (16, body_font)
root.TextScreen.heading_font = (24, header_font)
root.TextScreen.button_font = (16, body_font)
root.TabPanel.tab_font = (16, body_font)

root.MenuScreen = Theme('MenuScreen')
root.MenuScreen.font = (60, header_font)

root.Error = Theme('Error')
root.Error.font = (20, body_font)
root.Error.fg_color = (255, 0, 0)


if __name__ == '__main__':
    import doctest
    doctest.testfile(__file__+'.test')