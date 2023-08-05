import math
import time

import pygame


pygame.init()
a = pygame.font.SysFont("ariel", 30)


class Text:
    def __init__(self, font_size, txt, txt_color, size_obj = None, pos = "auto_XY", gui_obj = None):
        self.font_size = font_size
        self.txt = txt
        self.txt_color = txt_color
        self.font = pygame.font.SysFont("ariel", font_size)
        self.font_renderer = self.font.render(self.txt, True, txt_color)
        self.gui_obj = gui_obj
        self.pos = pos
        self.size_obj = size_obj
        self.size_txt = self.font_renderer.get_size()
        self.tmp_pos = int()


    def calculate_pos(self):
        if self.pos == "auto_XY":
            self.size_txt = self.font_renderer.get_size()
            return (self.size_obj[0] // 2 - self.size_txt[0] // 2, self.size_obj[1] // 2 - self.size_txt[1] // 2 )

        if self.pos == "auto_X":
            return self.size_obj[0] // 2 - self.size_txt[0] // 2

        if self.pos == "auto_Y":
            return self.size_obj[1] // 2 - self.size_txt[1] // 2

    def get_renderer(self):
        self.font = pygame.font.SysFont("ariel", self.font_size)
        self.font_renderer = self.font.render(self.txt, True, self.txt_color)
        return self.font_renderer



class Button:
    def __init__(self,window,pos,size,colour,txt_obj, listeners = [], listener_atributes = []):
        self.window = window
        self.pos = pos
        self.size = size
        self.listeners = listeners
        self.colour = colour
        self.txt_obj = txt_obj
        self.listener_atributes = listener_atributes
        ###
        if self.txt_obj:
            self.txt_obj.size_obj = self.size
        self.surface = pygame.Surface([self.size[0],size[1]])
        self.surface.fill(colour)
        self.rect = pygame.Rect(size,pos)


    def draw(self):
        if self.txt_obj:
            self.render_txt()
        self.window.blit(self.surface,self.pos)

    def check_press(self,e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    for i_funcs,funcs in enumerate(self.listeners):
                        funcs(self.listener_atributes[i_funcs])


    def non_event_update(self):
        self.surface = pygame.Surface([self.size[0], self.size[1]])
        self.rect = pygame.Rect(self.pos,self.size)
        self.surface.fill(self.colour)
        self.draw()


    def event_update(self,e):
        self.check_press(e)

    def render_txt(self):
        if self.txt_obj.pos == "auto_XY":

            self.surface.blit(self.txt_obj.get_renderer(), (self.txt_obj.calculate_pos()))

        elif self.txt_obj.pos == "auto_X":

            self.surface.blit(self.txt_obj.get_renderer(), (self.txt_obj.calculate_pos(), 0))

        elif self.txt_obj.pos == "auto_Y":

            self.surface.blit(self.txt_obj.get_renderer(), (0, self.txt_obj.calculate_pos()))



class Drop_down:
    def __init__(self,window,pos,size,colour,cases,txt_obj, listener, max_page_size = math.inf):
        self.window = window
        self.pos = pos
        self.size = size
        self.listener = listener
        self.colour = colour
        self.txt_obj = txt_obj

        ###
        if self.txt_obj:
            self.txt_obj.size_obj = self.size
        self.surface = pygame.Surface([self.size[0],size[1]])
        self.surface.fill(colour)
        self.rect = pygame.Rect(size,pos)
        self.selected_str = str()
        self.cases = cases
        self.drops_update = [[],[]]
        self.max_page_size = max_page_size
        self.current_page = 1
        self.boxes_are_dropped = False


    def draw(self):
        if self.txt_obj:
            self.render_txt()
        self.window.blit(self.surface,self.pos)

    def check_press(self,e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if not self.boxes_are_dropped:
                        self.duplicate_drop_downs(self.txt_obj)
                    self.boxes_are_dropped = True



    def non_event_update(self):
        self.surface = pygame.Surface([self.size[0], self.size[1]])
        self.rect = pygame.Rect(self.pos,self.size)
        self.surface.fill(self.colour)
        self.draw()
        self.drops_non_update()


    def event_update(self,e):
        self.check_press(e)
        self.drops_event_update(e)
        self.change_page(e)

    def render_txt(self):
        if self.txt_obj.pos == "auto_XY":

            self.surface.blit(self.txt_obj.get_renderer(), (self.txt_obj.calculate_pos()))

        elif self.txt_obj.pos == "auto_X":

            self.surface.blit(self.txt_obj.get_renderer(), (self.txt_obj.calculate_pos(), 0))

        elif self.txt_obj.pos == "auto_Y":

            self.surface.blit(self.txt_obj.get_renderer(), (0, self.txt_obj.calculate_pos()))

    def duplicate_drop_downs(self,txt_obj):
        pos_i = 0
        for i in range(len(self.cases)):
            pos_i += 1

            if i % (self.max_page_size) == 0:
                pos_i = 1

            #if i  >=  self.current_page * self.max_page_size - self.max_page_size and i < self.current_page * self.max_page_size:
            buttons_txt_obj = Text(30, self.cases[i], self.txt_obj.txt_color, self.size)

            a = Button(self.window, (self.pos[0], self.pos[1] + self.size[1] * pos_i), self.size, (0,112,111), buttons_txt_obj, [self.drop_down_event], [[self.cases[i],self.current_page]])

            self.drops_update[0].append(a.event_update)
            self.drops_update[1].append(a.non_event_update)




    def drop_down_event(self, arg):
        """

        :param arg: type(list[choosed case's name, current page number]);
                    it's argument passed to the listener function
        :return: None

        """

        self.selected_str = arg[0]
        self.listener(arg)
        self.drops_update = [[], []]
        self.boxes_are_dropped = False



    def drops_event_update(self,e):

        for i, f in enumerate(self.drops_update[0]):
            if i >= self.current_page * self.max_page_size - self.max_page_size and i < self.current_page * self.max_page_size:
                if f:
                    f(e)

    def drops_non_update(self):

        for i, f in enumerate(self.drops_update[1]):
            if i >= self.current_page * self.max_page_size - self.max_page_size and i < self.current_page * self.max_page_size:
                if f:
                    f()

    def change_page(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.boxes_are_dropped:
                    if not self.current_page >= math.ceil(len(self.cases) / self.max_page_size):
                        if e.button == 3:
                            self.current_page +=1
                    if not self.current_page <= 1:
                        if e.button == 1:
                            self.current_page -=1

