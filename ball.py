import random

from brick_block import BrickBlock
from racket_block import RacketBlock


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
        # можно сделать две функции: движение вверх и вниз. А стороны передавать в параметрах (вроде они идентичны, проверить..)
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
        
        # self.map_link.show()
