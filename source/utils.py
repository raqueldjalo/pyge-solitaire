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


def oposite(angle):
    #calculates oposite angle
    #TODO there must be a better way to do this
    if isinstance(angle, str):
        return angle[::-1]
    if angle > 360:
        raise Exception
    return (angle - 180) if ((angle - 180) >= 0) else (angle - 180 + 360)

def fit(inside, outside):
    """
        takes two dimensions (width, height)
        resizes the inside so it fits in the outside
        and returns the size of the inside
    """
    inside_ratio = inside[0] / inside[1]
    outside_ratio = outside[0] / outside[1]

    if inside_ratio > outside_ratio:
        #limit width
        dimension = (outside[0], outside[0] / inside_ratio)
    else:
        #limit height
        dimension = (outside[1], outside[1] * inside_ratio)
        
    return dimension


if __name__ == '__main__':
    import doctest
    doctest.testfile(__file__+'.test')