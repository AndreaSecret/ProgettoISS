from pygame import Surface
from pygame.sprite import Sprite, GroupSingle
from game_assets import screen_x, screen_y, bar_h

# semplicemente il rettangolo in basso con le mosse ecc.

class MatchBar(Sprite):
    def __init__(self):
        super().__init__()
        self.state = None
        self.image = Surface((screen_x, bar_h))
        self.image.fill("#FFFFFF")
        self.rect = self.image.get_rect(topleft = (0, screen_y-bar_h))

bar = GroupSingle(MatchBar())