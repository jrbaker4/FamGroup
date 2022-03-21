import networkx as nx
import csv
import numpy as np
import matplotlib.pyplot as plt
connection_matrix = np.genfromtxt('conn_mat.csv', delimiter=',')
G = nx.Graph()

with open("students.csv") as f:
    reader = csv.reader(f, delimiter = ',')
    names_array = []
    for row in reader:
        if(len(row)!=0):
            names_array.append(row[2])
            G.add_node(row[2])
for john_friend in range(len(names_array)):
    for friends_friend in range(len(connection_matrix)):
        if(connection_matrix[john_friend][friends_friend]==1):
            G.add_edge(names_array[john_friend], names_array[friends_friend])
pos = nx.spring_layout(G, scale=10)
#betCent = nx.betweenness_centrality(G, normalized=True, endpoints=True)
betCent = nx.closeness_centrality(G)
node_color = [2000.0 * G.degree(v) for v in G]
node_size =  [v * 1000 for v in betCent.values()]
plt.figure(figsize=(20,20))
nx.draw_networkx(G, pos=pos, with_labels=True,
                 node_color=node_color,
                 node_size=node_size )
plt.axis('off')
print(sorted(betCent, key=betCent.get, reverse=True)[:5])
print(betCent)
plt.show()