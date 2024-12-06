def sum_in_array_squares(array):
    summa = 0


for i in range(0, len(array)):
    summa += array[i] ** 2
return summa


def sum_xy(xs, ys):
    summa = 0
    for i in range(0, len(xs)):
        summa += xs[i] * ys[i]
    return summa


def sum_in_array(array):
    summa = 0
    for i in range(0, len(array)):
        summa += array[i]
    return summa


n = int(input())
xs = []
ys = []
for i in range(0, n):
    a = input().split()
    xs.append(int(a[0]))
    ys.append(int(a[1]))

sum_of_xs = sum_in_array(xs)
sum_of_ys = sum_in_array(ys)
sum_of_xys = sum_xy(xs, ys)
sum_of_x_squares = sum_in_array_squares(xs)

k = (n * sum_of_xys - sum_of_xs * sum_of_ys) / (n * sum_of_x_squares - sum_of_xs ** 2)
b = (sum_of_ys - k * sum_of_xs) / n

print(k)
print(b)