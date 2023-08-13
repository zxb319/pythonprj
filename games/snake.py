import os
import random
from collections import deque

import pygame

MAP_SIZE = (10, 10)
UNIT_SIZE = 40


class Food:
    def __init__(self, color):
        self.color = color
        self.food_pos = None

    def gen_next_food_pos(self, snake: 'Snake'):
        p = (random.randint(0, MAP_SIZE[0]), random.randint(0, MAP_SIZE[1]))
        while p in snake.body_poses:
            p = (random.randint(0, MAP_SIZE[0]), random.randint(0, MAP_SIZE[1]))
        self.food_pos = p

    def draw(self, screen: pygame.Surface):
        s = pygame.Surface((UNIT_SIZE, UNIT_SIZE))
        s.fill(self.color)
        screen.blit(s, tuple(x * UNIT_SIZE for x in self.food_pos))


class Snake:
    def __init__(self, body_poses: deque, head_color, body_color, default_direct):
        self.body_poses = body_poses
        self.head_color = head_color
        self.body_color = body_color
        self.direct = default_direct

    def draw(self, screen: pygame.Surface):
        for i, bp in enumerate(self.body_poses):
            cur_s = pygame.Surface((UNIT_SIZE, UNIT_SIZE))
            if i == len(self.body_poses)-1:
                cur_s.fill(self.head_color)
            else:
                cur_s.fill(self.body_color)

            screen.blit(cur_s, tuple(x * UNIT_SIZE for x in bp))
            text_surface=score_font.render(f"Score:{len(snake.body_poses)}", False, 'White')
            screen.blit(text_surface,(UNIT_SIZE,UNIT_SIZE))

    def change_direct(self, keys_pressed):
        if self.direct != (1, 0) and (keys_pressed == pygame.K_LEFT):
            self.direct = (-1, 0)
        elif self.direct != (-1, 0) and (keys_pressed == pygame.K_RIGHT):
            self.direct = (1, 0)
        elif self.direct != (0, 1) and (keys_pressed == pygame.K_UP):
            self.direct = (0, -1)
        elif self.direct != (0, -1) and (keys_pressed == pygame.K_DOWN):
            self.direct = (0, 1)

    def go(self, food: Food):
        head_pos = self.body_poses[-1]
        next_pos = tuple(x + p for x, p in zip(head_pos, self.direct))
        if next_pos == food.food_pos:
            self.body_poses.append(next_pos)
            food.gen_next_food_pos(self)
        elif next_pos in self.body_poses:
            # raise Exception(rf'bite yourself!')
            # self.body_poses.append(next_pos)
            # self.body_poses.popleft()
            pass
        elif not 0 <= next_pos[0] <= MAP_SIZE[0] or not 0 <= next_pos[1] <= MAP_SIZE[1]:
            # raise Exception(rf'hit on wall!')
            pass
        else:
            self.body_poses.append(next_pos)
            self.body_poses.popleft()


pygame.init()
screen = pygame.display.set_mode(tuple((x + 1) * UNIT_SIZE for x in MAP_SIZE))
pygame.display.set_caption('贪吃蛇')
clock = pygame.time.Clock()

snake = Snake(deque([(MAP_SIZE[0] // 2, MAP_SIZE[1] // 2,)]), 'Red', (255, 255, 125), (0, 1))
food = Food('Green')
food.gen_next_food_pos(snake)
test_font = pygame.font.Font(os.path.join(rf'msyh.ttc'), 50)
score_font = pygame.font.Font(None, 16)
running = True
not_quit = True
while not_quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            not_quit = False
            break
        elif event.type == pygame.KEYDOWN:
            snake.change_direct(event.key)

    if not not_quit:
        break
    try:
        if running:
            snake.go(food)
            screen.fill('Black')
            snake.draw(screen)
            food.draw(screen)
            pygame.display.flip()
    except Exception as e:
        running = False
        text_surface = test_font.render(f"Game Over:{e}", False, 'White')
        screen.blit(text_surface, (MAP_SIZE[0] // 2, MAP_SIZE[1] // 2 * UNIT_SIZE))
        pygame.display.flip()
        print(e)

    clock.tick(5)
    # time.sleep(1)
