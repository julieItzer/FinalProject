import random

def is_collinear(p1, p2, p3):
    return (p1[0] - p2[0]) * (p3[1] - p2[1]) == (p3[0] - p2[0]) * (p1[1] - p2[1])

def is_valid(board, row, col):
    # Checking if the point we want to put does not create three points on the same line with existing pointsת
    n = len(board)
    points = [(i, j) for i in range(row) for j in range(n) if board[i][j] == 1]
    for p1 in points:
        for p2 in points:
            if p1 != p2 and is_collinear(p1, p2, (row, col)):
                return False
    return True

def place_points(board, row):
    n = len(board)
    if row == n:
        return True  # We have reached the end of the board

    # Attempt to find two valid columns in this row
    columns = list(range(n))
    random.shuffle(columns)  # Random shuffle of the column
    for i in columns:
        for j in columns:
            if i != j and is_valid(board, row, i) and is_valid(board, row, j):
                board[row][i] = 1
                board[row][j] = 1
                if place_points(board, row + 1):
                    return True  # We have found a valid solution, we will continue recursively to the next line
                board[row][i] = 0
                board[row][j] = 0  #Canceling the configuration if we have not found a valid solution
    return False  # We did not find a valid solution for this line

def solve_no_three_in_line(n):
    board = [[0] * n for _ in range(n)]  # Creating an n x n board
    if place_points(board, 0):
        return board
    else:
        return None

# Print the solution
n = 9
solution = solve_no_three_in_line(n)
if solution:
    for row in solution:
        print(" ".join(str(cell) for cell in row))
else:
    print("No solution found")

import matplotlib.pyplot as plt

def plot_board(board):
    n = len(board)
    plt.figure(figsize=(n, n))
    plt.grid(True)
    plt.xticks(range(n))
    plt.yticks(range(n))
    plt.xlim(-0.5, n - 0.5)
    plt.ylim(-0.5, n - 0.5)

    # matrix of the points
    points = [(i, j) for i in range(n) for j in range(n) if board[i][j] == 1]
    for point in points:
        plt.scatter(point[1], n - 1 - point[0], s=200) # Drawing the point on the board

    plt.gca().invert_yaxis() # Flipping the y array so that 0 is at the top of the graph
    plt.show()

    return points

# leaving the functions is collinear, is_valid, place points, solve_no_three_in_line as they are
# ...

# Activating the function to solve and print the board
solution = solve_no_three_in_line(n)
if solution:
    points = plot_board(solution)
    print("Points placed on the board:")
    print(points)
else:
    print("No solution found")
