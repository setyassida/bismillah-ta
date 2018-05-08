import math
import heapq
import sys
from .helper import dominate

class Event:
    def __init__(self, item, ept, egt):
        self.item = item
        self.ept = ept
        self.egt = egt

    def __lt__(self, other):
        return self.ept < other.ept

class EventBased:
    def __init__(self, K, windows, dimension):
        self.K = K
        self.TopK = []
        self.windows = windows
        self.dimension = dimension
        self.data_lenght = len(windows)
        self.now = len(windows)
        self.EventQueue = []
        
        ## COMPUTE ALL FROM SCRATCH
        for i in range(0, self.data_lenght):
            for j in range(i, self.data_lenght):
                dominate_status = dominate(
                    self.windows[i].data, self.windows[j].data, self.dimension)
                if dominate_status == 1:
                    self.windows[i].score += 1
                elif dominate_status == -1:
                    self.windows[j].score += 1
        
        ## SORT ALL AND TAKE TOP-K
        sorted_window = sorted(
            self.windows, key = lambda object: object.score, reverse=True)
        localK = 0
        tao = self.data_lenght
        for row in sorted_window:
            if localK <= self.K:
                self.TopK.append(row)
                localK += 1
                if tao > row.score:
                    tao = row.score
            elif tao == row.score and localK == self.K:
                self.TopK.append(row)
            else:
                ## JIKA TIDAK MASUK TOP-K CREATE SCHEDULE
                self.scheduleEvent(row, self.now) 

    def getTopK(self):
        return self.TopK

    def insert(self, item):
        self.windows.append(item)
        self.windows.popleft()
        self.now += 1

        # UPDATE TOP-K DOMINATING SCORE
        for i,row in enumerate(self.TopK):
            if row.end > self.now:
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
                if event.item.end > self.now:
                    event.item = self.computeFromScratch(event.item)
                    if not self.InsertTopKD(event.item):
                        self.scheduleEvent(event.item, self.now)
            else:
                break
        # print(self.now, [(x.id, x.score, x.exp) for x in self.TopK])

    def scheduleEvent(self, item, now):
        Exp1 = None
        for row in self.TopK:
            if Exp1 == None or Exp1 > row.end:
                Exp1 = row.end
        ept = min((math.ceil((self.TopK[-1].score - item.score)/2)+now),Exp1)
        if ept >= now:
            e = Event(item, ept, now)
            heapq.heappush(self.EventQueue,e)

    def InsertTopKD(self, item):
        ## JIKA LEBIH BESAR DARI PADA TOP-K YANG TERKECIL MAKA MASUK TOP-K
        if item.score == self.TopK[-1].score or len(self.TopK) < self.K:
            self.TopK.append(item)
            return True
        elif item.score > self.TopK[-1].score:
            ''' 
            insert bisa dimasimalkan lagi
            dengan melakukan reschedule yang diperlukan sajas
            '''
            while item.score > self.TopK[-1].score and len(self.TopK) >= self.K:
                self.scheduleEvent(self.TopK[-1], self.now)
                self.TopK.pop()
            self.TopK.append(item)
            i = len(self.TopK)-2
            while i >= 0 and item.score > self.TopK[i].score:
                self.TopK[i+1] = self.TopK[i]
                i -= 1
            self.TopK[i+1] = item
            return True
        else:
            return False

    def computeFromScratch(self, item):
        item.score = 0
        for j in range(self.data_lenght):
            dominate_status = dominate(
                item.data, self.windows[j].data, self.dimension)
            if dominate_status == 1:
                item.score += 1
        return item
