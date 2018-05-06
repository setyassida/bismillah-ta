import csv
import time
import sys

from collections import deque


class Data:
    def __init__(self, id, value, epr):
        self.id = id
        self.value = value
        self.score = 0
        self.epr = epr
        self.dominateObj = dict()

if __name__ == "__main__":
    k = 5
    dimen = 7
    windows_size = 100
    file_path = "dataset/datatesting.csv"

    # read data testing
    with open(file_path) as input:
        file_data = csv.reader(input)
        next(file_data)
        obj_list = list()
    for i, row, in enumerate(file_data):
        data = Data(row[0], row[1:], i+windows_size + 1)
        obj_list.append(data)
    windows = deque() 
    for i in range(windows_size):
        windows.append(obj_list[i])
    
    # start filter-based algorithm
        


