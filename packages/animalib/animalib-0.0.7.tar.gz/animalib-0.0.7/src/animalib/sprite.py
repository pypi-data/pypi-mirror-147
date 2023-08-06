import pygame as pg

class AnimatedSprite(pg.sprite.Sprite):
    """
    Subclass of Sprite. Used to create animated sprites based on
    a list of couples (image, duration).
    """

    def __init__(self, frames:iter, *groups, start_frame:int=0, first_frame:int=0, last_frame:int=None, lock_at:int=-1, do_kill:bool=False, delay_before_kill:int=0):
        super().__init__()
        if groups:
            self.add(*groups)

        self.frames = frames # [(image, duration), ...]
        self.first_frame = first_frame # the first frame to be displayed at all time
        self.last_frame = last_frame # could be None

        if first_frame: # first frame "overrides" start_frame
            self.current_frame = first_frame
        else:
            self.current_frame = start_frame # the first frame to be shown (only once, for loop, use <first_frame>)
        self.current_couple = self.frames[self.current_frame] # (image, duration)

        self.lock_id = lock_at # index of last frame to lock on (could be > length(frames)) -> deduce a loop time
        self.dokill = do_kill # if the sprite should be killed
        self.delay_before_kill = delay_before_kill

        self.last_update = pg.time.get_ticks()
        self.length = len(self.frames)

        self.image = self.frames[self.current_frame][0] # mandatory for group draw
        self.rect = self.image.get_rect()

    def animate(self):
        now = pg.time.get_ticks()

        if self.lock_id >= 0:
            if self.current_frame == self.lock_id: # lock on last_frame
                if self.dokill and now - self.last_update > self.delay_before_kill:
                    self.kill()
                return

        if now - self.last_update > self.current_couple[1]: # if enough time has passed
            self.last_update = now
            if self.last_frame:
                if self.current_frame == self.last_frame:
                    self.current_frame = self.first_frame
                else:
                    self.current_frame += 1
            else:
                self.current_frame = (self.current_frame + 1) % self.length

            self.current_couple = self.frames[self.current_frame] # update the couple
            self.image = self.current_couple[0] # update the image

    def draw(self, surface:pg.Surface, pos:iter=None):
        if pos:
            surface.blit(self.image, pos)
        else:
            surface.blit(self.image, self.rect)

    def update(self):
        self.animate()
