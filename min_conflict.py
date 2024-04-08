import itertools
import random
import matplotlib.pyplot as plt
import numpy as np
from pyparsing import empty


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
    # יצירת מטריצה של אפסים עם הגודל המבוקש
    matrix = np.zeros((n, n))

    # עדכון המטריצה: עבור כל נקודה, שים -1 במיקום המתאים
    for point in points:
        # x, y = point
        matrix[point] = -1

    return matrix

def find_min_values_positions(matrix, num):
    # יצירת רשימה של כל הנקודות והערכים שלהן, למעט אלו עם ערך 0
    points_values = [(i, j, matrix[i][j]) for i in range(len(matrix)) for j in range(len(matrix[0]))
                     if matrix[i][j] >= 0]

    # מיון הרשימה לפי הערך בכל נקודה
    points_values.sort(key=lambda x: x[2])

    # מציאת num הערכים המינימליים
    min_positions = [(i, j) for i, j, value in points_values[:num]]
    #if min_positions[0] != 0:
        #random.shuffle(min_positions)# מערבב את הרשימה של המינימליים

    return min_positions

# הפונקציה תחזיר נקודה אשר נמצאת בקונפליקט עם הנקודה שהפונקציה מקבלת
def Finding_the_points_of_conflict(conPoints, points):
    for p1, p2 in itertools.combinations(points, 2):
        if is_collinear(p1, p2, conPoints):
            l = [p1, p2]
            return random.choice(l)

def fix_points (unique_points, conflicts):
    maxattempts = 1
    #extraPoint = random.choice(conflicts)# בחירת נקודה אקראית עם מעט קונפליקטים
    #unique_points.add(extraPoint)
    while maxattempts <= 10:
        #conPoint = Finding_the_points_of_conflict(extraPoint, unique_points) # הגרלת נקודה אחת שנמצאת בקונפליקט עם extraPoint
        #if conPoint == None:  #אין עוד קונפליקטים בגרף
           # break
        extraPoint = conflicts[0] #random.choice(conflicts)  # בחירת נקודה אקראית עם מעט קונפליקטים
        conPoint = Finding_the_points_of_conflict(extraPoint, unique_points)  # הגרלת נקודה אחת שנמצאת בקונפליקט עם extraPoint
        unique_points.add(extraPoint)
        if conPoint == None:  #אין עוד קונפליקטים בגרף
            break
        unique_points.remove(conPoint)
        matrix=create_matrix_from_points(unique_points) # אתחול מטריצה
        matrix = count_collinear_points(matrix, unique_points, n)
        conflicts = find_min_values_positions(matrix, int(0.4*n))
        if matrix[conflicts[0]] == 0: #ישנה נקודה שאינה נמצאת בקונפליקטים
            unique_points.add(conflicts[0])
            break
        #if len(conflicts) == 0:
           # break
        #extraPoint = random.choice(conflicts)
        #unique_points.add(extraPoint)
        maxattempts += 1
    print(maxattempts)

# יצירת הנקודות
n = 60
max_points = 2 * n
unique_points = generate_unique_points(n, max_points)
print(unique_points)
#matrix = np.zeros((n, n)) #אתחול מטריצה
matrix = create_matrix_from_points(unique_points)
matrix = count_collinear_points(matrix, unique_points, n)
conflicts = find_min_values_positions(matrix, int(0.4*n))
#print(conflicts)
#print(matrix)
print(len(unique_points))
fix_points(unique_points, conflicts)
#print(matrix)
# הצגה גרפית של הנק;ודות
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