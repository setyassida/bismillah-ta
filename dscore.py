import csv
import math
import pprint

class Object:
    def __init__(self, id, value, end):
        self.id = id
        self.value = value
        self.score = 0
        self.end = end
        self.position = list()
    
    def __repr__(self):
        return repr((self.id, self.value, self.score, self.end, self.position))

class Grid:
    def __init__(self, pos, total):
        self.pos = pos
        self.total = total
        self.list_id_object = list()
    
    def __repr__(self):
        return repr((self.pos, self.total, self.list_id_object))

def dominate(obj1, obj2, dimensi):
    dominate_status = 0
    for i in range(0, dimensi):
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

if __name__ == '__main__':

    #deklarasi variable
    window_size = 3
    dimensi = 2
    grid_range = 5

    file_path = 'dataset/pico.csv'

    site = list()

    with open(file_path) as input:
        reader = csv.reader(input)
        next(reader)

        for row in reader:
            object_data = Object(int(row[0]), row[1:], int(row[0]) + window_size + 1)
            site.append(object_data)

    # for i in range(len(site)):
    #     print(site[i])
    
    # print("sorted")

    # sort site by value
    sorted_site = sorted(site, key = lambda object:object.value)

    # sort site by id
    sorted_site_by_id = sorted(site, key = lambda object:object.id)
    
    # for i in range(len(sorted_site)):
    #     print(sorted_site[i])

    list_grid_position = list()
    grid_site = list()
    temp_val = 1

    for i in range(len(sorted_site)):
        temp_pos = list()
        
        # mencari posisi grid tiap object data, --> dimasukkan ke Object.pos
        for j in range(dimensi):
            x = int(sorted_site[i].value[j]) / grid_range
            x = math.ceil(x)
            if x == 0:
                x = 1
            temp_pos.append(x)

        # print(temp_pos)
        for k in range(len(temp_pos)):
            sorted_site[i].position.append(temp_pos[k])  
        
        if(temp_pos in list_grid_position):
            # menghitung jumlah object yang ada di dalam grid tersebut            
            for x in range(len(grid_site)):
                if(grid_site[x].pos) == temp_pos:
                    grid_site[x].total += 1
                    grid_site[x].list_id_object.append(sorted_site[i].id) # menambahkah id object ke dalam grid
            continue

        temp_grid_site = Grid(temp_pos, 1)
        temp_grid_site.list_id_object.append(sorted_site[i].id) # menambahkah id object ke dalam grid
        # print(temp_grid_site)
        grid_site.append(temp_grid_site)
                  
        list_grid_position.append(temp_pos)
        
    print("\n--- list seluruh object yang ada pada site tersebut ---")
    for elem in sorted_site:
        print(elem)
    
    list_grid_position = sorted(list_grid_position)

    print("\n--- list posisi grid-grid yang ada ---")
    print(list_grid_position)

    print("\n--- list seluruh object grid (posisi, total oject pada grid tersebut) ---")
    for elem in grid_site:
        print(elem)
        
    # HITUNG DOMINASI SCORE
    for i in range(len(sorted_site)):
        for j in range(len(grid_site)):
            if(sorted_site[i].position > grid_site[j].pos):
                flag = 0
                for elem in sorted_site[i].position:
                    if(elem in grid_site[j].pos):
                        flag = 1
                        break
                    else:
                        continue
                if(flag == 1):
                    # cek satu2 dengan object yang ada di point tersebut
                    for row in grid_site[j].list_id_object:
                        if(sorted_site[i].id == row):
                            continue
                        else:
                            dominate_status = dominate(sorted_site[i].value, sorted_site_by_id[row-1].value, dimensi)
                            if (dominate_status == 1):
                                sorted_site[i].score += 1
                else:
                    sorted_site[i].score  = grid_site[j].total
            elif(sorted_site[i].position == grid_site[j].pos):
                # cek satu2 dengan object yang ada di point tersebut
                for row in grid_site[j].list_id_object:
                    if(sorted_site[i].id == row):
                        continue
                    else:
                        dominate_status = dominate(sorted_site[i].value, sorted_site_by_id[row-1].value, dimensi)
                        if (dominate_status == 1):
                            sorted_site[i].score += 1
            elif(sorted_site[i].position < grid_site[j].pos):
                continue

    print("\n-BISMILLAH-")
    for elem in sorted_site:
        print(elem)