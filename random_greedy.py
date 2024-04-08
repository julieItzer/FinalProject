import random
import itertools
import matplotlib.pyplot as plt

def is_collinear(p1, p2, p3):
    return (p1[0] - p2[0]) * (p3[1] - p2[1]) == (p3[0] - p2[0]) * (p1[1] - p2[1])

def generate_unique_points(n, max_points):
    points = [(x, y) for x in range(n) for y in range(n)]
    non_diagonal_points = [p for p in points if p[0] != p[1] and p[0] != n - 1 - p[1]]
    diagonal_points = [p for p in points if p[0] == p[1] or p[0] == n - 1 - p[1]]

    chosen_points = set()

    # בחר תחילה נקודות שאינן על אלכסונים
    while non_diagonal_points and len(chosen_points) < max_points:
        p = random.choice(non_diagonal_points)
        if is_valid_point(chosen_points, p):
            chosen_points.add(p)
        non_diagonal_points.remove(p)

    # אם יש עוד מקום, בחר נקודות מהאלכסונים
    while diagonal_points and len(chosen_points) < max_points:
        p = random.choice(diagonal_points)
        if is_valid_point(chosen_points, p):
            chosen_points.add(p)
        diagonal_points.remove(p)

    return chosen_points

def is_valid_point(chosen_points, new_point):
    # בדוק שהנקודה החדשה לא יוצרת שלוש נקודות קולינאריות
    for p1, p2 in itertools.combinations(chosen_points, 2):
        if is_collinear(p1, p2, new_point):
            return False
    return True

# יצירת הנקודות
n = 60
max_points = 2 * n
unique_points = generate_unique_points(n, max_points)



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