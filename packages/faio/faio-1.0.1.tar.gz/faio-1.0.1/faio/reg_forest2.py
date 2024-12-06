import numpy as np

class RandomForestRegressor:
    def __init__(self, n_trees, max_depth, min_size):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_size = min_size
        self.forest = []

    def fit(self, X, y):
        for _ in range(self.n_trees):
            idx = np.random.choice(len(X), len(X), replace=True)
            X_s, y_s = X[idx], y[idx]
            tree = self._build_tree(X_s, y_s)
            self.forest.append(tree)

    def predict(self, X):
        preds = np.array([self._predict_tree(tree, x) for x in X for tree in self.forest]).reshape(self.n_trees, -1)
        return np.mean(preds, axis=0)

    def _build_tree(self, X, y, depth=0):
        if len(np.unique(y)) == 1 or depth >= self.max_depth or len(X) <= self.min_size:
            return np.mean(y)
        idx, val = self._get_split(X, y)
        left_mask = X[:, idx] < val
        left, right = X[left_mask], X[~left_mask]
        left_y, right_y = y[left_mask], y[~left_mask]
        return {
            "index": idx,
            "value": val,
            "left": self._build_tree(left, left_y, depth + 1),
            "right": self._build_tree(right, right_y, depth + 1),
        }

    def _get_split(self, X, y):
        best_idx, best_val, best_score = 0, 0, float("inf")
        for idx in range(X.shape[1]):
            for val in np.unique(X[:, idx]):
                left = y[X[:, idx] < val]
                right = y[X[:, idx] >= val]
                score = len(left) * np.var(left) + len(right) * np.var(right)
                if score < best_score:
                    best_idx, best_val, best_score = idx, val, score
        return best_idx, best_val

    def _predict_tree(self, tree, x):
        if isinstance(tree, dict):
            if x[tree["index"]] < tree["value"]:
                return self._predict_tree(tree["left"], x)
            else:
                return self._predict_tree(tree["right"], x)
        return tree
