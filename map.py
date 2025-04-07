
from cell import Cell
from brick_block import BrickBlock
from racket_block import RacketBlock
from ball import Ball


class Map:
    def __init__(self, w=10, h=10):
        self.width = w
        self.height = h
        self.map = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        self.bricks = []
        self.racket = None
        self.ball = None
        
        
    def show(self):
        border = " " + "-=-" * len(self.map[0])
        print(border)
        for y in range(self.height):
            print("|", end="")
            num_line = " "
            for x in range(self.width):
                num_line += f" {x} "
                content = self.map[y][x].content
                if content is None:
                    print("   ", end="")
                elif isinstance(content, BrickBlock):
                    print(" b ", end="")
                elif isinstance(content, RacketBlock):
                    print(" r ", end="")
                elif isinstance(content, Ball):
                    print(" o ", end="")
            print("|", y)
        print(border)
        print(num_line)
        
        
    def add_racket(self, r, x=None, to_center=False):
        if self.racket is not None:
            return
        
        start_x = 0
        if x is not None:
            start_x = x
        else:        
            # расчет индекса для добавления ракетки по центру (при ровном делении)
            if to_center:
                start_x = (self.width // 2) - (r.width // 2)
        
        for i in range(len(r.blocks)):
            r.blocks[i].y = self.height - 1
            r.blocks[i].x = start_x + i
            self.map[r.blocks[i].y][r.blocks[i].x].content = r.blocks[i]
        
        r.map_link = self
        self.racket = r


    def add_ball(self, b, y=None, x=None):
        if self.ball is not None:
            return

        _y = y
        _x = x
        if (y is None) or (x is None):
            _y = (self.height // 2) - 1
            _x = (self.width // 2) - 1
            if self.racket is not None:
                _y = self.racket.blocks[0].y - 1
                _x = self.racket.blocks[self.racket.width // 2].x
        b.y = _y
        b.x = _x

        self.map[b.y][b.x].content = b
        self.ball = b
        b.map_link = self
        

    def add_brick(self, brick, y=None, x=None):
        if brick in self.bricks:
            return
        
        _y = 0
        _x = 0
        
        if (x is not None) and (y is not None):
            if self.map[y][x].content is not None:
                return
            _y = y
            _x = x
        
        # определение координат: на основе уже добавленных блоков или от 0 если пусто
        # или рандом (опция)
        
        # if len(self.bricks) > 0:
        #     last_brick = self.bricks[-1]
        
        for i in range(len(brick.blocks)):
            brick.blocks[i].y = _y # пока так, для тестов
            brick.blocks[i].x = _x + i
            self.map[brick.blocks[i].y][brick.blocks[i].x].content = brick.blocks[i]
        
        brick.map_link = self
        self.bricks.append(brick)

        
    def remove_brick(self, brick):
        for block in brick.blocks:
            self.map[block.y][block.x].content = None
        
        brick.map_link = None
        self.bricks.remove(brick)
        
    
    def update(self):
        pass