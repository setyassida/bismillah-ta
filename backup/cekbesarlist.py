import math

def check(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

def cek(a, b):
    status = 0
    if(a == b):
        return status
    else:
        for i in range(len(a)):
            if(a[i] > b[i]):
                
                
    

a = [4, 4]
b = [6, 1]

print("a", a)
print("b", b, "\n")


print("iki loh")
ab = check(a, b)
print(ab)


if (b > a):
    print("masuk")
    flag = 0
    for elem in b:
        print(elem)
        if(elem in a):
            flag = 1
        else:
            continue
    if(flag == 1):
        print("cek satu2")
    else:
        print("ambil dscore")
elif(b<a):
    print("ngga di cek")
elif(b > a):
    print("cek satu2")
elif(b == a):
    print("cek satu2")
