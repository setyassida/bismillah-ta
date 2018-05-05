'''
import pandas as pd

f = pd.read_csv('dataset/btc1.csv')
keep_col = ['Open', 'High', 'Low', 'Close', 'Volume_(BTC)','Volume_(Currency)', 'Weighted_Price']

new_f = f[keep_col]
new_f.to_csv('dataset/btc1-fix.csv', index=False)

'''

import csv

with open('dataset/btc1-fix.csv') as inp, open('dataset/datatesting.csv', 'w') as out:
    reader = csv.reader(inp)
    writer = csv.writer(out, delimiter=',', lineterminator='\n')
    #No need to use `insert(), `append()` simply use `+` to concatenate two lists.
    writer.writerow(['Id'] + next(reader))
    #Iterate over enumerate object of reader and pass the starting index as 1.
    writer.writerows([i] + row for i, row in enumerate(reader, 1))