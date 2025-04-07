from racket_block import RacketBlock


class Racket:
    def __init__(self, w=2):
        self.width = w
        self.map_link = None
        self.blocks = []
        
        for i in range(self.width):
            self.blocks.append(RacketBlock(None, None, self))
              
            
    def move(self, new_dir):
        def check_on_borders(map, x1, x2):
            if (x1 < 0) or (x2 >= len(map[0])):
                return False
            
            return True
        
        dirs = {
            "right": 1,
            "left": -1
        }
        
        print(new_dir)
        new_x1 = self.blocks[0].x + dirs[new_dir]
        # new_x2 = new_x1 + self.width - 1
        new_x2 = self.blocks[-1].x + dirs[new_dir]
        
        if not check_on_borders(self.map_link.map, new_x1, new_x2):
            print("Border!")
            return
        
        for b in self.blocks:
            self.map_link.map[b.y][b.x].content = None
        
        for b in self.blocks:
            b.x = b.x + dirs[new_dir]
            self.map_link.map[b.y][b.x].content = b
        
        # self.map_link.update()
        # self.map_link.show()
