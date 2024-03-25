import pygame
import numpy as np
import threading
import matplotlib.pyplot as plt
from scipy.stats import entropy
import time

# Pygame 설정
num_particles = 100
grid_size = 600
particle_size = 2
particle_color = (255, 255, 255)
particles = [[grid_size // 2, grid_size // 2] for _ in range(num_particles)]

# 엔트로피 데이터 리스트
entropy_values = []

# 엔트로피 계산 함수
def calculate_entropy(density_grid):
    p = density_grid.flatten()
    p = p / np.sum(p)
    return entropy(p, base=2)

# Pygame 시뮬레이션 함수
def pygame_simulation():
    pygame.init()
    screen = pygame.display.set_mode((grid_size, grid_size))
    pygame.display.set_caption('Gas Diffusion Simulation')
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        density_grid = np.zeros((grid_size, grid_size))

        for particle in particles:
            particle[0] += np.random.randint(-1, 2)
            particle[1] += np.random.randint(-1, 2)
            particle[0] = max(0, min(particle[0], grid_size-1))
            particle[1] = max(0, min(particle[1], grid_size-1))
            density_grid[particle[0], particle[1]] += 1
            pygame.draw.circle(screen, particle_color, particle, particle_size)

        pygame.display.flip()
        clock.tick(60)

        # 엔트로피 계산 및 저장
        entropy_value = calculate_entropy(density_grid)
        entropy_values.append(entropy_value)

    pygame.quit()

# Matplotlib 시각화 함수
def plot_entropy():
    plt.ion()
    fig, ax = plt.subplots()
    while True:
        if entropy_values:
            ax.clear()
            ax.plot(entropy_values, color='blue')
            ax.set_xlabel('Time Step')
            ax.set_ylabel('Entropy')
            fig.canvas.draw()
            fig.canvas.flush_events()
        time.sleep(0.1)  # 업데이트 간격 조정

# Pygame 스레드 시작
thread = threading.Thread(target=pygame_simulation)
thread.start()

# Matplotlib 시각화 실행
plot_entropy()