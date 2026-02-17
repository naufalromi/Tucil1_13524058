import sys
import time
import string

grid = []
region = {}

filename = input("Insert txt name: ")

try:
    with open(filename, "r") as f:
        for line in f:
            row = list(line.strip())
            if row:
                grid.append(row)
            for char in row:
                if char not in string.ascii_uppercase:
                    print(f"Invalid character '{char}'")
                    sys.exit()
except FileNotFoundError:
    print("File not found.")
    sys.exit()

N = len(grid)

if not all(len(row) == N for row in grid):
    print("Grid isn't square.")
    sys.exit()

for r in range(N):
    for c in range(N):
        color = grid[r][c]
        id = (r * N) + c
        
        if color not in region:
            region[color] = []
        region[color].append(id)

if len(region) != N:
    print(f"Found {len(region)} region, expected {N}")
    sys.exit()

update = input("Enter how long each update in n-th iteration (0 for none): ")
try:
    update = int(update)
    if update < 0: update = 0
except ValueError:
    update = 0

graph = [[False for _ in range(N*N)] for _ in range(N*N)]

for id1 in range(N*N):
    r1, c1 = id1 // N, id1 % N
    color1 = grid[r1][c1]
    
    for id2 in range(id1 + 1, N*N):
        r2, c2 = id2 // N, id2 % N
        color2 = grid[r2][c2]
        
        if color1 == color2:
            graph[id1][id2] = True
            graph[id2][id1] = True
            continue

        row_dist = r1 - r2 if r1 > r2 else r2 - r1
        col_dist = c1 - c2 if c1 > c2 else c2 - c1
        
        if row_dist <= 1 and col_dist <= 1:
            graph[id1][id2] = True
            graph[id2][id1] = True

p = [0] * N
iterations = 0
grid_solution = None
start = time.time()

while True:
    iterations += 1
    duplicate = False
    for i in range(N):
        for j in range(i + 1, N):
            if p[i] == p[j]:
                duplicate = True
                break
        if duplicate:
            break

    if not duplicate:
        valid = True
        for r1 in range(N):
            for r2 in range(r1 + 1, N):
                id1 = (r1 * N) + p[r1]
                id2 = (r2 * N) + p[r2]
                if graph[id1][id2]:
                    valid = False
                    break
            if not valid: 
                break
        if valid:
            grid_solution = list(p)
            break
    
    if (update > 0) and (iterations % update == 0):
        print(f"\nIterations: {iterations}")
        for r in range(N):
            row_str = ""
            for c in range(N):
                if p[r] == c:
                    row_str += "# "
                else:
                    row_str += grid[r][c] + " "
            print(row_str)
        print("\n\n")

    d = N - 1
    while d >= 0:
        p[d] += 1 
        if p[d] < N:
            break 
        else:
            p[d] = 0 
            d -= 1    
    if d < 0:
        break

duration = time.time() - start

if grid_solution:
    solution = "Solution\n"
    solution += "="*N*2 + "\n"
    for r in range(N):
        row = ""
        for c in range(N):
            row += "# " if grid_solution[r] == c else grid[r][c] + " "
        solution += row.rstrip() + "\n"
    solution += "="*N
    solution += f"\n\nTotal iterations: {iterations}\nDuration: {duration:.4f} seconds\n"
else:
    solution = f"No solution found\nTotal Iterations: {iterations}\nDuration: {duration:.4f} seconds"

print(solution)
save = input("\nDo you want to save the answer? (Y if want to save): ")
if save == 'Y':
    path = input("Directory path: ")
    with open(path, "w") as f:
        f.write(solution)
    print(f"\nSaved to: {path}")
else:
    print("Answer isn't saved")