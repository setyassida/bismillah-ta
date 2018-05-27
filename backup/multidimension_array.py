import numpy as np

class Object:
    def __init__(self, id, value, arr, exp, site_id):
        self.id = id
        self.value = value
        self.score = 0
        self.arr = arr
        self.exp = exp
        self.position = list()
        self.site_id = site_id

    def __repr__(self):
        return repr((self.id, self.value, self.score, self.arr, self.exp, self.position, self.site_id))


obj = Object(1, [1, 2, 3], 5, 10, 1)
arr = np.zeros(90)
arr = arr.reshape(9, 2, 5)

print(arr[1][1][1])
arr[1][1][1] = obj
print(arr[1][1][1])


print(arr)