"""Игра Змейка на pygame"""

from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

ALL_CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (24, 16, 38)

# Цвет границы ячейки
BORDER_COLOR = (126, 87, 194)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (192, 145, 255)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """класс игровых объектов"""

    def __init__(self):
        """задаем позицию начала и цвет объекта"""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """определяем отрисовку объекта"""
        pass


class Apple(GameObject):
    """описание поведения яблока"""

    def __init__(self, filled_positions=()):
        """задаем цвет и позицию с учетом клеток, занятых змейкой"""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(filled_positions)

    def randomize_position(self, filled_positions=()):
        """выбор клетки свободной"""
        free_cells = ALL_CELLS - set(filled_positions)
        self.position = choice(tuple(free_cells))

    def draw(self):
        """отрисовка яблока на поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """описание логики змеи"""
    
    def __init__(self):
        """задаем цвет и начальную позицию"""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    # вернуть в нач позицию
    def reset(self):
        """вернуть змею на начальное состояние - сброс"""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """определяем направление, которое выбрал пользователь"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """передвижение змейки на 1 клетку"""
        x, y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """отрисовка змеи - стираем хвост"""
        if self.last:
            last_rect = pygame.Rect(
                self.last, (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                screen, BOARD_BACKGROUND_COLOR, last_rect
            )
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """возвращаем голову змейки"""
        return self.positions[0]


# Обработка действий пользователя
def handle_keys(game_object):
    """обработка нажатия клавиш для игры"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """запуск основной логики игры"""
    # Инициализация PyGame:
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)

    record = snake.length
    pygame.display.set_caption(f'Змейка | Рекорд: {record}')
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.positions.append(snake.last)
            snake.last = None

            if snake.length > record:
                record = snake.length
                pygame.display.set_caption(f'Змейка | Рекорд: {record}')

            if snake.length == len(ALL_CELLS):
                pygame.quit()
                return

            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

            if apple.position in snake.positions:
                apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
