import pandas as pd 
data = {"id":[0,1,2],
        "name":['john', 'randall', 'baker'],
        "dg_leader":[0,0,0],
        "maturity":[5,6,10],
        "fg_num":[0,0,0],
        "female":[0,0,0]
       }

df = pd.DataFrame(data)
conn_data = [[0,0,1],
[0,0,1],
[1,1,0]]
conns_df = pd.DataFrame(conn_data, index= [0,1,2], columns=['ho','hey','so'])
for idx, row in conns_df.iterrows():
    things_to_add = []
    for idx, value in row.iteritems():
        if value == 1:
            print(idx)
        