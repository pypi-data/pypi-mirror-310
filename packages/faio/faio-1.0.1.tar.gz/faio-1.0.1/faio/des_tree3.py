from sklearn.tree import DecisionTreeRegressor

m = DecisionTreeRegressor(random_state=1)

x = [[1], [2], [3], [4], [5], [100], [200], [300], [400]]
y = [1, 2, 3, 4, 5, 100, 200, 300, 400]

x1 = [[100], [200], [300], [500], [600]]

m.fit(x, y)
print(m.predict(x1))
