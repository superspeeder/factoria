import pygame

import gui

class Toolbelt(gui.GUIContainer):
    def __init__(self, slots):
        self.fillersurf = pygame.Surface((32,32))
        self.fillersurf.fill((0,0,0))

        self.selected_filler_surf = pygame.Surface((32,32))
        self.selected_filler_surf.fill((0,255,0))

        self.slots = [gui.Slot(self.fillersurf) for x in range(slots)]

    def insert_item_into_slot(self, slotid, item):
        if item:
            self.slots[slotid].set_item(item)
        else:
            self.slots[slotid].set_item(self.fillersurf)

    def get_slot_point_in(self, point):
        for sn, slot in enumerate(self.slots):
            rect = pygame.Rect((2 + sn * 34, 2), (32,32))
            if rect.collidepoint(point):
                return sn

        else: return None

    def draw(self, screen, pos, selected_slots):
        toolbelt_surf = pygame.Surface((2 + len(self.slots)*34,36)).convert_alpha()
        toolbelt_surf.fill((255,255,255))
        for sn,slot in enumerate(self.slots):
            try:
                if sn in selected_slots:
                    toolbelt_surf.blit(self.selected_filler_surf, (2 + sn * 34, 2))
                else:
                    toolbelt_surf.blit(self.fillersurf, (2 + sn * 34, 2))


                toolbelt_surf.blit(slot.get_surface(), (2+sn*34,2))
            except:
                continue

        screen.blit(toolbelt_surf, pos)