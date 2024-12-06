import numpy
class SVM:
    def __init__(self, lr=0.1, ep=10000, c=1.0):
        self.lr = lr
        self.ep = ep
        self.c = c
        self.w = None
        self.b = None

    def fit(self, x, y):
        n, m = len(x), len(x[0])
        self.w = [0] * m
        self.b = 0
        for _ in range(self.ep):
            for i in range(n):
                cond = y[i] * (self._dot(x[i], self.w) + self.b) >= 1
                if cond:
                    for j in range(m):
                        self.w[j] -= self.lr * (2 / self.ep * self.w[j])
                else:
                    for j in range(m):
                        self.w[j] -= self.lr * (2 / self.ep * self.w[j] - self.c * y[i] * x[i][j])
                    self.b -= self.lr * self.c * y[i]

    def predict(self, x):
        return np.sign(np.dot(x, self.w) + self.b)

x = [[2, 3], [1, 1], [2, 2], [3, 3], [5, 5]]
y = [1, -1, 1, 1, -1]
xt = [[1.5, 2], [4, 4], [5, 6]]

svm1 = SVM()
svm1.fit(x, y)
print(svm1.predict(xt))
