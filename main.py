import time
import keyboard
import pydirectinput as dir
from PIL import Image, ImageGrab
import numpy as np
import sys


def draw_coords_with_mouse(coords: list[list[int]], start_x, start_y):
    pixel_size = 1

    def move_to(x, y):
        relative_x = start_x + (x * pixel_size)
        relative_y = start_y + (y * pixel_size)
        dir.moveTo(relative_x, relative_y, duration=0)

    def is_straight_line_segment(start, end):
        return start[0] == end[0] or start[1] == end[1]

    def draw_line_segment(start, end):
        move_to(start[1], start[0])
        dir.mouseDown()
        move_to(end[1], end[0])
        dir.mouseUp()

    time.sleep(0.15)

    i = 0
    while i < len(coords):
        if keyboard.is_pressed("p"):
            break

        start = coords[i]
        end = start
        j = i + 1
        while j < len(coords) and is_straight_line_segment(start, coords[j]):
            end = coords[j]
            j += 1

        draw_line_segment(start, end)
        i = j
    isActive = False
    dir.mouseUp()


def find_path(data: list[list[int]]) -> list[list[list[int]]]:
    def is_valid(x, y):
        return 0 <= x < len(data) and 0 <= y < len(data[0]) and data[x][y] == 1

    def dfs(x, y, path):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                data[nx][ny] = 0  # Mark as visited
                path.append([nx, ny])
                dfs(nx, ny, path)

    result = []
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 1:
                path = [[i, j]]
                data[i][j] = 0  # Mark as visited
                dfs(i, j, path)
                result.append(path)

    return result


def image_to_binary_matrix(threshold=100):
    image = ImageGrab.grabclipboard()

    if image is None:
        raise ValueError("No image found in clipboard")

    image = image.convert("L")

    image_array = np.array(image)

    binary_matrix = (image_array < threshold).astype(int)

    return binary_matrix.tolist()


binary_matrix = image_to_binary_matrix()

raw_data = []

for row in binary_matrix:
    raw_data.append(row)

sys.setrecursionlimit(900000)

paths = find_path(raw_data)

time.sleep(2)
start_x, start_y = dir.position()
for path in paths:
    draw_coords_with_mouse(path, start_x, start_y)
