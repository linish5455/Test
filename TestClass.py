# Импортируем модуль очереди
from queue import Queue
# Импортируем модуль для генерации случайных чисел
import random
# Импортируем модуль для визуализации данных
import matplotlib.pyplot as plt

class CityGrid:
    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.grid = [[0 for _ in range(M)] for _ in range(N)]

        # Заполняем сетку случайными блоками (1 - заблокирован, 0 - разблокирован)
        self.populate_grid()

    def populate_grid(self):
        # Рассчитываем количество блоков для достижения покрытия
        total_blocks = self.N * self.M
        min_blocked_blocks = int(0.3 * total_blocks)
        blocked_blocks = 0

        while blocked_blocks < min_blocked_blocks:
            # Генерируем случайные координаты
            row = random.randint(0, self.N - 1)
            col = random.randint(0, self.M - 1)

            # Если выбранный блок еще не заблокирован, заблокируем его
            if self.grid[row][col] == 0:
                self.grid[row][col] = 1
                blocked_blocks += 1

    def display_grid(self):
        for row in self.grid:
            print(" ".join(map(str, row)))

    def place_tower(self, row, col, R):
        """
        Размещает башню в указанной позиции (row, col) с заданным радиусом действия R.
        """
        if row < 0 or row >= self.N or col < 0 or col >= self.M:
            print("Недопустимые координаты башни.")
            return

        for i in range(max(0, row - R), min(self.N, row + R + 1)):
            for j in range(max(0, col - R), min(self.M, col + R + 1)):
                # Помечаем ячейки, находящиеся в радиусе действия башни
                self.grid[i][j] = 2  # 2 - область покрытия башни

    def display_grid(self):
        for row in self.grid:
            print(" ".join(map(str, row)))

    def optimize_towers_placement(self, R):
        """
        Размещает башни так, чтобы все непокрытые блоки были в зоне действия хотя бы одной башни.
        """
        # Создаем список свободных блоков, которые нужно покрыть
        uncovered_blocks = [(i, j) for i in range(self.N) for j in range(self.M) if self.grid[i][j] == 0]

        while uncovered_blocks:
            # Выбираем случайный свободный блок и размещаем башню в его центре
            row, col = uncovered_blocks.pop()
            self.place_tower(row, col, R)

    def display_towers(self):
        """
        Отображает расположение башен на сетке.
        """
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] == 2:  # Блок внутри зоны покрытия башни
                    print("T", end=" ")
                else:
                    print("_", end=" ")
            print()

    def find_most_reliable_path(self, start, end):
        """
        Находит наиболее надежный путь между двумя башнями, где надежность пути - минимальное количество переходов.
        Возвращает путь в виде списка координат башен.
        """
        if self.grid[start[0]][start[1]] != 2 or self.grid[end[0]][end[1]] != 2:
            print("Начальная и конечная точки должны быть башнями.")
            return None

        visited = set()
        queue = Queue()
        parent = {}
        queue.put(start)
        visited.add(start)

        while not queue.empty():
            current = queue.get()
            if current == end:
                path = [end]
                while current != start:
                    current = parent[current]
                    path.append(current)
                path.reverse()
                return path

            row, col = current
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < self.N and 0 <= new_col < self.M and self.grid[new_row][new_col] == 2:
                        neighbor = (new_row, new_col)
                        if neighbor not in visited:
                            parent[neighbor] = current
                            visited.add(neighbor)
                            queue.put(neighbor)
        return None

    def visualize_grid(self):
        fig, ax = plt.subplots()
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] == 1:  # Блоки заблокированы
                    ax.add_patch(plt.Rectangle((j, self.N - i - 1), 1, 1, color='gray'))
                elif self.grid[i][j] == 2:  # Башня и ее зона покрытия
                    ax.add_patch(plt.Rectangle((j, self.N - i - 1), 1, 1, color='red'))
                else:  # Свободные блоки
                    ax.add_patch(plt.Rectangle((j, self.N - i - 1), 1, 1, color='white', fill=False))

        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()
