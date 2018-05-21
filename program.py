import csv
import time
import sys

from collections import deque

class Object:
    def __init__(self, id, value, arr, exp):
        self.id = id
        self.value = value
        self.score = 0
        self.arr = arr
        self.exp = exp
        self.position = list()

    def __repr__(self):
        return repr((self.id, self.value, self.score, self.arr, self.exp, self.position))

class Grid:
    def __init__(self, pos, total):
        self.pos = pos
        self.total = total
        self.list_id_object = list()
    
    def __repr__(self):
        return repr((self.pos, self.total, self.list_id_object))

def read_data(file_path, window_size):
    site = list()
    with open(file_path) as input:
        reader = csv.reader(input)
        next(reader)

        for row in reader:
            object_data = Object(int(row[0]), row[1:], int(row[0]), int(row[0]) + window_size)
            site.append(object_data)
    return site

if __name__ == "__main__":
    # deklarasi variabel
    k = 3
    dimension = 2
    window_size = 3
    grid_range = 5
    file_path1 = "dataset/pico1.csv"
    file_path2 = "dataset/pico2.csv"

    site1 = list()
    site2 = list()

    site1 = read_data(file_path1, window_size)
    site2 = read_data(file_path2, window_size)
