import csv

from collections import deque
from collections import Counter

from itertools import islice

class Object:
    def __init__(self, id, value, arr, exp, site_id):
        self.id = id
        self.value = value
        self.dscore = 0
        self.score = 0
        self.arr = arr
        self.exp = exp
        self.position = list()
        self.site_id = site_id

    def __repr__(self):
        return repr((self.id, self.value, self.dscore, self.score, self.arr, self.exp, self.position, self.site_id))

def read_data(file_path, window_size, site_id):
    site = list()
    with open(file_path) as input:
        reader = csv.reader(input)
        next(reader)

        for row in reader:
            object_data = Object(int(row[0]), row[1:], int(row[0]), int(row[0]) + window_size, site_id)
            object_data.value = list(map(int, object_data.value)) # convert value as int
            site.append(object_data)

    return site


file_path = "../dataset/pico15.csv"
window = 5

site = list()
site = read_data(file_path, window, 1)
site =  sorted(site, key = lambda object:object.id)

window_site = deque()

# for i in range(len(site)):
#     print(site[i])

for i in range(window):
    window_site.append(site[i])
del site[:window]

# for i in range(len(site)):
#     print(site[i])

# for i in range(len(window_site)):
#     print(window_site[i])

counter = 0
while(counter < len(site)):
    # window_site = sliding_window(window_site, site)

    hilang = window_site[0]
    # print(hilang)
    
    window_site.popleft()
    # print(site[counter])
    
    window_site.append(site[counter])
    # print(window_site)
    
    counter = counter + 1

