import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

mainDistricts = ["L'ile-Bizard-Sainte-Genevieve",
                 "Pierrefonds-Roxboro",
                 "Saint-Laurent",
                 "Lachine",
                 "LaSalle",
                 "Verdun",
                 "Le Sud-Ouest",
                 "Cote-des-Neiges-Notre-Dame-de-Grace",
                 "Outremont",
                 "Ville-Marie"
                 "Le Plateau-Mont-Royal",
                 "Rosemont-La-Petite-Prairie",
                 "Villeray-Saint-Michel-Parc-Extension",
                 "Ahuntsic-Cartierville",
                 "Montreal-Nord",
                 "Saint-Leonard",
                 "Mercier-Hochelaga-Monsonneuve",
                 "Anjou",
                 "Riviere-des-Prairies-Pointes-aux-Trembles"]

def drawDistrict(district):
    mp = ox.graph_from_place(district + ", Montreal, Canada")
    ox.plot_graph(mp)

def drawGraphDistrict(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=70, node_color="red")
    nx.draw_networkx_edges(G, pos, edge_color="black")
    plt.show()

def getGraphFromDistrict(district):
    G = ox.graph_from_place(district + ", Montreal, Canada", network_type='drive')
    H = nx.Graph(G)
    return H

getGraphFromDistrict("Verdun")
