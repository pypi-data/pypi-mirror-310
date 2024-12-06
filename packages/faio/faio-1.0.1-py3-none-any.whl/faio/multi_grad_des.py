#Made by Askar


#f(w, b) = w1 * x1 + w2 * x2 + w3 * x3 + ... + b
#df_dw_i = 2 * sum((w1 * x1 + w2 * x2 + ... + b - y) * xi) / n
#df_db = 2 * sum(w1 * x1 + w2 * x2 + ... + b - y) / n
#sum_all = (w1 * x1 + w2 * x2 + ... + b - y)
#cost_function = (w1 * x1 + w2 * x2 + ... + b - y)^2

def df_dw (xs, ys, ws, b):
    n1 = len(ws)
    n2 = len(ys)
    df_dw = []
    for i in range(n1):
        df_dw.append(0)
#df_dw = [0, 0, 0, ...]
    for x, y in zip(xs, ys):
        sum_all = sum(w * x_i for w, x_i in zip(ws, x)) + b
        sum_all -= y
        for i in range(n1):
            df_dw[i] += sum_all * x[i]
# df_dw = [sum_all • x_1, sum_all • x_2, sum_all • x_3, ...]
    df_dw = [2 * df_dw_i / n2 for df_dw_i in df_dw]
    return df_dw
# df_dw = [2 * sum_all • x_1 / n, 2 * sum_all • x_2 / n, 2 * sum_all • x_3 / n, ...]

def df_db (xs, ys, ws, b):
    sum_all = 0
    for x, y in zip(xs, ys):
        sum_all += sum(w * x_i for w, x_i in zip(ws, x)) + b
        sum_all -= y
    df_db = 2 * sum_all / len(ys)
    return df_db

def cost_function(xs, ys, ws, b):
    cost_function = 0
    for x, y in zip(xs, ys):
        sum_all = sum(w * x_i for w, x_i in zip(ws, x)) + b
        sum_all -= y
        cost_function += (sum_all ** 2)
    return cost_function

lr_w = 0.001
lr_b = 0.001

limit = 1000

xs = []
ys = []

n = int(input())

for i in range(n):
    x_input = map(float, input().split(" ")) # "750 12.3 0.75 1"
    x = [x_input_num for x_input_num in x_input]
    xs.append(x)
    # xs = [ [750, 12.3, 0.75, 1], [ ... ], ... ]
    y_input = float(input())
    ys.append(y_input)

temp_ws = [0] * len(xs[0])
temp_b = 0

ws = [0] * len(xs[0])
b = 0

for _ in range(limit):
    df_dws = df_dw(xs, ys, ws, b)
    temp_ws = [w - lr_w * df_dw_i for w, df_dw_i in zip(ws, df_dws)]
    temp_b = b - lr_b * df_db(xs, ys, ws, b)
    ws = temp_ws
    b = temp_b
    #print("ws:", ws, "| b:", b, "| cost function:", cost_function(xs, ys, ws, b))

print("ws:", ws)
print("b:", b)
print("cost function:", cost_function(xs, ys, ws, b))