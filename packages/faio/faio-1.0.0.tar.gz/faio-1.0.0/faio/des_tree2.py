import numpy as np

class Tree:
    def __init__(self):
        self.t = None

    def _e(self, y):
        _, c = np.unique(y, return_counts=True)
        p = c / len(y)
        return -np.sum(p * np.log2(p))

    def _s(self, x, y, f):
        v = np.unique(x[:, f])
        return {val: np.where(x[:, f] == val)[0] for val in v}

    def _bf(self, x, y):
        e = self._e(y)
        bg, bf = -1, None
        for f in range(x.shape[1]):
            s = self._s(x, y, f)
            g = e
            for idx in s.values():
                g -= len(idx) / len(y) * self._e(y[idx])
            if g > bg:
                bg, bf = g, f
        return bf

    def _bt(self, x, y):
        if len(np.unique(y)) == 1:
            return y[0]
        if x.shape[1] == 0:
            return np.bincount(y).argmax()
        bf = self._bf(x, y)
        t = {bf: {}}
        s = self._s(x, y, bf)
        for v, idx in s.items():
            sx = np.delete(x[idx], bf, axis=1)
            sy = y[idx]
            t[bf][v] = self._bt(sx, sy)
        return t

    def fit(self, x, y):
        self.t = self._bt(x, y)

    def predict(self, x):
        def tr(t, r):
            if not isinstance(t, dict):
                return t
            f, b = next(iter(t.items()))
            v = r[f]
            k = sorted(b.keys())
            if v < k[0]:
                return tr(b[k[0]], r)
            if v > k[-1]:
                return tr(b[k[-1]], r)
            return tr(b[v], r)

        return np.array([tr(self.t, r) for r in x])

m = Tree()

x = np.array([[1], [2], [3], [4], [5], [100], [200], [300], [400]])
y = np.array([1, 2, 3, 4, 5, 100, 200, 300, 400])

x1 = np.array([[100], [200], [300], [500], [600], [0]])

m.fit(x, y)
print(m.predict(x1))
