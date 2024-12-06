import numpy as np
from collections import Counter

def dist(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

def knn(t, p, k):
    pts = t[:, :-1]
    lbls = t[:, -1]
    d = np.linalg.norm(pts - p, axis=1)
    idx = np.argsort(d)[:k]
    return Counter(lbls[idx]).most_common(1)[0][0]

tr = np.array([
    [2.0, 4.0, 0],
    [4.0, 4.0, 0],
    [4.0, 6.0, 1],
    [6.0, 2.0, 1]
])

ts = np.array([5.0, 5.0])
k = 3
print(knn(tr, ts, k))
