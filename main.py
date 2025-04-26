
from map import Map
from brick import Brick
from racket import Racket
from ball import Ball
from brick_block import BrickBlock
from racket_block import RacketBlock


def start_console():
    map = Map(10, 15)
    racket = Racket(2)
    map.add_racket(racket, 3, to_center=False)
    ball = Ball()
    map.add_ball(ball, 4, 4)

    for i in range(3):
        for j in range(0, 10, 2):
            map.add_brick(Brick(), i, j)
        
    map.show()

    while True:
        com = input()
        if com == "q":
            break
        elif com == "s":
            result = racket.move("left")
        elif com == "f":
            result = racket.move("right")
        ball.move()
        map.show()


def start_gui():
    import pygame

    MAP_WIDTH = 12
    MAP_HEIGHT = 16

    map = Map(MAP_WIDTH, MAP_HEIGHT)
    racket = Racket(2)
    map.add_racket(racket, 3, to_center=False)
    ball = Ball()
    map.add_ball(ball, 4, 4)

    for i in range(3):
        for j in range(0, MAP_WIDTH, 2):
            map.add_brick(Brick(), i, j)

    map.show()

    BLOCK_SIZE = 20
    SCREEN_WIDTH = MAP_WIDTH * BLOCK_SIZE
    SCREEN_HEIGHT = MAP_HEIGHT * BLOCK_SIZE
    FPS = 60
    GAME_SPEED = 150

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # GAME_STATE_FILENAME = "game_state"

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Arkanoid")
    clock = pygame.time.Clock()
    TIMEREVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMEREVENT, GAME_SPEED)


    def update_screen():
        screen.fill(BLACK)
        x = 0
        y = 0
        for h in range(MAP_HEIGHT):
            for w in range(MAP_WIDTH):
                content = map.map[h][w].content
                if content is not None:
                    if isinstance(content, BrickBlock):
                        pygame.draw.rect(screen, RED, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                    elif isinstance(content, RacketBlock):
                        pygame.draw.rect(screen, GREEN, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                    elif isinstance(content, Ball):
                        pygame.draw.rect(screen, BLUE, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                x += BLOCK_SIZE
            x = 0
            y += BLOCK_SIZE
        pygame.display.update()


    running = True
    is_need_update_screen = True
    racket_moved = False

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == TIMEREVENT:
                ball_moved = ball.move()
                if ball_moved is None:
                    running = False
                is_need_update_screen = True

            if event.type == pygame.KEYDOWN:
                is_need_update_screen = True

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                if not racket_moved:
                    racket.move("left")
                    racket_moved = True
            elif pressed[pygame.K_RIGHT]:
                if not racket_moved:
                    racket.move("right")
                    racket_moved = True
            elif pressed[pygame.K_q]:
                running = False


        if is_need_update_screen:
            update_screen()
            is_need_update_screen = False
            racket_moved = False

        clock.tick(FPS)
    pygame.quit()




def main():
    cmd = input("Select version please (1 - console, 2 - gui): ")
    # cmd = "2"
    if cmd == "1":
        start_console()
    elif cmd == "2":
        start_gui()
    else:
        print("Unknown command!")


if __name__ == "__main__":
    main()

