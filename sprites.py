import pygame

import random

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

class SpriteMap:

    def populate_map(self, filler):
        for y in range(self.height):
            print(y)
            for x in range(self.width):
                self.map.add(filler(x*32,y*32))



    def __init__(self, mapsize, filler=None):
        self.width, self.height = mapsize
        self.map = pygame.sprite.Group()
        self.populate_map(filler)

    def draw(self, screen):
        self.map.draw(screen)


def constructMap(size, filler):
    return SpriteMap(size, filler)

sprites = {}

def getSprite(name):
    return sprites[name]


class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y

class RandomChoiceSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, surfaces):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(surfaces)
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y

def sprite_builder(sprite_class, surf):
    def get_sprite(x,y):
        return sprite_class(x,y,surf)

    return get_sprite


grass_images = Variable([pygame.image.load("grass1.png"),pygame.image.load("grass2.png"),pygame.image.load("grass3.png")])
sprites["grass"] = sprite_builder(RandomChoiceSprite, grass_images)


def reload_textures():
    grass_images.set([pygame.image.load("grass1.png"), pygame.image.load("grass2.png"), pygame.image.load("grass3.png")])
    sprites["grass"] = sprite_builder(RandomChoiceSprite, grass_images)
