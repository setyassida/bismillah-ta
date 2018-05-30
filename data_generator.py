import csv
import random as rand
from tqdm import tqdm

total_data = 200000
file_path = "dataset/3000.csv"

my_file = open(file_path, 'w')
with my_file:
    writer = csv.writer(my_file, lineterminator='\n')
    writer.writerow(["id","value1","value2"])
    for i in tqdm(range(total_data+50)):
        writer.writerow([i+1, rand.randint(1, 100), rand.randint(1, 100)])
        # print("%d,%d,%d" % (i+1, rand.randint(1, 15), rand.randint(1, 15)))