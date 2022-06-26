import time
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

mainDistricts = ["L'Île-Bizard–Sainte-Geneviève",
                 "Pierrefonds-Roxboro",
                 "Saint-Laurent",
                 "LaSalle",
                 "Verdun",
                 "Le Sud-Ouest",
                 "Côte-des-Neiges–Notre-Dame-de-Grâce",
                 "Outremont",
                 "Ville-Marie",
                 "Le Plateau-Mont-Royal",
                 "Rosemont—La Petite-Patrie",
                 "Villeray-Saint-Michel-Parc-Extension",
                 "Ahuntsic-Cartierville",
                 "Montreal-Nord",
                 "Saint-Leonard",
                 "Mercier–Hochelaga-Maisonneuve",
                 "Anjou"]

disctrictError = ["Lachine", "Rivière-des-Prairies–Pointe-aux-Trembles"]



def getGraphFromDistrict(district):
    t1 = time.time()
    print("Downloading " + district + " map..")
    G = ox.graph_from_place(district + ", Montreal, Canada", network_type='drive', simplify=True)
    t2 = time.time()
    print("Done " + str(round(t2 - t1, 2)) + " second(s)")
    return G.to_undirected()

def convertToNetworkx(G):
    return nx.Graph(G)

def drawDistrict(district):
    mp = getGraphFromDistrict(district)
    ox.plot_graph(mp)

def removeOneNeighbor(G):
    undi = G.to_undirected()
    treat = True
    while treat:
        treat = False
        for node in list(undi.nodes):
            if len([n for n in undi.neighbors(node)]) == 1:
                treat = True
                undi.remove_node(node)
    return undi

def eulerian_route(G):
    nG = removeOneNeighbor(G)
    print("Finding Eulerian Path...")
    t1 = time.time()
    euler = nx.eulerize(nG)
    t2 = time.time()
    print("Done " + str(round(t2 - t1, 2)) + " second(s)")
    path = nx.eulerian_path(euler)
    lst = []
    for (i, j) in path:
        if (len(lst) == 0):
            lst.append(i)
            lst.append(j)
        else:
            lst.append(j)
    return lst

def eulerian_route_save(G, district):
    nG = removeOneNeighbor(G)
    print("Finding Eulerian Path...")
    t1 = time.time()
    euler = nx.eulerize(nG)
    t2 = time.time()
    print("Done " + str(round(t2 - t1, 2)) + " second(s)")
    path = nx.eulerian_path(euler)
    f = open("paths/" + district + ".txt", "w")
    lst = []
    for (i, j) in path:
        if (len(lst) == 0):
            lst.append(i)
            lst.append(j)
            f.writelines(str(i)+"\n")
            f.writelines(str(j)+"\n")
        else:
            lst.append(j)
            f.writelines(str(j)+"\n")
    f.close()
    return lst

def get_graph_from(district):
    return ox.load_graphml("maps/" + district + "_undirected.graphml")

def get_path_from_file(district):
    lst = []
    f = open("paths/" + district + ".txt", "r")
    lines = f.readlines()
    for line in lines:
        lst.append(int(line.strip()))
    return lst


def unSnowMontreal():
    routes = []
    montrealdistricts = []
    for dist in mainDistricts:
        G = get_graph_from(dist)
        montrealdistricts.append(G)
        path = get_path_from_file(dist)
        routes.append(path)
    montreal = nx.compose_all(montrealdistricts)
    ox.plot_graph_routes(montreal, routes, route_colors=['b', 'g', 'r', 'c', 'm', 'y', 'b', 'g', 'r', 'c', 'm', 'y', 'b', 'g', 'r', 'c', 'm'])

unSnowMontreal()