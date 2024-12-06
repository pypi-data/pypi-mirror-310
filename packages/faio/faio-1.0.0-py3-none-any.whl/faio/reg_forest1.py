import random
import numpy as np

class RandomForestRegressor:
    def __init__(self, n_trees, max_depth, min_size):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_size = min_size
        self.forest = []

    def fit(self, X, y):
        for _ in range(self.n_trees):
            X_s, y_s = self._bootstrap_sample(X, y)
            tree = self._build_tree(X_s, y_s)
            self.forest.append(tree)

    def predict(self, X):
        predictions = [self._predict_tree(tree, x) for tree in self.forest for x in X]
        return [sum(p) / len(p) for p in zip(*predictions)]

    def _bootstrap_sample(self, X, y):
        indices = [random.randint(0, len(X) - 1) for _ in range(len(X))]
        return [X[i] for i in indices], [y[i] for i in indices]

    def _build_tree(self, X, y, depth=0):
        if len(set(y)) == 1 or depth >= self.max_depth or len(X) <= self.min_size:
            return sum(y) / len(y)
        idx, value = self._get_split(X, y)
        left_X, left_y, right_X, right_y = self._split(X, y, idx, value)
        left = self._build_tree(left_X, left_y, depth + 1)
        right = self._build_tree(right_X, right_y, depth + 1)
        return {"index": idx, "value": value, "left": left, "right": right}

    def _split(self, X, y, idx, val):
        left_X, left_y, right_X, right_y = [], [], [], []
        for xi, yi in zip(X, y):
            if xi[idx] < val:
                left_X.append(xi)
                left_y.append(yi)
            else:
                right_X.append(xi)
                right_y.append(yi)
        return left_X, left_y, right_X, right_y

    def _get_split(self, X, y):
        best_idx, best_val, best_score = 0, 0, float("inf")
        for idx in range(len(X[0])):
            for xi in X:
                left, right = self._split(X, y, idx, xi[idx])[:2]
                score = self._gini_impurity(left, right)
                if score < best_score:
                    best_idx, best_val, best_score = idx, xi[idx], score
        return best_idx, best_val

    def _predict_tree(self, tree, x):
        if isinstance(tree, dict):
            if x[tree["index"]] < tree["value"]:
                return self._predict_tree(tree["left"], x)
            else:
                return self._predict_tree(tree["right"], x)
        return tree

X = np.random.rand(100, 3)  # 100 примеров, 3 признака
y = X[:, 0] + X[:, 1] * 2 + X[:, 2] * 3 + np.random.randn(100) * 0.1  # Линейная зависимость с шумом

# Разделение данных на тренировочную и тестовую выборку
train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Пример тестирования для каждой реализации

# 1. Тест для базовой реализации
rf1 = RandomForestRegressor(n_trees=10, max_depth=5, min_size=10)
rf1.fit(X_train, y_train)
predictions1 = rf1.predict(X_test)
print("Test MSE (Base Implementation):", np.mean((predictions1 - y_test) ** 2))