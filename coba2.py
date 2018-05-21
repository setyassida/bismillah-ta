import csv
import time
import heapq

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

def dominate(obj1, obj2, dimensi):
    dominate_status = 0
    for i in range(0, dimensi):
        if obj1[i] > obj2[i]:
            if dominate_status == -1:
                dominate_status = 0
                break
            dominate_status = 1
        elif obj1[i] < obj2[i]:
            if dominate_status == 1:
                dominate_status = 0
                break
            dominate_status = -1
    return dominate_status

def insert(self, item):
    self.windows.append(item)
    self.windows.popleft()
    self.now += 1

    # UPDATE TOP-K DOMINATING SCORE
    for i,row in enumerate(self.TopK):
        if row.end > self.now:
            '''
            bisa di improve buat apa kita menghitung dari awal kalau kita
            tau siapa yang keluar dan siapa yang masuk
            '''
            self.TopK[i] = self.computeFromScratch(row)
        else:
            self.TopK.pop(i)
    self.TopK = sorted(
        self.TopK, key=lambda object: object.score, reverse=True)
    
    ## COMPUTE FROM SCRATCH
    item = self.computeFromScratch(item)
    ## INSERT TOPK JIKA TIDAK SCHEDULE ULANG
    if not self.InsertTopKD(item):
        self.scheduleEvent(item, self.now)
    
    ## LIHAT SCHEDULE PADA WAKTU SEKARANG
    while self.EventQueue:
        if self.EventQueue[0].ept == self.now:
            event = heapq.heappop(self.EventQueue)
            if event.item.exp > self.now:
                event.item = self.computeFromScratch(event.item)
                if not self.InsertTopKD(event.item):
                    self.scheduleEvent(event.item, self.now)
        else:
            break
    # print(self.now, [(x.id, x.score, x.exp) for x in self.TopK])

if __name__ == '__main__':

    # deklarasi variabel-variabel
    k = 10
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
    window1 = deque()
    for i in range(window_size):
        window1.append(site1[i])

    for i in range(0, len(window1)):
        for j in range(i, len(window1)):
            dominate_status = dominate(window1[i].data, window1[j].data, dimensi)
            if dominate_status == 1:
                window1[i].score += 1
            elif dominate_status == -1:
                window1[j].score += 1
    
    for row in site1[window_size:]:
        insert(row)

    # for x in range(len(site1)):
    #     print (site1[x].id)
            
