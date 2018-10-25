import pygame
from pygame.locals import *

import sprites, logic, toolbelt, gui
import math

# Variable Class
class Variable:
    def __init__(self, val):
        self.val = val

    def set(self, val):
        self.val = val

    def get(self):
        return self.val

    def __repr__(self):
        return self.val.__repr__()

    def __eq__(self, other):
        return self.val == other

    def __le__(self, other):
        return self.val <= other

    def __ge__(self, other):
        return self.val >= other

    def __lt__(self, other):
        return self.val < other

    def __gt__(self, other):
        return self.val > other

    def __setitem__(self, key, value):
        self.val[key] = value

    def __getitem__(self, item):
        return self.val[item]

    def __len__(self):
        return len(self.val)

    def __iter__(self):
        return iter(self.val)

pygame.init()

# Map and Window Size Constants
WINDOW_W, WINDOW_Y = 800,800
MAPSIZE = (5120,5120)

#make screen
screen = pygame.display.set_mode((WINDOW_W, WINDOW_Y))

#map the map
the_map = Variable(sprites.constructMap((math.ceil(MAPSIZE[0]/32),math.ceil(MAPSIZE[1]/32)), sprites.getSprite("grass")))

#load items
items = Variable({
    "gem-1": pygame.image.load("textures/items/gem-1.png").convert_alpha(),
    "gem-2": pygame.image.load("textures/items/gem-2.png").convert_alpha(),
    "gem-3": pygame.image.load("textures/items/gem-3.png").convert_alpha(),
    "gem-4": pygame.image.load("textures/items/gem-4.png").convert_alpha(),
    "gem-5": pygame.image.load("textures/items/gem-5.png").convert_alpha(),
    "gem-6": pygame.image.load("textures/items/gem-6.png").convert_alpha(),
    "gem-7": pygame.image.load("textures/items/gem-7.png").convert_alpha(),
    "gem-8": pygame.image.load("textures/items/gem-8.png").convert_alpha(),
    "gem-9": pygame.image.load("textures/items/gem-9.png").convert_alpha(),
    "gem-10": pygame.image.load("textures/items/gem-10.png").convert_alpha(),
    "stone": pygame.image.load("textures/items/stone.png").convert_alpha(),
    "water": pygame.image.load("textures/items/water.png").convert_alpha()
})

#load tiles
tiles = Variable({
    "stone": pygame.image.load("textures/tiles/stone.png").convert_alpha(),
    "water": pygame.image.load("textures/tiles/water.png").convert_alpha()
})

#make the toolbelt
tb = toolbelt.Toolbelt(10)
names = {0:"stone", 1:"water"}
for slotn, tb_slot_name in names.items():
    tb.insert_item_into_slot(slotn, items[tb_slot_name])

#Debug Menu
mode = Variable("debug_menu")

def set_mode(mode_):
    mode.set(mode_)

def reload_textures():
    old_items = items.get()
    new_items = {}
    for key in old_items:
        new_items[key] = pygame.image.load("textures/items/{}.png".format(key))
        if new_items[key] != old_items[key]:
            print(key, "has changed!")

    items.set(new_items)

    old_tiles = tiles.get()
    new_tiles = {}
    for key in old_tiles:
        new_tiles[key] = pygame.image.load("textures/tiles/{}.png".format(key))

    tiles.set(new_tiles)

    for slotn, tb_slot_name in names.items():
        tb.insert_item_into_slot(slotn, items[tb_slot_name])

    sprites.reload_textures()

    the_map.set(sprites.constructMap((math.ceil(MAPSIZE[0]/32),math.ceil(MAPSIZE[1]/32)), sprites.getSprite("grass")))

    set_mode("main")

reload_textures_button = gui.Button(lambda event: reload_textures(), "textures/gui/buttons/reload_textures.png")
menu_items = [reload_textures_button]
menu = gui.Menu(menu_items)

#offset variable
# offset = Variable([2048,2048])
offset = Variable([2048,2048])


def adjust_for_offset(pos):
    px, py = pos
    ox, oy = offset
    return (px+ox,py+oy)

selected_slot = 0
draws = {}

def get_tile_pos(pos):
    tx, ty = pos[0]//32, pos[1]//32
    return (tx*32,ty*32)


def flip_offset_sign():
    ox, oy = offset
    return (-ox,-oy)

bp = False

modes = ["main", "debug_menu"]

layer = pygame.Surface(MAPSIZE)

while 1:
    changed = False
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            # Event loop here


        if event.type == KEYDOWN:
            if event.key == K_c and mode == "main":
                draws = {}
                changed = True

            elif event.key == K_ESCAPE:
                if mode == "main":
                    set_mode("debug_menu")
                elif mode == "debug_menu":
                    set_mode("main")
                    changed = True

        if event.type == MOUSEBUTTONDOWN and mode == "main":
            bp = True
            slot_ = tb.get_slot_point_in(event.pos)
            if slot_ != None:
                if selected_slot != slot_:
                    selected_slot = slot_
            else:
                pos = get_tile_pos(event.pos)
                try:
                    draws[pos] = tiles[names[selected_slot]]

                except:
                    pass

        if event.type == MOUSEBUTTONUP and mode == "main":
            bp = False

        if event.type == MOUSEMOTION and bp and mode == "main":
            pos = get_tile_pos(event.pos)
            try:
                draws[adjust_for_offset(pos)] = tiles[names[selected_slot]]

            except:
                pass

        menu.interact(event, mode)


    if mode == "main":
        kp = pygame.key.get_pressed()
        
        if kp[K_LEFT]:
            pass
            


    screen.fill((255,255,255))

    if mode == "main":
        if changed:
            the_map.get().draw(layer)

            for tilepos, image in draws.items():
                layer.blit(image, tilepos)

            display.blit(layer, (0,0), pygame.Rect(offset.get(), (800,800)))

            tb.draw(screen, (0,0), [selected_slot])

    elif mode == "debug_menu":
        menu.draw(screen, (255,255,255))


    pygame.display.update()