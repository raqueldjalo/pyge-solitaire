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

from optparse import OptionParser
from gui import PygeShell
import sys, os


# we need cwd to be the program folder
# we can change it with chdir however
# __file__ is unset... huh!
# so we get utils.__file__ and use it.... 

from utils import __file__
if 'exe' in __file__:
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
else:
    os.chdir(os.path.dirname(__file__))
    

#log = __file__
#open('C:\\Program Files\\Pyge\\log.txt', 'w+').write(log)

def main():
    """
        Takes care of optional command line parameters and initiates the game
    """
    
    #set up command line options
    parser = OptionParser()
    
    #defaults are None because we want to use saved settings unless these are specifically set
    parser.add_option("-s", "--size",          dest="size",          help="size of board",       metavar="SIZE",       default=None)
    parser.add_option("-t", "--style",         dest="style",         help="style of board",      metavar="STYLE",      default=None)
    parser.add_option("-x", "--screen-width",  dest="screen_width",  help="game screen width",   metavar="WIDTH",      default=None)
    parser.add_option("-y", "--screen-height", dest="screen_height", help="game screen height",  metavar="HEIGHT",     default=None)
    parser.add_option("-r", "--frame-rate",    dest="frame_rate",    help="game framerate",      metavar="FRAMERATE",  default=None)

    (options, args) = parser.parse_args()
    
    shell = PygeShell(
        width=options.screen_width,
        height=options.screen_height,
        board_size=int(options.size) if options.size else options.size,
        board_style=options.style,
        frame_rate=int(options.frame_rate) if options.frame_rate else options.frame_rate
    )
    shell.run()


if __name__ == '__main__':
    #the file is being run directly and not imported
    
    main()
    


if __name__ == '__main__':
    import doctest
    doctest.testfile(__file__+'.test')