import math

class Tree:
    def __init__(self):
        self.t = None

    def _e(self, y):
        c = {}
        for l in y:
            c[l] = c.get(l, 0) + 1
        t = len(y)
        return -sum((v / t) * math.log2(v / t) for v in c.values())

    def _s(self, x, y, f):
        v = set(r[f] for r in x)
        s = {}
        for val in v:
            s[val] = [i for i, r in enumerate(x) if r[f] == val]
        return s

    def _bf(self, x, y):
        e = self._e(y)
        bg, bf = -1, None
        for f in range(len(x[0])):
            s = self._s(x, y, f)
            g = e
            for idx in s.values():
                sy = [y[i] for i in idx]
                g -= len(idx) / len(y) * self._e(sy)
            if g > bg:
                bg, bf = g, f
        return bf

    def _bt(self, x, y):
        if len(set(y)) == 1:
            return y[0]
        if not x[0]:
            return max(set(y), key=y.count)
        bf = self._bf(x, y)
        t = {bf: {}}
        s = self._s(x, y, bf)
        for v, idx in s.items():
            sx = [[r[i] for i in range(len(r)) if i != bf] for i, r in enumerate(x) if i in idx]
            sy = [y[i] for i in idx]
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
            if v not in b:
                k = sorted(b.keys())
                if v < k[0]:
                    return tr(b[k[0]], r)
                if v > k[-1]:
                    return tr(b[k[-1]], r)
            return tr(b[v], r)

        return [tr(self.t, r) for r in x]

m = Tree()
x = [[1], [2], [3], [4], [5], [100], [200], [300], [400]]
y = [1, 2, 3, 4, 5, 100, 200, 300, 400]

x1 = [[100], [200], [300], [500], [600]]

m.fit(x, y)
print(m.predict(x1))
