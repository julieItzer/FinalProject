import itertools
import random
import matplotlib.pyplot as plt
import numpy as np

def is_collinear(p1, p2, p3):
    # Calculating a scalar product
    return (p1[0] - p2[0]) * (p3[1] - p2[1]) == (p3[0] - p2[0]) * (p1[1] - p2[1])

def generate_unique_points(n, max_points):
    #A function randomizes points and adds to the list all points that meet the conditions of the problem
    chosen_points = set()
    remaining_points = [(x, y) for x in range(n) for y in range(n)]  # Creating a list of all possible points
    x_counts = {i: 0 for i in range(n)}  # Tracking the number of points in each row
    y_counts = {i: 0 for i in range(n)}  # Tracking the number of points in each column

    # Choosing a point at random and checking that it does not create collinearity with existing points
    while len(chosen_points) < max_points and remaining_points:
        k = random.randint(0, len(remaining_points)-1)
        new_point = remaining_points[k]
        remaining_points[k] = remaining_points[-1]
        remaining_points.pop()
        if x_counts[new_point[0]] >= 2 or y_counts[new_point[1]] >= 2:  # There are already two points in the row or column
            continue
        if not any(is_collinear(p1, p2, new_point) for p1, p2 in itertools.combinations(chosen_points, 2)):
            chosen_points.add(new_point)
            x_counts[new_point[0]] += 1
            y_counts[new_point[1]] += 1

    # Returning all selected points
    return chosen_points

def count_collinear_points(matrix, unique_points, n):
    # For each pair of points, check which other points form a collinear line
    for i in range(n):
        for j in range(n):
            for p1, p2 in itertools.combinations(unique_points, 2):
                if (p1 == (i,j) or p2 == (i,j)):
                    continue
                if (p1[0] == p2[0] and p2[0] == i) or (p1[1] == p2[1] and p2[1] == j):
                    matrix[i, j] += 1
                else:
                    if is_collinear(p1, p2, (i, j)):
                        matrix[i, j] += 1
    return matrix

def create_matrix_from_points(points):
    # Creating a matrix of zeros with the requested size
    matrix = np.zeros((n, n))

    # Updating the matrix: for each point, put -1 in the appropriate place
    for point in points:
        # x, y = point
        matrix[point] = -1

    return matrix

def find_zeros(matrix):
    positions = []  # A list to collect the positions of the zeros and ones
    for i, row in enumerate(matrix):  # Loop over each row and row index
        for j, value in enumerate(row):  # Loop over each column index value in a row
            if value == 1 or value == 0:
                positions.append((i, j))  # Adding the position of the zero and one to the list
    positions_sorted = sorted(positions, key=lambda x: (x[0], x[1]))
    return positions_sorted

def find_min_values_positions(matrix, num):
    # Creating a list of all the points and their values, except those with a value of 0
    points_values = [(i, j, matrix[i][j]) for i in range(len(matrix)) for j in range(len(matrix[0]))
                     if matrix[i][j] >= 0]

    # Sort list by value at each point
    points_values.sort(key=lambda x: x[2])

    # Finding the minimum num values
    min_positions = [(i, j) for i, j, value in points_values[:num]]

    return min_positions

# The function will return a point that is in conflict with the point the function receives
def Finding_the_points_of_conflict(conPoints, points):
    for p1, p2 in itertools.combinations(points, 2):
        if is_collinear(p1, p2, conPoints):
            l = [p1, p2]
            return random.choice(l)

def fix_points (unique_points, conflicts):
    #Implementation of minconflicts algorithm
    maxattempts = 1
    while maxattempts <= 10:
        if conflicts[0] == 0 or len(unique_points) == len(conflicts) == 1:
            extraPoint = conflicts[0] #Select a point with 0 conflicts
        else:
            pos = random.randint(0, len(conflicts) - 1)
            extraPoint = conflicts[pos]  # Random point selection with few conflicts
        conPoint = Finding_the_points_of_conflict(extraPoint, unique_points)  # One point draw that is in conflict with extraPoint
        unique_points.add(extraPoint)
        if conPoint == None:  #There are no more conflicts in the graph
            break
        unique_points.remove(conPoint)
        matrix=create_matrix_from_points(unique_points) # initialization matrix
        matrix = count_collinear_points(matrix, unique_points, n)
        conflicts = find_zeros(matrix)
        if matrix[conflicts[0]] == 0: #There is a point that is not in conflicts
            unique_points.add(conflicts[0])
            break
        maxattempts += 1
    print(maxattempts)

# creating the points
n = 100
max_points = 2 * n
unique_points = generate_unique_points(n, max_points)
print(unique_points) #Prints the collection of points selected by the random algorithm
matrix = create_matrix_from_points(unique_points)
matrix = count_collinear_points(matrix, unique_points, n)
conflicts = find_zeros(matrix)
print(len(unique_points))
temp = 0
while(temp < 50 and len(unique_points) / n <= 1.7):
    temp += 1
    fix_points(unique_points, conflicts)
    matrix = create_matrix_from_points(unique_points)
    matrix = count_collinear_points(matrix, unique_points, n)
    conflicts = find_zeros(matrix)
    print(len(unique_points))


# Graphical presentation of the points
x_values = [point[0] for point in unique_points]
y_values = [point[1] for point in unique_points]

print(unique_points) #Printing the selected points after using the minconflicts algorithm
print(len(unique_points))
print(len(unique_points)/n)
plt.figure(figsize=(5, 5))
plt.scatter(x_values, y_values)
plt.xlim(0, n-1)
plt.ylim(0, n-1)
plt.xticks(range(n))
plt.yticks(range(n))
plt.grid(True)
plt.title(f'Unique Points on a {n}x{n} Grid')
plt.show()