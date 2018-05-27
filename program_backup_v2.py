import csv
import time
import sys
import code
import math
import operator as op
import numpy as np

from collections import deque
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

class Grid:
    def __init__(self, pos, total):
        self.pos = pos
        self.total = total
        self.list_id_object = list()
    
    def __repr__(self):
        return repr((self.pos, self.total, self.list_id_object))

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


def dominate(obj1, obj2, dimension):
    dominate_status = 0
    for i in range(0, dimension):
        if obj1[i] < obj2[i]:
            if dominate_status == -1:
                dominate_status = 0
                break
            dominate_status = 1
        elif obj1[i] > obj2[i]:
            if dominate_status == 1:
                dominate_status = 0
                break
            dominate_status = -1
    return dominate_status


def calculate_dscore(window_site, dimension, grid_range):
    sorted_window_site = sorted(window_site, key = lambda object:object.value)
    sorted_window_site_by_id = sorted(window_site, key = lambda object:object.id)    
    list_grid_position = list()
    grid_site = list()

    for i in range(len(sorted_window_site)):
        temp_pos = list()

        # mencari posisi grid tiap object data, --> dimasukkan ke Object.pos
        for j in range(dimension):
            x = int(sorted_window_site[i].value[j]) / grid_range[j]
            x = math.ceil(x)
            if x == 0:
                x = 1
            temp_pos.append(x)

        # print("tempos", temp_pos)
        for k in range(len(temp_pos)):
            sorted_window_site[i].position.append(temp_pos[k])  
        
        # print("list grid pos ", list_grid_position)
        if(temp_pos in list_grid_position):
            # print("tempos juga")
            # menghitung jumlah object yang ada di dalam grid tersebut            
            for x in range(len(grid_site)):
                if(grid_site[x].pos) == temp_pos:
                    grid_site[x].total += 1
                    grid_site[x].list_id_object.append(sorted_window_site[i].id) # menambahkah id object ke dalam grid
            continue

        temp_grid_site = Grid(temp_pos, 1)
        temp_grid_site.list_id_object.append(sorted_window_site[i].id) # menambahkah id object ke dalam grid
        # print("temp_grid_site", temp_grid_site)
        grid_site.append(temp_grid_site)
        # print("grid_site", grid_site)
                  
        list_grid_position.append(temp_pos)

    print("\n--- list seluruh object yang ada pada site tersebut ---")
    for elem in sorted_window_site:
        print(elem)
    
    list_grid_position = sorted(list_grid_position)

    print("\n--- list posisi grid-grid yang ada ---")
    print(list_grid_position)

    print("\n--- list seluruh object grid (posisi, total oject pada grid tersebut) ---")
    for elem in grid_site:
        print(elem)

    # HITUNG DOMINATED SCORE
    for i in range(len(sorted_window_site)):
        for j in range(len(grid_site)):
            if(sorted_window_site[i].position > grid_site[j].pos):
                flag = 0
                for elem in sorted_window_site[i].position:
                    if(elem in grid_site[j].pos):
                        flag = 1
                        break
                    else:
                        continue
                if(flag == 1):
                    # cek satu2 dengan object yang ada di grid tersebut
                    for row in grid_site[j].list_id_object:
                        if(sorted_window_site[i].id == row):
                            continue
                        else:
                            dominated_status = dominate(sorted_window_site[i].value, sorted_window_site_by_id[row-1].value, dimension)
                            if (dominated_status == -1):
                                sorted_window_site[i].dscore += 1
                else:
                    sorted_window_site[i].dscore += grid_site[j].total
            elif(sorted_window_site[i].position == grid_site[j].pos):
                # cek satu2 dengan object yang ada di grid tersebut
                for row in grid_site[j].list_id_object:
                    if(sorted_window_site[i].id == row):
                        continue
                    else:
                        dominated_status = dominate(sorted_window_site[i].value, sorted_window_site_by_id[row-1].value, dimension)
                        if (dominated_status == -1):
                            sorted_window_site[i].dscore += 1
            elif(sorted_window_site[i].position > grid_site[j].pos):
                continue

    return sorted_window_site

def calculate_score(window_site, dimension, grid_range):
    sorted_window_site = sorted(window_site, key = lambda object:object.value)
    sorted_window_site_by_id = sorted(window_site, key = lambda object:object.id)    
    list_grid_position = list()
    grid_site = list()

    for i in range(len(sorted_window_site)):
        temp_pos = list()

        # mencari posisi grid tiap object data, --> dimasukkan ke Object.pos
        for j in range(dimension):
            x = int(sorted_window_site[i].value[j]) / grid_range[j]
            x = math.ceil(x)
            if x == 0:
                x = 1
            temp_pos.append(x)

        # print("tempos", temp_pos)
        for k in range(len(temp_pos)):
            sorted_window_site[i].position.append(temp_pos[k])  
        
        # print("list grid pos ", list_grid_position)
        if(temp_pos in list_grid_position):
            # print("tempos juga")
            # menghitung jumlah object yang ada di dalam grid tersebut            
            for x in range(len(grid_site)):
                if(grid_site[x].pos) == temp_pos:
                    grid_site[x].total += 1
                    grid_site[x].list_id_object.append(sorted_window_site[i].id) # menambahkah id object ke dalam grid
            continue

        temp_grid_site = Grid(temp_pos, 1)
        temp_grid_site.list_id_object.append(sorted_window_site[i].id) # menambahkah id object ke dalam grid
        # print("temp_grid_site", temp_grid_site)
        grid_site.append(temp_grid_site)
        # print("grid_site", grid_site)
                  
        list_grid_position.append(temp_pos)

    print("\n--- list seluruh object yang ada pada site tersebut ---")
    for elem in sorted_window_site:
        print(elem)
    
    list_grid_position = sorted(list_grid_position)

    print("\n--- list posisi grid-grid yang ada ---")
    print(list_grid_position)

    print("\n--- list seluruh object grid (posisi, total oject pada grid tersebut) ---")
    for elem in grid_site:
        print(elem)

    # HITUNG SCORE
    for i in range(len(sorted_window_site)):
        for j in range(len(grid_site)):
            if(sorted_window_site[i].position < grid_site[j].pos):
                flag = 0
                for elem in sorted_window_site[i].position:
                    if(elem in grid_site[j].pos):
                        flag = 1
                        break
                    else:
                        continue
                if(flag == 1):
                    # cek satu2 dengan object yang ada di point tersebut
                    for row in grid_site[j].list_id_object:
                        if(sorted_window_site[i].id == row):
                            continue
                        else:
                            dominate_status = dominate(sorted_window_site[i].value, sorted_window_site_by_id[row-1].value, dimension)
                            if (dominate_status == 1):
                                sorted_window_site[i].score += 1
                else:
                    sorted_window_site[i].score += grid_site[j].total
            elif(sorted_window_site[i].position == grid_site[j].pos):
                # cek satu2 dengan object yang ada di point tersebut
                for row in grid_site[j].list_id_object:
                    if(sorted_window_site[i].id == row):
                        continue
                    else:
                        dominate_status = dominate(sorted_window_site[i].value, sorted_window_site_by_id[row-1].value, dimension)
                        if (dominate_status == 1):
                            sorted_window_site[i].score += 1
            elif(sorted_window_site[i].position < grid_site[j].pos):
                continue

    return sorted_window_site

if __name__ == "__main__":
    # deklarasi variabel
    k = 3
    dimension = 2
    window_size = 15
    grid_range = [5, 5] # [] for dimension a, b, c, ....
    time_interval = 5
    t_current = 0
    lower_bound = 0

    file_path1 = "dataset/pico15.csv"
    file_path2 = "dataset/pico15.csv"

    central_site = list()
    topk_central_site = list()

    site1 = list()
    site1 = read_data(file_path1, window_size, 1)
    site1_by_id =  sorted(site1, key = lambda object:object.id)
    
    site2 = list()
    site2 = read_data(file_path2, window_size, 2)
    site2_by_id = sorted(site2, key = lambda object:object.id)

    window_site1 = deque()
    window_site2 = deque()

    for i in range(window_size):
        window_site1.append(site1[i])
        window_site2.append(site2[i])

    window_site1 = calculate_dscore(window_site1, dimension, grid_range)
    window_site1 = calculate_score(window_site1, dimension, grid_range)
    

    print("BISMILLAH")
    for i in range(len(window_site1)):
        print(window_site1[i])

