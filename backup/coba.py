import csv
import time

from collections import deque
from algorithm.event_based import EventBased

class Object:
    def __init__(self, id, data, arr, end, idsite):
        self.id = id
        self.data = data
        self.score = 0
        self.arr = arr
        self.end = end
        self.idsite = idsite

if __name__ == '__main__':

    # deklarasi variabel-variabel
    k = 20
    window_size = 100
    dimensi = 7
    file_path_site1 = 'dataset/datatesting.csv'
    file_path_site2 = 'dataset/site2.csv'

    site1 = list()
    site2 = list()
    
    # membuka dataset site1
    with open(file_path_site1) as input:
        reader = csv.reader(input)
        next(reader)

        '''
        cek data sudah terbaca
        for row in reader:
            print(row)
        '''
        
        # memasukkan data pada object_list, object_list ---> list()
        for row in reader:
            object_data = Object(row[0], row[1:], int(row[0]), int(row[0]) + window_size + 1, 1)
            #print(object_data.id)
            site1.append(object_data)
        
        '''
        cek data pada object_list sudah sesuai
        for x in range(len(object_list)):
            print (object_list[x].data)
        '''
    
    # membuka dataset site2
    with open(file_path_site2) as input:
        reader = csv.reader(input)
        next(reader)
        for row in reader:
            object_data = Object(row[0], row[1:], int(row[0]), int(row[0]) + window_size + 1, 2)
            site2.append(object_data)

    
    # cek isi site1 dan site2
    # for x in range(len(site1)):
    #     print (site1[x].id)
    # for x in range(len(site2)):
    #     print (site2[x].id)

    # monitoring site 1
    window = deque()
    for i in range(window_size):
        window.append(site1[i])

    time_start = time.time()
    eva = EventBased(k, window, dimensi)
    for row in site1[window_size:]:
        eva.insert(row)
    print("--- %s second ---" %(time.time() - time_start))
    for row in eva.getTopK():
        print(row.id, row.score)