from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import ArenaMap
layout = ArenaMap.MazeLayout(15,11,"*#*#*#*#A0507A0604D0206B0001D1302D1000A1307*0003*0303*0405*1107*0600*1104*0705*1317*#")
matrix = [[0 for x in range (0,15)]for y in range(0,11)]
for y in range(0,11):
    for x in range(0,15):
        if layout.blockedAt(x,y) == True:
            matrix[y][x] = 1
grid = Grid(matrix=matrix)

for y in range(0,11):
    print(matrix[y])
start = grid.node(11, 2)# (x,y)
end = grid.node(3,10)

finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, runs = finder.find_path(start, end, grid)

print('operations:', runs, 'path length:', len(path))
print(grid.grid_str(path=path, start=start, end=end))
