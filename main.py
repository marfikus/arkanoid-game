
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
                # if self.map[y][x].player_here:
                #     print(" p ", end="")
                #     continue
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
        
        # заполнение при толщине ракетки в 1 слой
        # for i in range(len(r.blocks)):
        #     r.blocks[i].y = self.height - 1
        #     r.blocks[i].x = start_x + i
        #     self.map[r.blocks[i].y][r.blocks[i].x].content = r.blocks[i]
               
        # при толщине в несколько слоёв
        n = 0
        for i in range(r.height):
            for j in range(start_x, end_x):
                r.blocks[n].y = (self.height - r.height) + i
                r.blocks[n].x = j
                self.map[r.blocks[n].y][r.blocks[n].x].content = r.blocks[n]
                n += 1
        
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
    def __init__(self, w=2, h=1):
        self.width = w
        self.height = h
        self.map_link = None
        self.blocks = []
        
        for i in range(self.height):
            for j in range(self.width):
                self.blocks.append(RacketBlock(i, j))
              
            
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

racket = Racket(w=3, h=1)
map.add_racket(racket)
map.show()

racket.move("left")
racket.move("right")
racket.move("right")
racket.move("right")
racket.move("left")
racket.move("right")
racket.move("right")
racket.move("right")
racket.move("right")
racket.move("right")
racket.move("right")


