
from map import Map
from brick import Brick
from racket import Racket
from ball import Ball


def start_console():
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


def start_gui():
    import pygame
    


def main():
    cmd = input("Select version please (1 - console, 2 - gui): ")
    # cmd = "1"
    if cmd == "1":
        start_console()
    elif cmd == "2":
        start_gui()
    else:
        print("Unknown command!")


if __name__ == "__main__":
    main()

