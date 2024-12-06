# Given two arrays: x = [randoms], y = w*x + b + error
# Find closest w and b

import random

number_of_dots = 10
x = [random.random() * 100 for _ in range(number_of_dots)]
# Код на с++ делает то же самое:
# int x[10]
# for(int i = 0; i < 10; i++){
#     x[i] = rand() * 100;
# }
# print(x)
w = random.random() * 20
b = random.random() * 50
y = [w * xi + b + random.random() * (-1 ** (random.random() > 0.5)) for xi in x]


# print(y)

# Let's look at the graph of the cost function (MSE), which is 3d graph
# with axis w, b and cf (cost function)

# Get a random w and b, we will set them as 0 and 0
# Update w and b simultaneusly
# by subtracting derrivative in the current dot

# Alpha is coefficent for a step (learning rate)
# We will start with alpha = 0.01

def cost_function(x, y, w, b):
    summ = 0
    for xi, yi in zip(x, y):
        summ += (yi - (w * xi + b)) ** 2
    return summ / len(x)


def dfdw(x, y, w, b):
    summ = 0
    for xi, yi in zip(x, y):
        summ += (yi - (w * xi + b)) * xi
    return -2 * summ / len(x)


def dfdb(x, y, w, b):
    summ = 0
    for xi, yi in zip(x, y):
        summ += (yi - (w * xi + b))
    return -2 * summ / len(x)


w = 0.0
b = 0.0
alphaB = 0.0001
alphaW = 0.1
copy_w = w
for _ in range(100):
    copy_w = w - alphaW * dfdw(x, y, w, b)
    b -= alphaB * dfdb(x, y, w, b)
    w = copy_w
    current_cost = cost_function(x, y, w, b)
    print("w: ", w, " | b: ", b, " | cost: ", current_cost)