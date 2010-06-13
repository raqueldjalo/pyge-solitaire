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

#--------------------------------------------------------------------------------
#
#   Imports
#
#--------------------------------------------------------------------------------

import pygame
from pygame.locals import *

from albow.widget import Widget
from albow.controls import Label, Button, AttrRef, CheckBox
from albow.layout import Column, Grid
from albow.shell import Shell
from albow.screen import Screen

from albow.theme import FontProperty

from theme import root
from extensions import *

try:
    import json
except:
    import simplejson as json

#--------------------------------------------------------------------------------
#
#   Menu
#
#--------------------------------------------------------------------------------

class MenuScreen(Screen):
    
    f1 = FontProperty('font')
    
    def __init__(self, shell):
        Screen.__init__(self, shell)
        self.shell = shell
        title = Label("Pyge", font = self.f1)
        def screen_button(text, screen):
            return Button(text, action = lambda: shell.show_screen(screen))
        
        menu = Column(
            [
                screen_button("Play", shell.board_screen),
                screen_button("Help", shell.help_screen),
                screen_button("Settings", shell.settings_screen),
                Button("Quit", shell.quit),
            ],
            align = 'l'
        )
        contents = Column(
            [
                title,
                menu,
            ],
            align = 'l',
            spacing = 20
        )
        self.add_centered(contents)
    
    def quit(self):
        sys.exit(0)

#--------------------------------------------------------------------------------
#
#   Settings
#
#--------------------------------------------------------------------------------

class SettingsScreen(Screen):

    def __init__(self, shell):
    
        Screen.__init__(self, shell)
        self.shell = shell #so save can use
        
        def setting(name):
            return AttrRef(self.shell.settings, name)
        
        self.size_field = IntField(ref = setting('board_size'))
        self.size_field.enter_action = self.save
        
        board_styles = [(b.title,b.title) for b in shell.pyge.board_styles]
        style_name = setting('board_style')
        self.style_choices = SelectField(board_styles, style_name)
        self.style_choices.enter_action = self.save
        
        self.highlights = Grid([
            [CheckBox(ref = setting('highlight_selected')), Label("Selected Peg")],
            [CheckBox(ref = setting('highlight_moves')), Label("Possible Moves")],
        ])
        
        self.show_grid = CheckBox(ref = setting('show_grid'))
        
        grid = Grid([
            [Label("Board Size"), self.size_field],
            [Label("Board Style"), self.style_choices],
            [Label("Highlight"), self.highlights],
            [Label("Show Grid"), self.show_grid],
        ])
        
        back = Button("Menu", action = shell.show_menu)
        save = Button("Save", action = self.save)
        
        contents = Column([grid, save, back])
        self.add_centered(contents)
        
        self.size_field.focus()
        
    def save(self):
        
        # TODO change settings without destroying current game
        self.shell.settings.save()
        game_created = self.shell.create_game()
        if game_created:
            self.shell.create_screens()
            self.shell.show_menu()

#--------------------------------------------------------------------------------
#
#   Board
#
#--------------------------------------------------------------------------------

class BoardScreen(Screen):

    def __init__(self, shell):
        
        Screen.__init__(self, shell)
        
        self.pyge = shell.pyge
        
        self.rect = shell.rect
        w, h = self.size
        
        bc = BoardContainer(self)
        self.add_centered(bc)
        
        #add buttons
        menu_button = Button("Menu", action = self.go_back)
        menu_button.rect.center = (w/1.5, h - 20)
        self.add(menu_button)
        
        undo_button = Button("Undo", action = self.undo)
        undo_button.rect.center = (w/3, h - 20)
        self.add(undo_button)
        
    def draw(self, surface):
        #self.pyge.board.draw(surface)
        return
        
    def go_back(self):
        self.parent.show_menu()
        
    def undo(self):
        self.pyge.board.undo()

class BoardContainer(Widget):

    def __init__(self, board_screen):
        self.pyge = board_screen.pyge
        Widget.__init__(self)
        self.rect = board_screen.rect.inflate(-100, -100)
        
    def draw(self, surface):
        try:
            self.pyge.board.draw(surface)
        except:
            self.parent.go_back()
        return
    
    def mouse_down(self, event):
        self.pyge.board.mouse_down(event)
        
    def mouse_up(self, event):
        self.pyge.board.mouse_up(event)
        
    def mouse_move(self, event):
        self.pyge.board.mouse_move(event)
        
    def begin_frame(self):
        self.invalidate()

#--------------------------------------------------------------------------------
#
#   Shell
#
#--------------------------------------------------------------------------------

from game import Pyge

class PygeShell(Shell, ExtendedRootWidget):
    
    current_screen_name = None
    
    def __init__(self, **kwargs):
    
        pygame.init()
        
        self.settings = Settings(**kwargs)
        
        pygame.display.set_caption('Pyge')
        
        screen_info = pygame.display.Info()
        
        self.set_icon()
        
        display = pygame.display.set_mode(self.settings.get('window_res'), pygame.RESIZABLE)
        #pygame.display.toggle_fullscreen()
        
        Shell.__init__(self, display)
        
        
        self.pyge = Pyge(self.settings)
        self.create_screens()
        self.create_game()
        
        self.set_timer(self.settings.get('frame_rate'))
        
        
    def create_screens(self):
        
        self.help_screen = CenteredTextScreen(self, "help.txt")
        self.settings_screen = SettingsScreen(self)
        self.board_screen = BoardScreen(self)
        self.menu_screen = MenuScreen(self) # Do this last
        
        csn = self.current_screen_name
        self.show_screen(self.__dict__[csn] if csn else self.menu_screen)
        
    def create_game(self):
        try:
            self.pyge.create_game()
            return True
        except Exception, e:
            self.show_screen(self.settings_screen)
            
            error_message = Error("Error: " + str(e))
            error_message.rect.center = (self.size[0]/2, 20)
            
            self.current_screen.add(error_message)
            
            return False
        
    def set_icon(self):
        
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
        
    def show_menu(self):
        self.show_screen(self.menu_screen)
        
    def show_screen(self, screen):
        
        #TODO Better way?
        for screen_name in self.__dict__:
            if screen_name != '_rect' and self.__dict__[screen_name] == screen:
                self.current_screen_name = screen_name
                break
        
        print self.current_screen_name
        
        Shell.show_screen(self, screen)
        
    def event_handler(self, event):
        
        if event.type == pygame.VIDEORESIZE :
            
            self.settings.window_res = event.size
            
            display = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            
            self.size = event.size
            self.menu_screen.size = event.size
            
            self.create_screens()
        
    def dispatch_key(self, name, event):
        
        #TODO Fix this mofo hack
        if self.visible and event.type == pygame.VIDEORESIZE:
            self.call_handler(name, event)
        else:
            ExtendedRootWidget.dispatch_key(self, name, event)

#--------------------------------------------------------------------------------

class Settings(object):
    #this would be the settings model except the shell needs 
    #to use settings before the settings screen can be initiated
    
    settings_file = "settings.json"
    
    #defaults
    board_size = 7
    board_style = 'British'
    window_pos = (0,0)
    window_res = (800, 493) #golden ratio ^_^,
    frame_rate = 50
    highlight_selected = True
    highlight_moves = True
    show_grid = False
    
    
    def __init__(self, **kwargs):
        
        self.load()
        self.override(**kwargs)
        
    def load(self):
        
        try:
            #if we already have a settings file use it
            settings = json.load(open(self.settings_file))
            for s in settings:
                self.__setattr__(s, settings[s])
            
        except:
            #create a new settings file with defaults
            #print 'new settings file'
            self.save()
        return self
        
    def override(self, **kwargs):
        
        for key in kwargs:
            if kwargs[key] != None:
                self.__setattr__(key, kwargs[key])
                #print (key, kwargs[key])
        #self.save()
        return self
        
    def save(self):
    
        json.dump(self.__dict__, open(self.settings_file, 'wb'))
        
        return self
    
    def get(self, name):
        return getattr(self, name)
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        self.save()

    def __getattr__(self, name):
        if name not in self.__dict__:
            setattr(self, name, None)
        return self.__dict__[name]


if __name__ == '__main__':
    import doctest
    doctest.testfile(__file__+'.test')