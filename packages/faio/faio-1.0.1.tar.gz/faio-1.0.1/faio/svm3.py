from sklearn.svm import SVC

class SVM:
    def __init__(self, c=1.0, k='linear'):
        self.m = SVC(C=c, kernel=k)

    def fit(self, x, y):
        self.m.fit(x, y)

    def predict(self, x):
        return self.m.predict(x)

x = [[2, 3], [1, 1], [2, 2], [3, 3], [5, 5]]
y = [1, -1, 1, 1, -1]
xt = [[1.5, 2], [4, 4], [5, 6]]

s = SVM()
s.fit(x, y)
print(s.predict(xt))
