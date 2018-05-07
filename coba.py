import csv


class Object:
    def __init__(self, id, data, arr, end):
        self.id = id
        self.data = data
        self.score = 0
        self.arr = arr
        self.end = end

data1 = Object("ovan","24", 100, 30)
#print(data1.id)


if __name__ == "__main__":

    # deklarasi variabel parameter
    window_size = 5
    file_path = "dataset/data-mini.csv"
    
    # membuka dataset
    with open(file_path) as input:
        reader = csv.reader(input)
        next(reader)

        # cek data sudah terbaca
        # for row in reader:
        #     print(row)
        
        object_list = list()

        # memasukkan data pada object_list, object_list ---> list()
        for row in reader:
            object_data = Object(row[0], row[1:], int(row[0]), int(row[0]) + window_size + 1)
            #print(object_data.id)
            object_list.append(object_data)

        # cek data pada object_list sudah sesuai
        for x in range(len(object_list)):
            print (object_list[x].data)
    



