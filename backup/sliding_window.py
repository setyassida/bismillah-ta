import csv

from collections import deque
from collections import Counter

from itertools import islice

from tqdm import tqdm




# class Object:a
#     def __init__(self, id, value, arr, exp, site_id):
#         self.id = id
#         self.value = value
#         self.dscore = 0
#         self.score = 0
#         self.arr = arr
#         self.exp = exp
#         self.position = list()
#         self.site_id = site_id

#     def __repr__(self):
#         return repr((self.id, self.value, self.dscore, self.score, self.arr, self.exp, self.position, self.site_id))

# def read_data(file_path, window_size, site_id):
#     site = list()
#     with open(file_path) as input:
#         reader = csv.reader(input)
#         next(reader)

#         for row in reader:
#             object_data = Object(int(row[0]), row[1:], int(row[0]), int(row[0]) + window_size, site_id)
#             object_data.value = list(map(int, object_data.value)) # convert value as int
#             site.append(object_data)

#     return site


# def site_processing()


# file_path = "../dataset/pico15.csv"
# window = 5

# site = list()
# site = read_data(file_path, window, 1)
# site =  sorted(site, key = lambda object:object.id)



