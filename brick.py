
from brick_block import BrickBlock


class Brick:
    def __init__(self, w=2):
        self.width = w
        self.map_link = None
        self.blocks = []
        
        for i in range(self.width):
            self.blocks.append(BrickBlock(None, None, self))
