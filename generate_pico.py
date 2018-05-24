import csv
import random as rand

total_data = 15
file_path = "dataset/pico15.csv"

my_file = open(file_path, 'w')
with my_file:
    writer = csv.writer(my_file, lineterminator='\n')
    writer.writerow(["id","value1","value2"])
    for i in range(15):
        writer.writerow([i+1, rand.randint(1, 15), rand.randint(1, 15)])
        # print("%d,%d,%d" % (i+1, rand.randint(1, 15), rand.randint(1, 15)))



