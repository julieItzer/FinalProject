import itertools
import random
import matplotlib.pyplot as plt
import numpy as np


def is_collinear(p1, p2, p3):
    # חישוב המכפלה סקלרית
    return (p1[0] - p2[0]) * (p3[1] - p2[1]) == (p3[0] - p2[0]) * (p1[1] - p2[1])

def generate_unique_points(n, max_points):
    chosen_points = set()
    remaining_points = [(x, y) for x in range(n) for y in range(n)]  # יצירת רשימת כל הנקודות
    x_counts = {i: 0 for i in range(n)}  # מעקב אחרי מספר הנקודות בכל שורה
    y_counts = {i: 0 for i in range(n)}  # מעקב אחרי מספר הנקודות בכל עמודה

    # בחירת נקודה באקראיות ובדיקה שהיא לא יוצרת קולינריות עם נקודות קיימות
    while len(chosen_points) < max_points and remaining_points:
        k = random.randint(0, len(remaining_points)-1)
        new_point = remaining_points[k]
        remaining_points[k] = remaining_points[-1]
        remaining_points.pop()
        #new_point = remaining_points.pop(random.randrange(len(remaining_points)))
        if x_counts[new_point[0]] >= 2 or y_counts[new_point[1]] >= 2:  # כבר יש שתי נקודות בשורה או בעמודה
            continue
        if not any(is_collinear(p1, p2, new_point) for p1, p2 in itertools.combinations(chosen_points, 2)):
            chosen_points.add(new_point)
            x_counts[new_point[0]] += 1
            y_counts[new_point[1]] += 1

    # החזרת כל הנקודות שנבחרו
    return chosen_points

def count_collinear_points(matrix, unique_points, n):
    # עבור כל זוג נקודות, בדוק אילו נקודות נוספות יוצרות ישר קולינרי
    for i in range(n):
        for j in range(n):
            if (i, j) not in unique_points:
                for p1, p2 in itertools.combinations(unique_points, 2):
                      if is_collinear(p1, p2, (i, j)):
                        matrix[i, j] += 1
    return matrix

def find_min_values_positions(matrix, num):
    # יצירת רשימה של כל הנקודות והערכים שלהן, למעט אלו עם ערך 0
    points_values = [(i, j, matrix[i][j]) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j] != 0]

    # מיון הרשימה לפי הערך בכל נקודה
    points_values.sort(key=lambda x: x[2])

    # מציאת num הערכים המינימליים
    min_positions = [(i, j) for i, j, value in points_values[:num]]

    return min_positions

def min_conflicts(points, n):
    """
    def find_collinear_point():
        # מחפשת נקודה שהיא חלק מקו קולינרי עם שתי נקודות נוספות
        for point in points:
            for p1, p2 in itertools.combinations(points, 2):
                if point != p1 and point != p2 and is_collinear(point, p1, p2):
                    return point
        return None
        """

    max_steps = 100
    """""
    for _ in range(max_steps):
        collinear_point = find_collinear_point()
        if collinear_point is None:
            # אם לא נמצאו נקודות קולינריות, הפתרון תקין
            return points
            """


        #points.remove(collinear_point)
    new_point = (random.randint(0, n-1), random.randint(0, n-1))
    while any(is_collinear(new_point, p1, p2) for p1, p2 in itertools.combinations(points, 2)):
        new_point = (random.randint(0, n-1), random.randint(0, n-1))
        points.append(new_point)

    # אם הגענו למספר הצעדים המקסימלי ללא פתרון תקין, מחזירים None
    return None

def can_place_point(p, placed_points, i):
    # Function to check if a point can be placed without violating the constraint
    for j in range(len(placed_points)):
        if i == j:
            continue
        if is_collinear(placed_points[i], p,placed_points[j] ):
                return False
    return True

def backtrack(points, placed_points, idx):
    if idx == len(points):
        return True

    for i in range(len(placed_points)):
        if can_place_point(points[idx], placed_points, i):
            placed_points.add(points[idx])
            if backtrack(points, placed_points, idx + 1):
                return True
            placed_points[i].pop()
    placed_points.add(points[idx])
    if backtrack(points, placed_points, idx + 1):
        return True
    placed_points.pop()
    return False


def fix_points(points):
    while True:
        placed_points = set()
        if backtrack(points, placed_points, 0):
            return placed_points
        else:
            # If backtracking fails, remove a random problematic point and retry
            problematic_points = [point for point in points if not can_place_point(point, placed_points)]
            if not problematic_points:
                return None  # No solution found
            else:
                # Remove a random problematic point
                points.remove(random.choice(problematic_points))

# יצירת הנקודות
n = 10
max_points = 2 * n
unique_points = generate_unique_points(n, max_points)
print(unique_points)
matrix = np.zeros((n, n)) #אתחול מטריצה
matrix = count_collinear_points(matrix, unique_points, n)
conflicts = find_min_values_positions(matrix, int(0.2*n))
print(conflicts)
for i in range (len(conflicts)):
    unique_points.add(conflicts[i])
print("help")
#min_conflicts(unique_points,n)
#fix_points(list(unique_points))
# הצגה גרפית של הנקודות
x_values = [point[0] for point in unique_points]
y_values = [point[1] for point in unique_points]

print(unique_points)
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