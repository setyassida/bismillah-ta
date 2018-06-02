import code
import csv
import math
import sys
import time
import pickle
import multiprocessing
import operator as op

import numpy as np

from sets import Set
from collections import deque
from itertools import islice
from tqdm import tqdm


# deklarasi variabel
k = 3
dimension = 2
window_size = 15
grid_range = [5, 5] # [] for dimension a, b, c, ....

file_path1 = "dataset/pico15.csv"
file_path2 = "dataset/pico15_2.csv"
file_path3 = "dataset/pico15.csv"  

pkl_site_1 = "pkl_data/data_site_1.pkl"  
pkl_site_2 = "pkl_data/data_site_2.pkl"  
pkl_site_3 = "pkl_data/data_site_3.pkl"  


class Object:
    def __init__(self, id, value, arr, exp, site_id):
        self.id = id
        self.value = value
        self.dscore = 0
        self.score = 0
        self.arr = arr
        self.exp = exp
        self.position = list()
        self.dominate_object = list()
        self.site_id = site_id
        self.cand_flag = 0

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return repr((self.id, self.value, self.dscore, self.score, self.arr, self.exp, self.position, self.dominate_object, self.site_id))

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

def calculate_score(window_site):
    sorted_window_site = sorted(window_site, key = lambda object:object.value)
    sorted_window_site_by_id = {}
    for site_data in sorted_window_site:
        sorted_window_site_by_id[site_data.id] = site_data
    list_grid_position = list()
    grid_site = list()

    max_grid_loc_site  = list()

    for i in tqdm(range(len(sorted_window_site))):
        temp_pos = list()

        # mencari posisi grid tiap object data, --> dimasukkan ke Object.pos
        for j in range(dimension):
            x = int(sorted_window_site[i].value[j]) / grid_range[j]
            x = math.ceil(x)
            if x == 0:
                x = 1
            temp_pos.append(x)

            # mencari max value grid
            if(len(max_grid_loc_site) != 0):
                if(max_grid_loc_site[j] < x):
                    max_grid_loc_site[j] = x

        if(len(max_grid_loc_site) == 0):
            max_grid_loc_site.extend(temp_pos)

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

    # print("\n--- list seluruh object yang ada pada site tersebut ---")
    # for elem in sorted_window_site:
    #     print(elem)
    
    list_grid_position = sorted(list_grid_position)

    # print("\n--- list posisi grid-grid yang ada ---")
    # print(list_grid_position)

    # print("\n--- list seluruh object grid (posisi, total oject pada grid tersebut) ---")
    # for elem in grid_site:
    #     print(elem)

    for x in tqdm(range(len(sorted_window_site))):
        get_pos = sorted_window_site[x].position
        temp = list()
        # print(get_pos)
        # print(max_grid_loc_site)

        if(dimension == 2):
            # cek fully dominated
            for i in range(get_pos[0], max_grid_loc_site[0]):
                for j in range(get_pos[1], max_grid_loc_site[1]):
                    temp = [i+1, j+1]
                    # print("iki pos e", temp)
                    for elem in grid_site:
                        if (elem.pos == temp):
                            sorted_window_site[x].score += elem.total
            
            # cek satu2
            cheking_list = list()
            
            # dimensi x
            for i in range(max_grid_loc_site[0]):
                temp = [i+1, get_pos[1]]
                if(temp in cheking_list):
                    continue
                else:
                    cheking_list.append(temp)
            
            #dimensi y
            for i in range(max_grid_loc_site[1]):
                temp = [get_pos[0], i+1]
                if(temp in cheking_list):
                    continue
                else:
                    cheking_list.append(temp)
            
            for temp in cheking_list:
                for elem in grid_site:
                    if(elem.pos == temp):
                        for row in elem.list_id_object:
                            if(sorted_window_site[x].id == row):
                                continue
                            else:
                                dominate_status = dominate(sorted_window_site[x].value, sorted_window_site_by_id[row].value, dimension)
                                if (dominate_status == 1):
                                    sorted_window_site[x].score += 1
                                elif (dominate_status == -1):
                                    sorted_window_site[x].dscore += 1
                    
            # yang dihiraukan
            for i in range(0, get_pos[0]-1):
                for j in range(0, get_pos[1]-1):
                    temp = [i+1, j+1]
                    # print("iki pos e", temp)
                    for elem in grid_site:
                        if (elem.pos == temp):
                            sorted_window_site[x].dscore += elem.total
    
    deque_sorted_window_site = deque()
    sorted_window_site = sorted(sorted_window_site, key = lambda object:object.id)
    for elem in sorted_window_site:
        deque_sorted_window_site.append(elem)

    return deque_sorted_window_site

def calculate_real_score(window_site):
    # sorted_window_site = sorted(window_site, key = lambda object:object.value)
    sorted_window_site = window_site
    sorted_window_site_by_id = {}
    for site_data in sorted_window_site:
        sorted_window_site_by_id[site_data.id] = site_data
    list_grid_position = list()
    grid_site = list()

    max_grid_loc_site  = list()

    for i in tqdm(range(len(sorted_window_site))):
        temp_pos = list()

        del sorted_window_site[i].position[:]
        sorted_window_site[i].score = 0

        # mencari posisi grid tiap object data, --> dimasukkan ke Object.pos
        for j in range(dimension):
            x = int(sorted_window_site[i].value[j]) / grid_range[j]
            x = math.ceil(x)
            if x == 0:
                x = 1
            temp_pos.append(x)

            # mencari max value grid
            if(len(max_grid_loc_site) != 0):
                if(max_grid_loc_site[j] < x):
                    max_grid_loc_site[j] = x

        if(len(max_grid_loc_site) == 0):
            max_grid_loc_site.extend(temp_pos)

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

    # print("\n--- list seluruh object yang ada pada site tersebut ---")
    # for elem in sorted_window_site:
    #     print(elem)
    
    list_grid_position = sorted(list_grid_position)

    # print("\n--- list posisi grid-grid yang ada ---")
    # print(list_grid_position)

    # print("\n--- list seluruh object grid (posisi, total oject pada grid tersebut) ---")
    # for elem in grid_site:
    #     print(elem)

    for x in tqdm(range(len(sorted_window_site))):
        get_pos = sorted_window_site[x].position
        temp = list()
        # print(get_pos)
        # print(max_grid_loc_site)

        if(dimension == 2):
            # cek fully dominated
            for i in range(get_pos[0], max_grid_loc_site[0]):
                for j in range(get_pos[1], max_grid_loc_site[1]):
                    temp = [i+1, j+1]
                    # print("iki pos e", temp)
                    for elem in grid_site:
                        if (elem.pos == temp):
                            sorted_window_site[x].score += elem.total
            
            # cek satu2
            cheking_list = list()
            
            # dimensi x
            for i in range(max_grid_loc_site[0]):
                temp = [i+1, get_pos[1]]
                if(temp in cheking_list):
                    continue
                else:
                    cheking_list.append(temp)
            
            #dimensi y
            for i in range(max_grid_loc_site[1]):
                temp = [get_pos[0], i+1]
                if(temp in cheking_list):
                    continue
                else:
                    cheking_list.append(temp)
            
            for temp in cheking_list:
                for elem in grid_site:
                    if(elem.pos == temp):
                        for row in elem.list_id_object:
                            if(sorted_window_site[x].id == row):
                                continue
                            else:
                                dominate_status = dominate(sorted_window_site[x].value, sorted_window_site_by_id[row].value, dimension)
                                if (dominate_status == 1):
                                    sorted_window_site[x].score += 1
                                elif (dominate_status == -1):
                                    sorted_window_site[x].dscore += 1
                    
            # yang dihiraukan
            for i in range(0, get_pos[0]-1):
                for j in range(0, get_pos[1]-1):
                    temp = [i+1, j+1]
                    # print("iki pos e", temp)
                    for elem in grid_site:
                        if (elem.pos == temp):
                            sorted_window_site[x].dscore += elem.total
    
    deque_sorted_window_site = deque()
    # sorted_window_site = sorted(sorted_window_site, key = lambda object:object.id)
    for elem in sorted_window_site:
        deque_sorted_window_site.append(elem)

    return deque_sorted_window_site

def calculate_sentral_dscore(sentral_site):
    sorted_sentral_site = sorted(sentral_site, key = lambda object:object.value)
    sorted_sentral_site_by_id = {}
    for site_data in sorted_sentral_site:
        sorted_sentral_site_by_id[site_data.id] = site_data

    list_grid_position = list()
    grid_site = list()

    max_grid_loc_site  = list()

    for i in tqdm(range(len(sorted_sentral_site))):
        temp_pos = list()

        del sorted_sentral_site[i].position[:]
        sorted_sentral_site[i].score = 0

        # mencari posisi grid tiap object data, --> dimasukkan ke Object.pos
        for j in range(dimension):
            x = int(sorted_sentral_site[i].value[j]) / grid_range[j]
            x = math.ceil(x)
            if x == 0:
                x = 1
            temp_pos.append(x)

            # mencari max value grid
            if(len(max_grid_loc_site) != 0):
                if(max_grid_loc_site[j] < x):
                    max_grid_loc_site[j] = x

        if(len(max_grid_loc_site) == 0):
            max_grid_loc_site.extend(temp_pos)

        # print("tempos", temp_pos)
        for k in range(len(temp_pos)):
            sorted_sentral_site[i].position.append(temp_pos[k])  
        
        # print("list grid pos ", list_grid_position)
        if(temp_pos in list_grid_position):
            # print("tempos juga")
            # menghitung jumlah object yang ada di dalam grid tersebut            
            for x in range(len(grid_site)):
                if(grid_site[x].pos) == temp_pos:
                    grid_site[x].total += 1
                    grid_site[x].list_id_object.append(sorted_sentral_site[i].id) # menambahkah id object ke dalam grid
            continue

        temp_grid_site = Grid(temp_pos, 1)
        temp_grid_site.list_id_object.append(sorted_sentral_site[i].id) # menambahkah id object ke dalam grid
        # print("temp_grid_site", temp_grid_site)
        grid_site.append(temp_grid_site)
        # print("grid_site", grid_site)
                  
        list_grid_position.append(temp_pos)

    # print("\n--- list seluruh object yang ada pada site tersebut ---")
    # for elem in sorted_window_site:
    #     print(elem)
    
    list_grid_position = sorted(list_grid_position)

    # print("\n--- list posisi grid-grid yang ada ---")
    # print(list_grid_position)

    # print("\n--- list seluruh object grid (posisi, total oject pada grid tersebut) ---")
    # for elem in grid_site:
    #     print(elem)

    for x in tqdm(range(len(sorted_sentral_site))):
        get_pos = sorted_sentral_site[x].position
        temp = list()
        # print(get_pos)
        # print(max_grid_loc_site)

        if(dimension == 2):
            # cek fully dominated
            for i in range(get_pos[0], max_grid_loc_site[0]):
                for j in range(get_pos[1], max_grid_loc_site[1]):
                    temp = [i+1, j+1]
                    # print("iki pos e", temp)
                    # for elem in grid_site:
                    #     if (elem.pos == temp):
                    #         sorted_window_site[x].score += elem.total
            
            # cek satu2
            cheking_list = list()
            
            # dimensi x
            for i in range(max_grid_loc_site[0]):
                temp = [i+1, get_pos[1]]
                if(temp in cheking_list):
                    continue
                else:
                    cheking_list.append(temp)
            
            #dimensi y
            for i in range(max_grid_loc_site[1]):
                temp = [get_pos[0], i+1]
                if(temp in cheking_list):
                    continue
                else:
                    cheking_list.append(temp)
            
            for temp in cheking_list:
                for elem in grid_site:
                    if(elem.pos == temp):
                        for row in elem.list_id_object:
                            if(sorted_sentral_site[x].id == row):
                                continue
                            else:
                                dominate_status = dominate(sorted_sentral_site[x].value, sorted_sentral_site_by_id[row].value, dimension)
                                # if (dominate_status == 1):
                                #     sorted_window_site[x].score += 1
                                if (dominate_status == -1):
                                    sorted_sentral_site[x].dscore += 1
                    
            # yang dihiraukan
            for i in range(0, get_pos[0]-1):
                for j in range(0, get_pos[1]-1):
                    temp = [i+1, j+1]
                    # print("iki pos e", temp)
                    for elem in grid_site:
                        if (elem.pos == temp):
                            sorted_sentral_site[x].dscore += elem.total
    deque_sorted_sentral = deque()
    sorted_sentral_site = sorted(sorted_sentral_site, key = lambda object:object.id)
    for elem in sorted_sentral_site:
        deque_sorted_sentral.append(elem)

    return deque_sorted_sentral

def dist_score_comp_processing(cand, site, id_site, pkl_name):
    
    for i in range(len(cand)):
        site.append(cand[i])

    for i in range(len(site)):
        print("iki loh", site[i])


    site_calculated = calculate_real_score(site)
    for i in range(len(site_calculated)):
        print(site_calculated[i])
    
    with open(pkl_name, "wb") as f:
        pickle.dump(len(site_calculated), f)
        for row in site_calculated:
            pickle.dump(row, f)

def dist_score_comp(cand, site1, site2, site3):
    
    # print("INI UDAH DI FUNGSI DIST_SCORE_COMP")
    # print("CAND")
    # for i in range(len(cand)):
    #     print(cand[i])

    # print("SITE 1")    
    # for i in range(len(site1)):
    #     print(site1[i])

    # print("SITE 2")        
    # for i in range(len(site2)):
    #     print(site2[i])

    # print("SITE 3")        
    # for i in range(len(site3)):
    #     print(site3[i])

    p1 = multiprocessing.Process(target = dist_score_comp_processing, args = (cand, site1, 1, pkl_site_1))
    p2 = multiprocessing.Process(target = dist_score_comp_processing, args = (cand, site2, 2, pkl_site_2))
    p3 = multiprocessing.Process(target = dist_score_comp_processing, args = (cand, site3, 3, pkl_site_3))

    p1.start()
    p1.join()

    p2.start()
    p2.join()
    
    p3.start()
    p3.join()

    dist_site1 = list()
    dist_site2 = list()
    dist_site3 = list()

    final_cand = cand
    for i in range(len(final_cand)):
        final_cand[i].score = 0
    
    with open(pkl_site_1, "rb") as f:
        for _ in range(pickle.load(f)):
            dist_site1.append(pickle.load(f))

    with open(pkl_site_2, "rb") as f:
        for _ in range(pickle.load(f)):
            dist_site2.append(pickle.load(f))

    with open(pkl_site_3, "rb") as f:
        for _ in range(pickle.load(f)):
            dist_site3.append(pickle.load(f))


    # del dist_site1[0:15]
    # del dist_site2[0:15]
    # del dist_site3[0:15]
    
    # print("----JADILAH APA 1----")
    for i in range(len(cand)):
        final_cand[i].score += dist_site1[i+window_size].score

    # print("----JADILAH APA 2----")
    for i in range(len(cand)):
        final_cand[i].score += dist_site2[i+window_size].score
        # print(dist_site2[i])

    # print("----JADILAH APA 3----")
    for i in range(len(cand)):
        final_cand[i].score += dist_site3[i+window_size].score
        # print(dist_site2[i])

    # # print("----FINALL CUYY----")
    # for i in range(len(final_cand)):
    #     print(final_cand[i])

    return final_cand

def site_processing(site, pkl_name):
    window_site = deque()

    for i in range(window_size):
        window_site.append(site[i])
    del site[:window_size]

    # for i in range(len(window_site)):
    #     print(window_site[i])

    window_site = calculate_score(window_site)

    with open(pkl_name, "wb") as f:
        pickle.dump(len(window_site), f)
        for row in window_site:
            pickle.dump(row, f)

    # for i in range(len(window_site)):
    #     pickle.dump(window_site[i], output)
    #     site_calculated[i] = window_site[i].id


    # counter = 0
    # while(counter < len(site)):

    #     window_site = calculate_score(window_site, dimension, grid_range)

    #     # for i in range(window_site):
    #     #     print(window_site[i])

    #     time.sleep(3)

    #     hilang = window_site[0]
    #     # print(hilang)
        
    #     window_site.popleft()
    #     # print(site[counter])
        
    #     window_site.append(site[counter])
    #     # print(window_site)
        
    #     counter = counter + 1

def next_site_processing(site, pkl_name):
    window_site = deque()

    window_site = calculate_score(window_site)

    with open(pkl_name, "wb") as f:
        pickle.dump(len(window_site), f)
        for row in window_site:
            pickle.dump(row, f)

if __name__ == "__main__":
    central_site = list()
    topk_central_site = list()

    site1 = list()
    site1 = read_data(file_path1, window_size, 1)
    site1 = sorted(site1, key = lambda object:object.id)

    site2 = list()
    site2 = read_data(file_path2, window_size, 2)
    site2 = sorted(site2, key = lambda object:object.id)

    site3 = list()
    site3 = read_data(file_path3, window_size, 3)
    site3 = sorted(site3, key = lambda object:object.id)

    p1 = multiprocessing.Process(target = site_processing, args = (site1, pkl_site_1))
    p2 = multiprocessing.Process(target = site_processing, args = (site2, pkl_site_2))
    p3 = multiprocessing.Process(target = site_processing, args = (site3, pkl_site_3))

    p1.start()
    p1.join()

    p2.start()
    p2.join()
    
    p3.start()
    p3.join()

    site1_calculated = deque()
    site2_calculated = deque()
    site3_calculated = deque()

    with open(pkl_site_1, "rb") as f:
        for _ in range(pickle.load(f)):
            site1_calculated.append(pickle.load(f))

    with open(pkl_site_2, "rb") as f:
        for _ in range(pickle.load(f)):
            site2_calculated.append(pickle.load(f))

    with open(pkl_site_3, "rb") as f:
        for _ in range(pickle.load(f)):
            site3_calculated.append(pickle.load(f))

    print("----BISMILLAH 1----")
    for i in range(len(site1_calculated)):
        print(site1_calculated[i])

    print("----BISMILLAH 2----")
    for i in range(len(site2_calculated)):
        print(site2_calculated[i])

    print("----BISMILLAH 3----")
    for i in range(len(site3_calculated)):
        print(site3_calculated[i])

    sent_to_sentral = list()

    for i in range(window_size):
        if(site1_calculated[i].dscore < k):
            sent_to_sentral.append(site1_calculated[i])
        if(site2_calculated[i].dscore < k):
            sent_to_sentral.append(site2_calculated[i])
        if(site3_calculated[i].dscore < k):
            sent_to_sentral.append(site3_calculated[i])

    print("----BISMILLAH !!----")
    for i in range(len(sent_to_sentral)):
        print(sent_to_sentral[i])

    sentral_site = sent_to_sentral
    sentral_site_calculated = calculate_sentral_dscore(sentral_site)
    sent_to_sentral = set(sent_to_sentral)
    
    print("----INIKAH HASILNYA----")
    for i in range(len(sentral_site_calculated)):
        print(sentral_site_calculated[i])

    cand = deque()
    for i in range(len(sentral_site_calculated)):
        if(sentral_site_calculated[i].dscore < k):
            cand.append(sentral_site_calculated[i])

    print("----INI NIH CAND YANG AKAN DI BROADCAST----")
    for i in range(len(cand)):
        print(cand[i])

    if (len(cand) > k):
        cand_calculated = dist_score_comp(cand, site1_calculated, site2_calculated, site3_calculated)
    
    # sorted_window_site = sorted(window_site, key = lambda object:object.value)
    cand_calculated = sorted(cand_calculated, key = lambda object:object.score, reverse=True)

    print("TOP-K FINAL INITIAL STATE")
    for i in range(k):
        print(cand_calculated[i])

    ## initial windows
    current_windows_site1 = deque(site1[0:window_size])
    current_windows_site2 = deque(site2[0:window_size])
    current_windows_site3 = deque(site3[0:window_size])
    counter = window_size
    
    ## begin sliding windows
    while(counter < len(site1)):
        current_windows_site1.popleft()
        current_windows_site1.append(site1[counter])

        current_windows_site2.popleft()
        current_windows_site2.append(site2[counter])

        current_windows_site3.popleft()
        current_windows_site3.append(site3[counter])

        ## calculate each site
        p1 = multiprocessing.Process(target = next_site_processing, args = (current_windows_site1, pkl_site_1))
        p2 = multiprocessing.Process(target = next_site_processing, args = (current_windows_site2, pkl_site_2))
        p3 = multiprocessing.Process(target = next_site_processing, args = (current_windows_site3, pkl_site_3))

        p1.start()
        p1.join()
        p2.start()
        p2.join()
        p3.start()
        p3.join()

        next_site1_calculated = list()
        next_site2_calculated = list()
        next_site3_calculated = list()

        with open(pkl_site_1, "rb") as f:
            for _ in range(pickle.load(f)):
                next_site1_calculated.append(pickle.load(f))

        ## find expired, and new generated data by finding the difference between 2 set
        filtered_site1 = set([datum for datum in next_site1_calculated if datum.dscore < k])
        generated_site1 = filtered_site1.difference(sent_to_sentral)
        expired_site1 = set({x for x in sent_to_sentral.difference(filtered_site1) if x.site_id == 1})

        with open(pkl_site_2, "rb") as f:
            for _ in range(pickle.load(f)):
                next_site2_calculated.append(pickle.load(f))

        filtered_site2 = set([datum for datum in next_site2_calculated if datum.dscore < k])
        generated_site2 = filtered_site2.difference(sent_to_sentral)
        expired_site2 = set({x for x in sent_to_sentral.difference(filtered_site2) if x.site_id == 2})

        with open(pkl_site_3, "rb") as f:
            for _ in range(pickle.load(f)):
                next_site3_calculated.append(pickle.load(f))

        filtered_site3 = set([datum for datum in next_site3_calculated if datum.dscore < k])
        generated_site3 = filtered_site3.difference(sent_to_sentral)
        expired_site3 = set({x for x in sent_to_sentral.difference(filtered_site3) if x.site_id == 3})


        ## update central data
        sent_to_sentral -= expired_site1
        sent_to_sentral -= expired_site2
        sent_to_sentral -= expired_site2
        sent_to_sentral = sent_to_sentral.union(generated_site1)
        sent_to_sentral = sent_to_sentral.union(generated_site2)
        sent_to_sentral = sent_to_sentral.union(generated_site3)

        counter = counter+1

        ## do something with the expire and generated here

        



