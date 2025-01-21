import random


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
    

class Cell:
    def __init__(self):
        self.content = None
        
        
class Brick:
    def __init__(self, w=2):
        self.width = w
        self.map_link = None
        self.blocks = []
        
        for i in range(self.width):
            self.blocks.append(BrickBlock(None, None, self))


class BrickBlock:
    def __init__(self, y, x, brick_link):
        self.x = x
        self.y = y
        self.brick_link = brick_link


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
        
        
class RacketBlock:
    def __init__(self, y, x, racket_link):
        self.x = x
        self.y = y
        self.racket_link = racket_link


class Ball:
    def __init__(self):
        self.x = None
        self.y = None
        self.map_link = None
        self.prev_dir = None


    def move(self, new_dir=None):
        dirs = {
            "up-left": (-1, -1),
            "up-right": (-1, 1),
            "down-left": (1, -1),
            "down-right": (1, 1),
        }
        
        # можно добавить случайности: 
            # при удалении нескольких кирпичей (удалять какой-то один)
            # при попадании в угол выбирать случайное направление (только не вниз при попадании в угол ракетки, хотя...)
        
        # может стоит выстроить проверки в один уровень:
        # проверка границ поля
        # проверка на наличие кирпичей и ракетки:
            # в направлении текущего движения
            # в направлении нового движения
        
        # исправить: передача лишних параметров, возврат нового значения, а не изменённого параметра. ну и оптимизация, много повторов..
        def check_dir(new_dir, new_y, new_x, map):
            if new_dir == "up-left":
                if new_x < 0:
                    if new_y < 0:
                        # стена и потолок (угол)
                        new_dir = "down-right"
                    elif isinstance(map[new_y][self.x].content, BrickBlock):
                        # стена и кирпич (угол)
                        content_up = map[new_y][self.x].content
                        content_up.brick_link.map_link.remove_brick(content_up.brick_link)
                        new_dir = "down-right"
                    else:
                        # стена
                        new_dir = "up-right"
                elif new_y < 0:
                    # потолок
                    new_dir = "down-left"
                else:
                    content_up = map[new_y][self.x].content # над мячом
                    content_left = map[self.y][new_x].content # слева от мяча
                    content_up_left = map[new_y][new_x].content # по диагонали от мяча
                    if isinstance(content_up, BrickBlock):
                        if isinstance(content_left, BrickBlock):
                            # кирпичи сверху и слева от мяча
                            content_up.brick_link.map_link.remove_brick(content_up.brick_link)
                            content_left.brick_link.map_link.remove_brick(content_left.brick_link)
                            new_dir = "down-right"
                        else:
                            # кирпич над мячом
                            content_up.brick_link.map_link.remove_brick(content_up.brick_link)
                            new_dir = "down-left"
                    elif isinstance(content_left, BrickBlock):
                        # кирпич слева от мяча
                        content_left.brick_link.map_link.remove_brick(content_left.brick_link)
                        new_dir = "up-right"
                    elif isinstance(content_up_left, BrickBlock):
                        # кирпич по диагонали от мяча
                        content_up_left.brick_link.map_link.remove_brick(content_up_left.brick_link)
                        new_dir = "down-right"

            elif new_dir == "up-right":
                if new_x == self.map_link.width:
                    if new_y < 0:
                        # стена и потолок (угол)
                        new_dir = "down-left"
                    elif isinstance(map[new_y][self.x].content, BrickBlock):
                        # стена и кирпич (угол)
                        content_up = map[new_y][self.x].content
                        content_up.brick_link.map_link.remove_brick(content_up.brick_link)
                        new_dir = "down-left"
                    else:
                        # стена
                        new_dir = "up-left"
                elif new_y < 0:
                    # потолок
                    new_dir = "down-right"
                else:
                    content_up = map[new_y][self.x].content # над мячом
                    content_right = map[self.y][new_x].content # справа от мяча
                    content_up_right = map[new_y][new_x].content # по диагонали от мяча
                    if isinstance(content_up, BrickBlock):
                        if isinstance(content_right, BrickBlock):
                            # кирпичи сверху и справа от мяча
                            content_up.brick_link.map_link.remove_brick(content_up.brick_link)
                            content_right.brick_link.map_link.remove_brick(content_right.brick_link)
                            new_dir = "down-left"
                        else:
                            # кирпич над мячом
                            content_up.brick_link.map_link.remove_brick(content_up.brick_link)
                            new_dir = "down-left"
                    elif isinstance(content_right, BrickBlock):
                        # кирпич справа от мяча
                        content_right.brick_link.map_link.remove_brick(content_right.brick_link)
                        new_dir = "up-left"
                    elif isinstance(content_up_right, BrickBlock):
                        # кирпич по диагонали от мяча
                        content_up_right.brick_link.map_link.remove_brick(content_up_right.brick_link)
                        new_dir = "down-left"

            elif new_dir == "down-left":
                if new_x < 0:
                    if new_y == self.map_link.height:
                        # стена и пол (угол)
                        print("game over")
                        return
                    elif isinstance(map[new_y][self.x].content, BrickBlock):
                        # стена и кирпич (угол)
                        content_down = map[new_y][self.x].content
                        content_down.brick_link.map_link.remove_brick(content_down.brick_link)
                        new_dir = "up-right"
                    elif isinstance(map[new_y][self.x].content, RacketBlock):
                        # стена и ракетка (угол)
                        new_dir = "up-right"
                    else:
                        # стена
                        new_dir = "down-right"
                elif new_y == self.map_link.height:
                    # пол
                    print("game over")
                    return
                else:
                    content_down = map[new_y][self.x].content # под мячом
                    content_left = map[self.y][new_x].content # слева от мяча
                    content_down_left = map[new_y][new_x].content # по диагонали от мяча
                    if isinstance(content_down, BrickBlock):
                        if isinstance(content_left, BrickBlock):
                            # кирпичи снизу и слева от мяча
                            content_down.brick_link.map_link.remove_brick(content_down.brick_link)
                            content_left.brick_link.map_link.remove_brick(content_left.brick_link)
                            new_dir = "up-right"
                        else:
                            # кирпич под мячом
                            content_down.brick_link.map_link.remove_brick(content_down.brick_link)
                            new_dir = "up-left"
                    elif isinstance(content_down, RacketBlock):
                        # ракетка под мячом
                        new_dir = "up-left"
                    elif isinstance(content_left, BrickBlock):
                        # кирпич слева от мяча
                        content_left.brick_link.map_link.remove_brick(content_left.brick_link)
                        new_dir = "down-right"
                    elif isinstance(content_down_left, BrickBlock):
                        # кирпич по диагонали от мяча
                        content_down_left.brick_link.map_link.remove_brick(content_down_left.brick_link)
                        new_dir = "up-right"
                    elif isinstance(content_down_left, RacketBlock):
                        # ракетка по диагонали от мяча
                        new_dir = "up-right"

            elif new_dir == "down-right":
                if new_x == self.map_link.width:
                    if new_y == self.map_link.height:
                        # стена и пол (угол)
                        print("game over")
                        return
                    elif isinstance(map[new_y][self.x].content, BrickBlock):
                        # стена и кирпич (угол)
                        content_down = map[new_y][self.x].content
                        content_down.brick_link.map_link.remove_brick(content_down.brick_link)
                        new_dir = "up-left"
                    elif isinstance(map[new_y][self.x].content, RacketBlock):
                        # стена и ракетка (угол)
                        new_dir = "up-left"
                    else:
                        # стена
                        new_dir = "down-left"
                elif new_y == self.map_link.height:
                    # пол
                    print("game over")
                    return
                else:
                    content_down = map[new_y][self.x].content # под мячом
                    content_right = map[self.y][new_x].content # справа от мяча
                    content_down_right = map[new_y][new_x].content # по диагонали от мяча
                    if isinstance(content_down, BrickBlock):
                        if isinstance(content_right, BrickBlock):
                            # кирпичи снизу и справа от мяча
                            content_down.brick_link.map_link.remove_brick(content_down.brick_link)
                            content_right.brick_link.map_link.remove_brick(content_right.brick_link)
                            new_dir = "up-left"
                        else:
                            # кирпич под мячом
                            content_down.brick_link.map_link.remove_brick(content_down.brick_link)
                            new_dir = "up-right"
                    elif isinstance(content_down, RacketBlock):
                        # ракетка под мячом
                        new_dir = "up-right"
                    elif isinstance(content_right, BrickBlock):
                        # кирпич справа от мяча
                        content_right.brick_link.map_link.remove_brick(content_right.brick_link)
                        new_dir = "down-left"
                    elif isinstance(content_down_right, BrickBlock):
                        # кирпич по диагонали от мяча
                        content_down_right.brick_link.map_link.remove_brick(content_down_right.brick_link)
                        new_dir = "up-left"
                    elif isinstance(content_down_right, RacketBlock):
                        # ракетка по диагонали от мяча
                        new_dir = "up-left"
                        
            return new_dir
        

        if new_dir is None:
            if self.prev_dir is not None:
                new_dir = self.prev_dir
            else:
                new_dir = random.choice(list(dirs.keys()))

        while True:
            print(new_dir)
            new_y = self.y + dirs[new_dir][0]
            new_x = self.x + dirs[new_dir][1]
            checked_new_dir = check_dir(new_dir, new_y, new_x, self.map_link.map)
            if checked_new_dir is None:
                return
            elif checked_new_dir == new_dir:
                break
            else:
                new_dir = checked_new_dir

        self.map_link.map[self.y][self.x].content = None
        self.y = self.y + dirs[new_dir][0]
        self.x = self.x + dirs[new_dir][1]
        self.map_link.map[self.y][self.x].content = self

        print(new_dir)
        self.prev_dir = new_dir
        
        self.map_link.show()


def main():
    map = Map(10, 15)
    racket = Racket(2)
    map.add_racket(racket, 3, to_center=False)
    ball = Ball()
    map.add_ball(ball, 4, 4)

    # map.add_brick(Brick(), 0, 0)
    # map.add_brick(Brick(), 0, 8)
    # map.add_brick(Brick(), 1, 5)
    for i in range(3):
        for j in range(0, 10, 2):
            map.add_brick(Brick(), i, j)
        
    map.show()
    # ball.move("up-left")
    # ball.move()
    # ball.move()
    # ball.move()
    # ball.move()

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
        ball.move()


if __name__ == "__main__":
    main()

