import random

def is_collinear(p1, p2, p3):
    # חישוב המכפלה סקלרית
    return (p1[0] - p2[0]) * (p3[1] - p2[1]) == (p3[0] - p2[0]) * (p1[1] - p2[1])

def is_valid(board, row, col):
    # בדיקה אם הנקודה שאנו רוצים לשים אינה יוצרת שלוש נקודות על אותו קו עם נקודות קיימות
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
        return True  # הגענו לסוף הלוח

    # ניסיון למצוא שתי עמודות חוקיות בשורה זו
    columns = list(range(n))
    random.shuffle(columns)  # ערבוב רנדומלי של העמודות
    for i in columns:
        for j in columns:
            if i != j and is_valid(board, row, i) and is_valid(board, row, j):
                board[row][i] = 1
                board[row][j] = 1
                if place_points(board, row + 1):
                    return True  # מצאנו פתרון חוקי, נמשיך רקורסיבית לשורה הבאה
                board[row][i] = 0
                board[row][j] = 0  # ביטול התצורה אם לא מצאנו פתרון חוקי
    return False  # לא מצאנו פתרון חוקי עבור שורה זו

def solve_no_three_in_line(n):
    board = [[0] * n for _ in range(n)]  # יצירת לוח n x n
    if place_points(board, 0):
        return board
    else:
        return None

# הדפסת הפתרון
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

    # מטריצה של הנקודות
    points = [(i, j) for i in range(n) for j in range(n) if board[i][j] == 1]
    for point in points:
        plt.scatter(point[1], n - 1 - point[0], s=200) # ציור הנקודה על הלוח

    plt.gca().invert_yaxis() # הפיכת מערך ה-y כדי ש-0 יהיה בחלק העליון של הגרף
    plt.show()

    return points

# השארת הפונקציות is_collinear, is_valid, place_points, solve_no_three_in_line כפי שהן
# ...

# הפעלת הפונקציה לפתרון והדפסת הלוח
solution = solve_no_three_in_line(n)
if solution:
    points = plot_board(solution)
    print("Points placed on the board:")
    print(points)
else:
    print("No solution found")