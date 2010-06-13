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
    Extensions to Albow
    Because some things are crap and others don't exist...
    Most of the code in ExtendedRootWidget and CenteredTextScreen are copied from albow
"""


#--------------------------------------------------------------------------------
#
#   Albow Extensions
#
#--------------------------------------------------------------------------------

##WTF!!! there isn't a native drop down box field.......

from albow.fields import Field
from albow.menu import Menu
from albow import root
import pygame
from pygame.locals import *
from albow import root
from albow.root import *

class SelectMenu(Menu):
    """
        The menu used by the Select Field type
    """

    def invoke_item(self, i):
        get_focus().handle_command('handler', i)

class SelectField(Field):
    
    def handler(self, value):
        self.set_value(self.options[value][1])
        
    def __init__(self, options, value = None, width = None, **kwds):
        
        if value:
            self.value = value.get()
            self.ref = value
        else:
            self.value = options[0][1]
        
        self.menu = SelectMenu('-'*100, options, **kwds)
        
        self.options = options
        
        Field.__init__(self, width, **kwds)
    
    def mouse_down(self, event):
        mx = event.local[0]
        font = self.font
        x = 0
        
        text = " %s " % self.menu.title
        w = font.size(text)[0]
        if x <= mx < x + w:
            self.focus()
            self.show_menu(self.menu, x)
    
    def show_menu(self, menu, x):
        self._hilited_menu = menu
        try:
            i = menu.present(self, (x, self.height))
        finally:
            self._hilited_menu = None
        menu.invoke_item(i)
        
    def key_down(self, event):
        self.show_menu(self.menu, 0)
            
        Field.key_down(self, event)

## Just because I can

class NumField(Field):
    def key_down(self, event):
        if event.key == 273:
            self.value += 1
        elif event.key == 274:
            self.value -= 1
            
        Field.key_down(self, event)
    
class IntField(NumField):
    type = int

class FloatField(NumField):
    type = float

##The default text screen puts everything to the top left of the screen...

from albow.resource import get_text
from albow.vectors import add, maximum
from albow.text_screen import Page, TextScreen
from albow.controls import Button
from albow.screen import Screen

class CenteredTextScreen(TextScreen):
    
    #because of how the original is written we need to override the entire init and draw methods
    
    def __init__(self, shell, filename, **kwds):
        
        text = get_text(filename)
        text_pages = text.split("\nPAGE\n")
        pages = []
        page_size = (0, 0)
        for text_page in text_pages:
            lines = text_page.strip().split("\n")
            page = Page(self, lines[0], lines[1:])
            pages.append(page)
            page_size = maximum(page_size, page.size)
        self.pages = pages
        bf = self.button_font
        b1 = Button("Prev Page", font = bf, action = self.prev_page)
        b2 = Button("Menu", font = bf, action = self.go_back)
        b3 = Button("Next Page", font = bf, action = self.next_page)
        
        self.b = ((shell.rect.width-page_size[0])/2, (shell.rect.height-page_size[1])/2)
        
        page_rect = Rect(self.b, page_size)
        gap = (0, 18)
        b1.topleft = add(page_rect.bottomleft, gap)
        b2.midtop = add(page_rect.midbottom, gap)
        b3.topright = add(page_rect.bottomright, gap)
        Screen.__init__(self, shell, **kwds)
        self.size =  add(b3.bottomright, self.b)
        self.add(b1)
        self.add(b2)
        self.add(b3)
        self.prev_button = b1
        self.next_button = b3
        self.set_current_page(0)
    
    def draw(self, surface):
        self.pages[self.current_page].draw(surface, self.fg_color, self.b)
    
    
    
## Albow ignores events that it doesn't recognise
## instead of allowing someone to add their own event handler...
## In particular this includes window resizing
## ...WTF!!!!!!!!

class ExtendedRootWidget(RootWidget):
    
    def run_modal(self, modal_widget):
        is_modal = modal_widget is not None
        modal_widget = modal_widget or self
        print 'run_model: ', modal_widget
        try:
            old_top_widget = root.top_widget
            root.top_widget = modal_widget
            was_modal = modal_widget.is_modal
            modal_widget.is_modal = True
            modal_widget.modal_result = None
            if not modal_widget.focus_switch:
                modal_widget.tab_to_first()
            mouse_widget = None
            if root.clicked_widget:
                root.clicked_widget = modal_widget
            num_clicks = 0
            last_click_time = 0
            self.do_draw = True
            while modal_widget.modal_result is None:
                try:
                    if self.do_draw:
                        if self.is_gl:
                            self.gl_clear()
                            self.gl_draw_all(self, (0, 0))
                        else:
                            self.draw_all(self.surface)
                        self.do_draw = False
                        pygame.display.flip()
                    events = [pygame.event.wait()]
                    events.extend(pygame.event.get())
                    for event in events:
                        type = event.type
                        if type == QUIT:
                            self.quit()
                        elif type == MOUSEBUTTONDOWN:
                            self.do_draw = True
                            t = get_ticks()
                            if t - last_click_time <= double_click_time:
                                num_clicks += 1
                            else:
                                num_clicks = 1
                            last_click_time = t
                            event.dict['num_clicks'] = num_clicks
                            add_modifiers(event)
                            mouse_widget = self.find_widget(event.pos)
                            if not mouse_widget.is_inside(modal_widget):
                                mouse_widget = modal_widget
                            root.clicked_widget = mouse_widget
                            root.last_mouse_event_handler = mouse_widget
                            root.last_mouse_event = event
                            mouse_widget.notify_attention_loss()
                            mouse_widget.handle_mouse('mouse_down', event)
                        elif type == MOUSEMOTION:
                            add_modifiers(event)
                            modal_widget.dispatch_key('mouse_delta', event)
                            mouse_widget = self.find_widget(event.pos)
                            root.last_mouse_event = event
                            if root.clicked_widget:
                                root.last_mouse_event_handler = mouse_widget
                                root.clicked_widget.handle_mouse('mouse_drag', event)
                            else:
                                if not mouse_widget.is_inside(modal_widget):
                                    mouse_widget = modal_widget
                                root.last_mouse_event_handler = mouse_widget
                                mouse_widget.handle_mouse('mouse_move', event)
                        elif type == MOUSEBUTTONUP:
                            add_modifiers(event)
                            self.do_draw = True
                            mouse_widget = self.find_widget(event.pos)
                            if root.clicked_widget:
                                root.last_mouse_event_handler = root.clicked_widget
                                root.last_mouse_event = event
                                root.clicked_widget = None
                                root.last_mouse_event_handler.handle_mouse('mouse_up', event)
                        elif type == KEYDOWN:
                            key = event.key
                            set_modifier(key, True)
                            self.do_draw = True
                            self.send_key(modal_widget, 'key_down', event)
                            if root.last_mouse_event_handler:
                                event.dict['pos'] = root.last_mouse_event.pos
                                event.dict['local'] = root.last_mouse_event.local
                                root.last_mouse_event_handler.setup_cursor(event)
                        elif type == KEYUP:
                            key = event.key
                            set_modifier(key, False)
                            self.do_draw = True
                            self.send_key(modal_widget, 'key_up', event)
                            if root.last_mouse_event_handler:
                                event.dict['pos'] = root.last_mouse_event.pos
                                event.dict['local'] = root.last_mouse_event.local
                                root.last_mouse_event_handler.setup_cursor(event)
                        elif type == MUSIC_END_EVENT:
                            self.music_end()
                        elif type == USEREVENT:
                            make_scheduled_calls()
                            if not is_modal:
                                self.do_draw = self.redraw_every_frame
                                if root.last_mouse_event_handler:
                                    event.dict['pos'] = root.last_mouse_event.pos
                                    event.dict['local'] = root.last_mouse_event.local
                                    add_modifiers(event)
                                    root.last_mouse_event_handler.setup_cursor(event)
                                self.begin_frame()
                        else:
                            self.do_draw = True
                            self.send_key(modal_widget, 'event_handler', event)
                            if root.last_mouse_event_handler:
                                event.dict['pos'] = root.last_mouse_event.pos
                                event.dict['local'] = root.last_mouse_event.local
                                root.last_mouse_event_handler.setup_cursor(event)
                except Cancel:
                    pass
        finally:
            modal_widget.is_modal = was_modal
            root.top_widget = old_top_widget
        root.clicked_widget = None


from albow.controls import Label

class Error(Label):
    pass




if __name__ == '__main__':
    import doctest
    doctest.testfile(__file__+'.test')