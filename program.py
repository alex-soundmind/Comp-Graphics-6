import matplotlib.pyplot as plt

def cohen_sutherland(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    INSIDE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8

    def compute_code(x, y):
        code = INSIDE
        if x < x_min:
            code |= LEFT
        elif x > x_max:
            code |= RIGHT
        if y < y_min:
            code |= BOTTOM
        elif y > y_max:
            code |= TOP
        return code

    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    while True:
        if code1 == INSIDE and code2 == INSIDE:
            return True, x1, y1, x2, y2
        elif code1 & code2 != 0:
            return False, None, None, None, None
        elif code1 != INSIDE:
            if code1 & TOP != 0:
                x1 = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y1 = y_max
            elif code1 & BOTTOM != 0:
                x1 = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y1 = y_min
            elif code1 & RIGHT != 0:
                y1 = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x1 = x_max
            elif code1 & LEFT != 0:
                y1 = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x1 = x_min
            code1 = compute_code(x1, y1)
        else:
            if code2 & TOP != 0:
                x2 = x2 + (x1 - x2) * (y_max - y2) / (y1 - y2)
                y2 = y_max
            elif code2 & BOTTOM != 0:
                x2 = x2 + (x1 - x2) * (y_min - y2) / (y1 - y2)
                y2 = y_min
            elif code2 & RIGHT != 0:
                y2 = y2 + (y1 - y2) * (x_max - x2) / (x1 - x2)
                x2 = x_max
            elif code2 & LEFT != 0:
                y2 = y2 + (y1 - y2) * (x_min - x2) / (x1 - x2)
                x2 = x_min
            code2 = compute_code(x2, y2)

def midpoint_clipping(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    def compute_midpoint(x1, y1, x2, y2):
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def is_inside(x, y):
        return x_min <= x <= x_max and y_min <= y <= y_max

    mid_x, mid_y = compute_midpoint(x1, y1, x2, y2)

    if is_inside(mid_x, mid_y):
        return True, x1, y1, x2, y2
    else:
        if not is_inside(x1, y1) and not is_inside(x2, y2):
            return False, None, None, None, None
        elif not is_inside(x1, y1):
            x1, y1 = mid_x, mid_y
        else:
            x2, y2 = mid_x, mid_y
        return midpoint_clipping(x1, y1, x2, y2, x_min, y_min, x_max, y_max)

def main():
    print("Выберите алгоритм:")
    print("1. Алгоритм Сазерленда-Коэна")
    print("2. Алгоритм разбиения средней точкой")
    choice = int(input("Введите ваш выбор: "))

    x_min, y_min, x_max, y_max = map(int, input("Введите координаты окна (x_min y_min x_max y_max): ").split())
    x1, y1, x2, y2 = map(int, input("Введите координаты отрезка (x1 y1 x2 y2): ").split())

    if choice == 1:
        visible, x1, y1, x2, y2 = cohen_sutherland(x1, y1, x2, y2, x_min, y_min, x_max, y_max)
    elif choice == 2:
        visible, x1, y1, x2, y2 = midpoint_clipping(x1, y1, x2, y2, x_min, y_min, x_max, y_max)
    else:
        print("Неверный выбор")
        return

    if visible:
        plt.plot([x1, x2], [y1, y2], 'b-')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.gca().set_aspect('equal')
        plt.show()
    else:
        print("Отрезок не виден")

if __name__ == "__main__":
    main()