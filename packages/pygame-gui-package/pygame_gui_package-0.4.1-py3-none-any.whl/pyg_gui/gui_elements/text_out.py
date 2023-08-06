import sys, time, pygame

class Txt_out:
    def __init__(self,win, pos, size, color, txt_obj):
        self.win = win
        self.pos = pos
        self.size = size
        self.color = color
        self.txt_obj = txt_obj
        ###
        txt_obj.size_obj = size
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.rect = pygame.Rect(pos,size)
        self.scroll_pos = 0


    def draw(self):
        self.win.blit(self.surface, (self.pos))

    def draw_txt(self):

        if self.txt_obj.get_renderer().get_width() <= self.size[0]:
            self.surface.blit(self.txt_obj.get_renderer(), self.txt_obj.calculate_pos())
        else:
            self.surface.blit(self.txt_obj.get_renderer(), (0, self.size[1] // 2 - self.txt_obj.get_renderer().get_size()[1] // 2), (self.scroll_pos, 0, self.size[0], self.size[1]))

    def update_draw_pos(self, e):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if e.type == pygame.MOUSEWHEEL:
                if e.y == 1:
                    if self.scroll_pos + self.size[0] <= self.txt_obj.get_renderer().get_width():
                        self.scroll_pos += 20

                if e.y == -1:
                    if self.scroll_pos >= 0:
                        self.scroll_pos -= 20


    def non_event_update(self):
        self.draw_txt()
        self.draw()
        self.surface.fill(self.color)


    def event_update(self, e):
        self.rect = pygame.Rect(self.pos, self.size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)


        self.update_draw_pos(e)





