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

