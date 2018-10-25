import pygame


class Button:
    def __init__(self, action, texture):
        self.image = pygame.image.load(texture)
        self.action = action

    def get_surface(self):
        return self.image

    def interact(self, event):
        self.action(event)

    def __repr__(self):
        return "<Button {}>".format(self.action.__name__)


class Menu:
    def __init__(self, menu_item_list):
        self.menu_items = menu_item_list
        self.interactable = False

        self.menu_items_rects = []

    def interact(self, event, mode):
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            print(self.menu_items)
            print(self.menu_items_rects)
            mp = event.pos
            for mii, mir in enumerate(self.menu_items_rects):
                if mir.collidepoint(mp):
                    self.menu_items[mii].interact(event)
                    print(mode)

    def draw(self, screen, background_color):

        self.menu_items_rects = []

        screensize = screen.get_size()

        menu = pygame.Surface(screensize)

        menu.fill(background_color)

        centerx, cur_top_y = screensize[0]//2, 15

        for menu_item in self.menu_items:
            mi_surf = menu_item.get_surface()
            mi_rect = mi_surf.get_rect()
            mi_rect.centerx = centerx
            mi_rect.y = cur_top_y
            drect = menu.blit(mi_surf, mi_rect.topleft)

            cur_top_y = drect.bottom+5

            self.menu_items_rects.append(drect)


        screen.blit(menu, (0,0))



class Slot:
    def __init__(self, base_item):
        self.item = base_item
        self.base = base_item
        self.has_item = False

    def set_item(self, new_item):
        self.item = new_item

    def set_has_item(self, has_item):
        self.has_item = has_item


    def get_surface(self):
        if not self.item:
            return self.base

        surf = pygame.Surface((32,32)).convert_alpha()
        surf.fill((0,0,0,0))
        surf.blit(self.item, (4,4))

        return surf

class GUIContainer: pass