from sklearn.neighbors import KNeighborsClassifier
import numpy as np

tr = np.array([
    [2.0, 4.0, 0],
    [4.0, 4.0, 0],
    [4.0, 6.0, 1],
    [6.0, 2.0, 1]
])

x = tr[:, :-1]
y = tr[:, -1]

ts = np.array([5.0, 5.0]).reshape(1, -1)

k = 3
m = KNeighborsClassifier(n_neighbors=k)
m.fit(x, y)

print(m.predict(ts))
