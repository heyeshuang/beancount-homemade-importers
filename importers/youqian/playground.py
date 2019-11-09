#%%
import csv
from collections import defaultdict
# from beancount.ingest.importers.csv import Importer, Col
# csv.Importer
columns=defaultdict(list)
with open("./documents.tmp/网易有钱记账数据-trans.csv",newline='') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v)

# %%
set(columns["小类"])

# %%
set(columns["大类"])

# %%
set(map(lambda x :x[0]+","+x[1] ,zip(columns["大类"],columns["小类"])))

# %%
set(map(lambda x :x[0]+","+x[1] ,zip(columns["转出账户"],columns["转入账户"])))


# %%
