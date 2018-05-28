import numpy as np
# x = 4

# arr = list()

# for i in range(x):
#     for j in range(x):
#         for k in range(x):
#             a = [i+1, j+1, k+1]
#             arr.append(a)


# for i in range(len(arr)):
#     print(arr[i])


# brr = list()
# for i in range(x):
#     for j in range(x):
#         a = [i+1, j+1]
#         brr.append(a)

# for i in range(len(brr)):
#     print(brr[i])


# apa = list()
# apa.append(8)
# apa.append(1)
# apa.append(3)

# a = [[0] * 100 for i in range(100)]
# print(len(a))

# a[2][2][2] = 4
# # print(a)


a = np.zeros((100, 100, 100, 100))
print(len(a))
a[3][4][5][6] = int(5)
print(a[3][4][5][6])
print(type(a[3][4][5][6]))
print(a)

