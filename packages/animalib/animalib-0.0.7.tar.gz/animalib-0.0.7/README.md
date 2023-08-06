# Pygame `AnimaLib`

The `AnimaLib` is a library for animating `Sprites` of the [PyGame](https://www.pygame.org/) library.

---

## Installation

Simply run 
`pip install anima-lib`
to download and install the library from [PyPI](https://pypi.org/project/anima-lib/).

---

### How it works

The core of the animation stands in the `frames` parameter of the `AnimatedSprite`.

In fact, the program will check if the duration associated to the current frame has been reached.
If so, the current frame will be set to the next one, and the duration will be reset, waiting for the next duration to be reached, and so on.

---

## How to use
### Classes
- #### Class `AnimatedSprite`
The class `AnimatedSprite` is a subclass of the [pygame.sprite.Sprite](https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite) class
that takes two mandatory parameters :

| Argument | Description                                      |
| --- |--------------------------------------------------|
| `frames` | A list of tuples of the form `(image, duration)` |
| `*groups` | A list of groups to add the sprite to. |

And a bunch of optional parameters :

| Optional argument | Description                                                                             |
| --- |-----------------------------------------------------------------------------------------|
| `start_frame` | The index of the first frame that will be displayed                                     |
| `first_frame` | The index of the first frame of the loop to be displayed [^1]                           |
| `last_frame` | The index of the last frame of the loop that will be displayed [^1]                     |
| `lock_at` | The index of the frame on which the animation will stop at                              |
| `do_kill` | A boolean that indicates whether the sprite will be removed from its groups or not [^2] |
| `delay_before_kill` | The delay before the sprite is removed from its groups [^2]                             |


[^1]: Considering the animation **will** loop.

[^2]: To be efficient, the `lock_at` parameter **has to be set**.

---

### Functions:
- `update()`

If the sprite is added to a group, it will automatically be updated.
Although, you can manuallly call `update()` to update the sprite each frame.

- `draw(surface:pygame.Surface, pos:iterable)`

If the sprite is added to a group, then it will automatically be drawn.
Although, you can call `draw(surface, pos)` to draw the sprite on a surface.

Notice that the `pos` parameter is optional, and if not provided, the sprite's rect will be used.

---

## Examples

- #### Imperative (using group)

```python
import pygame
from animalib import animalib
pygame.init()

run = True

screen = pygame.display.set_mode((500, 500))
group = pygame.sprite.Group()

frames = []
# [(image_0, duration_0), (image_1, duration_1), ...]

r, g, b = 255, 255, 255
for i in range(0, 10):
    surf = pygame.Surface((400, 400))
    surf.fill((r, g, b))
    # You can either load an image from a file instead of creating a surface...
    
    frames.append((surf, 500))
    # the duration is in milliseconds
    
    r -= 25
    g -= 25
    b -= 25

sprite = animalib.AnimatedSprite(frames, group)

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
            break
    screen.fill((0, 0, 0))
    
    group.update()
    group.draw(screen)
    
    pygame.display.flip()
pygame.quit()
```

- #### Object (without group, using `lock_at`)

```python
import pygame
from animalib import animalib

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((500, 500))
        self.run = False
        frames = self.load_frames()
        self.sprite = animalib.AnimatedSprite(frames, lock_at=5)

    def load_frames(self):
        frames = []
        r, g, b = 255, 255, 255
        for i in range(0, 10):
            surf = pygame.Surface((400, 400))
            surf.fill((r, g, b))
            # You can either load an image from a file instead of creating a surface...
            
            frames.append((surf, 500))
            # the duration is in milliseconds
            r -= 25
            g -= 25
            b -= 25
        return frames
        
        
    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
                
    def loop(self):
        self.run = True
        while self.run:
            self.events()
            self.screen.fill((0, 0, 0))
            
            self.sprite.update()
            self.sprite.draw(self.screen, (0, 0))
            
            pygame.display.flip()
        pygame.quit()

game = Game()
game.loop()
```

In these examples, the sprite's image is changing every 500 milliseconds and
its color is changing form white to gray. However, in the first one, the animation is looping,
and the group handle the draw itself.

But for the second one, the sprite locks itself at the 5th frame, 
and you have to manually handle the draw.
