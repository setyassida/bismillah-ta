
x = 4

arr = list()

for i in range(x):
    for j in range(x):
        for k in range(x):
            a = [i+1, j+1, k+1]
            arr.append(a)


for i in range(len(arr)):
    print(arr[i])


brr = list()
for i in range(x):
    for j in range(x):
        a = [i+1, j+1]
        brr.append(a)

for i in range(len(brr)):
    print(brr[i])
