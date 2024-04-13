import pygame
import random

# иницилизация
pygame.init()

# размер окна и ячейка
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Константы для направлений движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Создание класса для представления змейки
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # Запретить поворот на 180 градусов
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x * CELL_SIZE) % SCREEN_WIDTH, (cur[1] + y * CELL_SIZE) % SCREEN_HEIGHT)
        # Проверка на столкновение со своим хвостом
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        return False

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


# Создание класса для точки (еды)
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


# Функция для отображения счета
def draw_score(surface, score, high_score):
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("Счет: " + str(score), True, WHITE)
    high_score_text = font.render("Рекорд: " + str(high_score), True, WHITE)
    surface.blit(score_text, (10, 10))
    surface.blit(high_score_text, (10, 40))


# Основная функция игры
def main():
    # Создание окна Pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')

    # Создание объектов
    snake = Snake()
    food = Food()
    clock = pygame.time.Clock()

    # Переменные для хранения счета
    score = 0
    high_score = 0

    # Основной игровой цикл
    running = True
    while running:
        screen.fill(BLACK)

        # Обработка действий пользователя
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)

        # Проверка на столкновение с едой
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1  # Увеличение счета при съедании еды
            if score > high_score:
                high_score = score
            food.randomize_position()

        # Проверка на столкновение с собственным хвостом
        if snake.move():
            high_score = max(high_score, score)
            score = 0
            snake.reset()

        # Отрисовка еды и змейки
        food.draw(screen)
        for p in snake.positions:
            rect = pygame.Rect(p[0], p[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, snake.color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

        # Отображение счета
        draw_score(screen, score, high_score)

        # Обновление экрана
        pygame.display.update()

        # Ограничение скорости кадров
        clock.tick(10)

    # Завершение Pygame после выхода из игры
    pygame.quit()


if __name__ == "__main__":
    main()



