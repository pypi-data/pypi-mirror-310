import math
from collections import Counter

def dist(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def knn(t, p, k):
    d = [(dist(p, r[:-1]), r[-1]) for r in t]
    d.sort(key=lambda x: x[0])
    n = [lbl for _, lbl in d[:k]]
    return Counter(n).most_common(1)[0][0]

tr = [
    [2.0, 4.0, 0],
    [4.0, 4.0, 0],
    [4.0, 6.0, 1],
    [6.0, 2.0, 1]
]

ts = [5.0, 5.0]
k = 3
print(knn(tr, ts, k))
