import sys, time, pygame

is_shift = False


def pyg_keydecoder(key, shift):
    keycode = {
        113: "q",
        119: "w",
        101: "e",
        114: "r",
        116: "t",
        122: "z",
        117: "u",
        105: "i",
        111: "o",
        112: "p",
        97: "a",
        115: "s",
        100: "d",
        102: "f",
        103: "g",
        104: "h",
        106: "j",
        107: "k",
        108: "l",
        121: "y",
        120: "x",
        99: "c",
        118: "v",
        98: "b",
        110: "n",
        109: "m",
        48: "0",
        49: "1",
        50: "2",
        51: "3",
        52: "4",
        53: "5",
        54: "6",
        55: "7",
        56: "8",
        57: "9",
        44: ",",
        46: ".",
        45: "-",
        1073742049: "shift",
        1073742048: "control",
        1073741881: "capslock",
        9: "tab",
        32: " ",
        233: "é",
        225: "á",
        237: "í",
        48: "ö",
        252: "ü",
        243: "ó",
        337: "ő",
        250: "ú",
        369: "ű",
        1073741913: "1",
        1073741914: "2",
        1073741915: "3",
        1073741916: "4",
        1073741917: "5",
        1073741918: "6",
        1073741919: "7",
        1073741920: "8",
        1073741921: "9"
    }
    if key in keycode.keys():
        global is_shift
        if is_shift:
            is_shift = False

            return keycode[key].capitalize()
        if shift:
            is_shift = True
            return ""
        else:
            return keycode[key]
    return ""



class Txt_in:
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
        self.rect = pygame.Rect(pos, size)
        self.scroll_pos = 0
        self.backspace = False



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
        self.use_backspace()
        self.draw_txt()
        self.draw()
        self.surface.fill(self.color)


    def event_update(self, e):
        self.rect = pygame.Rect(self.pos, self.size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)

        self.get_input(e)
        self.update_draw_pos(e)

    def get_input(self,e):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if e.type == pygame.KEYDOWN:

                if e.key == 1073742049:
                    if pyg_keydecoder(e.key, True) != "":
                        self.txt_obj.txt = f"{self.txt_obj.txt} {pyg_keydecoder(e.key, True)}"
                        self.scroll_pos = self.txt_obj.font_renderer.get_width() - self.size[0] + 30

                else:
                    self.txt_obj.txt = f"{self.txt_obj.txt}{pyg_keydecoder(e.key, False)}"
                    self.scroll_pos = self.txt_obj.font_renderer.get_width() - self.size[0] + 30



                if e.key == pygame.K_BACKSPACE:
                    self.backspace = True


            if e.type == pygame.KEYUP:
                if e.key == pygame.K_BACKSPACE:
                    self.backspace = False


    def use_backspace(self):
        if self.backspace:

            self.txt_obj.txt = self.txt_obj.txt[:-1]
            time.sleep(0.07)