
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

matrix = [[0 for x in range (0,15)]for y in range(0,11)]
grid = Grid(matrix=matrix)
matrix[0][1] = 1
matrix[1][1] = 1

grid = Grid(matrix=matrix)

start = grid.node(0, 0)
end = grid.node(14,10)

finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, runs = finder.find_path(start, end, grid)
for y in range(0,11):
    print(matrix[y])

print('operations:', runs, 'path length:', len(path))
print(grid.grid_str(path=path, start=start, end=end))