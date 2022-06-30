import time
from urllib.parse import parse_qs
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

mainDistricts = ["L'Île-Bizard–Sainte-Geneviève",
                 "Pierrefonds-Roxboro", #
                 "Saint-Laurent", #
                 "LaSalle", #
                 "Verdun",
                 "Le Sud-Ouest", #
                 "Côte-des-Neiges–Notre-Dame-de-Grâce", #
                 "Outremont",
                 "Ville-Marie", #
                 "Le Plateau-Mont-Royal", #
                 "Rosemont—La Petite-Patrie", #
                 "Villeray-Saint-Michel-Parc-Extension", #
                 "Ahuntsic-Cartierville", #
                 "Montreal-Nord",
                 "Saint-Leonard", #
                 "Mercier–Hochelaga-Maisonneuve", #
                 "Anjou"] #

districtwalk = ["L'Île-Bizard–Sainte-Geneviève",
                 "Verdun",
                 "Outremont",
                 "Montreal-Nord"]

disctrictError = ["Lachine", "Rivière-des-Prairies–Pointe-aux-Trembles"]

drone_speed = 45 # km/h
drive_speed = 10 # km/h
walk_speed = 15 # km/h

drone_per_district = [
    ("L'Île-Bizard–Sainte-Geneviève", 2),
    ("Pierrefonds-Roxboro", 3),
    ("Saint-Laurent", 5),
    ("LaSalle", 3),
    ("Verdun", 1),
    ("Le Sud-Ouest", 3),
    ("Côte-des-Neiges–Notre-Dame-de-Grâce",3),
    ("Outremont",1),
    ("Ville-Marie",3),
    ("Le Plateau-Mont-Royal",2),
    ("Rosemont—La Petite-Patrie",3),
    ("Villeray-Saint-Michel-Parc-Extension",5),
    ("Ahuntsic-Cartierville",4),
    ("Montreal-Nord",2),
    ("Saint-Leonard",3),
    ("Mercier–Hochelaga-Maisonneuve",3),
    ("Anjou",2)
]

total_drive = 422
drive_per_district = [
    ("L'Île-Bizard–Sainte-Geneviève", 30),
    ("Pierrefonds-Roxboro", 30),
    ("Saint-Laurent", 30),
    ("LaSalle", 20),
    ("Verdun", 10),
    ("Le Sud-Ouest", 30),
    ("Côte-des-Neiges–Notre-Dame-de-Grâce",20),
    ("Outremont",20),
    ("Ville-Marie",20),
    ("Le Plateau-Mont-Royal",20),
    ("Rosemont—La Petite-Patrie",30),
    ("Villeray-Saint-Michel-Parc-Extension",30),
    ("Ahuntsic-Cartierville",30),
    ("Montreal-Nord",30),
    ("Saint-Leonard",30),
    ("Mercier–Hochelaga-Maisonneuve",20),
    ("Anjou",22)
]

walk_per_district = [
    ("L'Île-Bizard–Sainte-Geneviève", 2),
    ("Pierrefonds-Roxboro", 3),
    ("Saint-Laurent", 5),
    ("LaSalle", 3),
    ("Verdun", 1),
    ("Le Sud-Ouest", 3),
    ("Côte-des-Neiges–Notre-Dame-de-Grâce",3),
    ("Outremont",1),
    ("Ville-Marie",3),
    ("Le Plateau-Mont-Royal",2),
    ("Rosemont—La Petite-Patrie",3),
    ("Villeray-Saint-Michel-Parc-Extension",5),
    ("Ahuntsic-Cartierville",4),
    ("Montreal-Nord",2),
    ("Saint-Leonard",3),
    ("Mercier–Hochelaga-Maisonneuve",3),
    ("Anjou",2)
]

drone_routes_colors=['darkcyan',
                     'darkorange',
                     'yellowgreen',
                     'darkred',
                     'blue',
                     'forestgreen',
                     'goldenrod',
                     'lime',
                     'orangered',
                     'mediumorchid',
                     'aqua',
                     'red',
                     'lightcoral',
                     'gold',
                     'orange',
                     'burlywood',
                     'limegreen']

def getGraphFromDistrict(district):
    t1 = time.time()
    print("Downloading " + district + " map..")
    G = ox.graph_from_place(district + ", Montreal, Canada", network_type='walk', simplify=True)
    t2 = time.time()
    print("Done " + str(round(t2 - t1, 2)) + " second(s)")
    G = G.to_undirected()
    ox.save_graphml(G, "./maps/"+district+"_undirected_walk.graphml")

def getnumberofdrones(district):
    for (i, j) in drone_per_district:
        if (i == district):
            return j
    return 0

def getnumberofdrive(district):
    for (i, j) in drive_per_district:
        if (i == district):
            return j
    return 0

def getnumberofwalk(district):
    for (i, j) in walk_per_district:
        if (i == district):
            return j
    return 0


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

def eulerian_route_save(G, district):
    nG = removeOneNeighbor(G)
    print("Finding Eulerian Path...")
    t1 = time.time()
    euler = nx.eulerize(nG)
    t2 = time.time()
    print("Done " + str(round(t2 - t1, 2)) + " second(s)")
    path = nx.eulerian_path(euler)
    f = open("paths/" + district + "_walk.txt", "w")
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

def get_graph_walk_from(district):
    return ox.load_graphml("maps/" + district + "_undirected_walk.graphml")

def get_path_from_file(district):
    lst = []
    f = open("paths/" + district + ".txt", "r")
    lines = f.readlines()
    for line in lines:
        lst.append(int(line.strip()))
    return lst

def get_path_walk_from_file(district):
    lst = []
    f = open("paths/" + district + "_walk.txt", "r")
    lines = f.readlines()
    for line in lines:
        lst.append(int(line.strip()))
    return lst

def estimate_length(G, path):
    i = 0
    total = 0
    while i < len(path) - 1:
        src = path[i]
        dest = path[i + 1]
        if ("length" in G[src][dest][0]):
            total += G[src][dest][0]["length"]
        i += 1
    return round(total / 1000, 2)

def estimate_time_drone(distance):
    return distance / drone_speed


def hourstomin(hours):
    return hours * 60 / 100

def estimate_time_road(distance):
    t = distance / drive_speed
    return t * 60

def estimate_time_walk(distance):
    t = distance / walk_speed
    return t * 60

def printprocess(district):
    if (district == "L'Île-Bizard–Sainte-Geneviève"):
        print("Processing \033[38;5;6mL'Île-Bizard–Sainte-Geneviève\033[0;0m ...")
    if (district == "Pierrefonds-Roxboro"):
        print("Processing \033[38;5;214mPierrefonds-Roxboro\033[0;0m ...")
    if (district == "Saint-Laurent"):
        print("Processing \033[38;5;118mSaint-Laurent\033[0;0m ...")
    if (district == "LaSalle"):
        print("Processing \033[38;5;160mLaSalle\033[0;0m ...")
    if (district == "Verdun"):
        print("Processing \033[38;5;25mVerdun\033[0;0m ...")
    if (district == "Le Sud-Ouest"):
        print("Processing \033[38;5;40mLe Sud-Ouest\033[0;0m ...")
    if (district == "Côte-des-Neiges–Notre-Dame-de-Grâce"):
        print("Processing \033[38;5;220mCôte-des-Neiges–Notre-Dame-de-Grâce\033[0;0m ...")
    if (district == "Outremont"):
        print("Processing \033[38;5;82mOutremont\033[0;0m ...")
    if (district == "Ville-Marie"):
        print("Processing \033[38;5;202mVille-Marie\033[0;0m ...")
    if (district == "Le Plateau-Mont-Royal"):
        print("Processing \033[38;5;201mLe Plateau-Mont-Royal\033[0;0m ...")
    if (district == "Rosemont—La Petite-Patrie"):
        print("Processing \033[38;5;80mRosemont—La Petite-Patrie\033[0;0m ...")
    if (district == "Villeray-Saint-Michel-Parc-Extension"):
        print("Processing \033[38;5;196mVilleray-Saint-Michel-Parc-Extension\033[0;0m ...")
    if (district == "Ahuntsic-Cartierville"):
        print("Processing \033[38;5;197mAhuntsic-Cartierville\033[0;0m ...")
    if (district == "Montreal-Nord"):
        print("Processing \033[38;5;226mMontreal-Nord\033[0;0m ...")
    if (district == "Saint-Leonard"):
        print("Processing \033[38;5;214mSaint-Leonard\033[0;0m ...")
    if (district == "Mercier–Hochelaga-Maisonneuve"):
        print("Processing \033[38;5;228mMercier–Hochelaga-Maisonneuve\033[0;0m ...")
    if (district == "Anjou"):
        print("Processing \033[38;5;46mAnjou\033[0;0m ...")


def launchDrones():
    print("~~~~~~~~~~~~~   Launching Drones   ~~~~~~~~~~~~~")
    routes = []
    montrealdistricts = []
    for dist in mainDistricts:
        printprocess(dist)
        G = get_graph_from(dist)
        montrealdistricts.append(G)
        path = get_path_from_file(dist)
        lg = estimate_length(G, path)
        drones = getnumberofdrones(dist)
        print("     -> Distance travelled : " + str(round(lg/drones, 2)) + " km.")
        print("     -> Estimated time     : " + str(round(estimate_time_drone(lg) / drones)) + " hour(s).")
        print("     -> Drones needed : " + str(drones) + " drones.")
        print("")
        routes.append(path)
    montreal = nx.compose_all(montrealdistricts)
    print("SCHEMA DU TRACE DES DRONES DANS LA VILLE (NE MARCHE PAS SUR DOCKER)")
    ox.plot_graph_routes(montreal, routes, route_colors=drone_routes_colors, route_linewidths=2, orig_dest_size=50)

def launchDrive():
    print("~~~~~~~~~~~~~   Launching Road Machines   ~~~~~~~~~~~~~")
    routes = []
    montrealdistricts = []
    for dist in mainDistricts:
        printprocess(dist)
        G = get_graph_from(dist)
        montrealdistricts.append(G)
        path = get_path_from_file(dist)
        lg = estimate_length(G, path)
        machines = getnumberofdrive(dist)
        print("     -> Distance travelled : " + str(round(lg/machines, 2)) + " km per machine")
        print("     -> Estimated time     : " + str(round(estimate_time_road(lg/machines))) + " minute(s) per machine.")
        print("     -> Machines needed : " + str(machines) + " machine(s).")
        print("")
        routes.append(path)
    montreal = nx.compose_all(montrealdistricts)
    print("SCHEMA DU TRACE DES DENEIGEUSES DE ROUTE DANS LA VILLE (NE MARCHE PAS SUR DOCKER)")
    ox.plot_graph_routes(montreal, routes, route_colors=drone_routes_colors, route_linewidths=2, orig_dest_size=50)

def launchWalk():
    print("~~~~~~~~~~~~~   Launching Pedestrian Machines   ~~~~~~~~~~~~~")
    routes = []
    montrealdistricts = []
    for dist in mainDistricts:
        G = get_graph_walk_from(dist)
        montrealdistricts.append(G)
        if dist in districtwalk:
            printprocess(dist)   
            path = get_path_walk_from_file(dist)
            lg = estimate_length(G, path)
            machines = getnumberofwalk(dist)
            print("     -> Distance travelled : " + str(round(lg/machines, 2)) + " km per machine")
            print("     -> Estimated time     : " + str(round(estimate_time_road(lg/machines))) + " minute(s) per machine.")
            print("     -> Machines needed : " + str(machines) + " machine(s).")
            print("")
            routes.append(path)
    montreal = nx.compose_all(montrealdistricts)
    print("SCHEMA DU TRACE DES DENEIGEUSES DE TROTTOIR DANS LA VILLE (NE MARCHE PAS SUR DOCKER)")
    ox.plot_graph_routes(montreal, routes, route_colors=['cyan', 'blue', 'green', 'yellow'], route_linewidths=2, orig_dest_size=50)




def demo():
    launchDrones()
    print("")
    launchDrive()
    print("")
    launchWalk()

demo()

