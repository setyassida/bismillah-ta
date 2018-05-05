import csv
import time
import sys


class Data:
    def __init__(self, id, value, epr):
        self.id = id
        self.value = value
        self.score = 0
        self.epr = epr
        self.dominateObj = dict()


if __name__ = "__main__":
    k = 5
    dimen = 7
    windows_size = 100
    file_path = "datatesting.csv"

    with open(file_path) as inp:
        
