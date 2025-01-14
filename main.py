
class Map:
    def __init__(self, w=10, h=10):
        self.width = w
        self.height = h
        self.map = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        self.bricks = []
        self.racket = None
        
        
    def show(self):
        # border = "=" * len(self.map[0]) * 3
        border = " = " * len(self.map[0])
        print(border)
        for y in range(self.height):
            for x in range(self.width):
                content = self.map[y][x].content
                if content is None:
                    print("   ", end="")
                elif isinstance(content, BrickBlock):
                    print(" b ", end="")
                elif isinstance(content, RacketBlock):
                    print(" r ", end="")
                elif isinstance(content, BallBlock):
                    print(" o ", end="")
            print()
        print(border)
        
        
    def add_racket(self, r, to_center=False):
        if self.racket is not None:
            return
        
        # расчет индексов, чтобы добавлять ракетку по центру
        start_x = 0
        end_x = r.width
        if to_center:
            start_x = (self.width // 2) - (r.width // 2)
            end_x = start_x + r.width
        
        for i in range(len(r.blocks)):
            r.blocks[i].y = self.height - 1
            r.blocks[i].x = start_x + i
            self.map[r.blocks[i].y][r.blocks[i].x].content = r.blocks[i]
        
        r.map_link = self
        self.racket = r

    
    def update(self):
        pass
    

class Cell:
    def __init__(self):
        self.content = None
        
        
class Brick:
    pass


class BrickBlock:
    def __init__(self, y, x):
        self.x = x
        self.y = y


class Racket:
    def __init__(self, w=2):
        self.width = w
        self.map_link = None
        self.blocks = []
        
        for i in range(self.width):
            self.blocks.append(RacketBlock(None, i))
              
            
    def move(self, new_dir) -> bool:
        def check_on_borders(map, x1, x2):
            if (x1 < 0) or (x2 >= len(map[0])):
                return False
            
            return True
        
        dirs = {
            "right": (0, 1),
            "left": (0, -1)
        }
        
        print(new_dir)
        new_x1 = self.blocks[0].x + dirs[new_dir][1]
        # new_x2 = new_x1 + self.width - 1
        new_x2 = self.blocks[-1].x + dirs[new_dir][1]
        
        if not check_on_borders(self.map_link.map, new_x1, new_x2):
            print("Border!")
            return
        
        for b in self.blocks:
            self.map_link.map[b.y][b.x].content = None
        
        for b in self.blocks:
            b.x = b.x + dirs[new_dir][1]
            self.map_link.map[b.y][b.x].content = b
        
        # self.map_link.update()
        self.map_link.show()
        
        
class RacketBlock:
    def __init__(self, y, x):
        self.x = x
        self.y = y


class Ball:
    pass


class BallBlock:
    def __init__(self, y, x):
        self.x = x
        self.y = y


map = Map()
map.show()

racket = Racket(3)
map.add_racket(racket, to_center=False)
map.show()

# racket.move("left")
# racket.move("right")
# racket.move("right")
# racket.move("right")
# racket.move("left")
# racket.move("right")
# racket.move("right")
# racket.move("right")
# racket.move("right")
# racket.move("right")
# racket.move("right")

while True:
    com = input()
    if com == "q":
        break
    elif com == "s":
        result = racket.move("left")
    elif com == "f":
        result = racket.move("right")
