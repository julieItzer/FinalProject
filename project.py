import itertools
import random
import matplotlib.pyplot as plt

 
def is_collinear(p1, p2, p3):
    # חישוב המכפלה הצלבית
    return (p1[0] - p2[0]) * (p3[1] - p2[1]) == (p3[0] - p2[0]) * (p1[1] - p2[1])


def generate_unique_points(n, max_points):
    chosen_points = set()
    remaining_points = [(x, y) for x in range(n) for y in range(n)]  # יצירת רשימת כל הנקודות
    x_counts = {i: 0 for i in range(n)}  # מעקב אחרי מספר הנקודות בכל שורה
    y_counts = {i: 0 for i in range(n)}  # מעקב אחרי מספר הנקודות בכל עמודה

    # בחירת נקודה באקראיות ובדיקה שהיא לא יוצרת קולינריות עם נקודות קיימות
    while len(chosen_points) < max_points and remaining_points:
        new_point = remaining_points.pop(random.randrange(len(remaining_points)))
        if x_counts[new_point[0]] >= 2 or y_counts[new_point[1]] >= 2:  # כבר יש שתי נקודות בשורה או בעמודה
            continue
        if not any(is_collinear(p1, p2, new_point) for p1, p2 in itertools.combinations(chosen_points, 2)):
            chosen_points.add(new_point)
            x_counts[new_point[0]] += 1
            y_counts[new_point[1]] += 1

    # החזרת כל הנקודות שנבחרו
    return chosen_points


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
