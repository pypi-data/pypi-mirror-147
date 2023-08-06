import json
import pickle

def adj_list_reader(file):
    adj_list = {};
    # Opening JSON file
    with open(file) as json_file:
        adj_list = json.load(json_file)
    return adj_list


def fetch_bipartite_graph_node(adj_list):
    colors = {}
    for key in adj_list.keys():
        colors[key] = 0
    
    for key in colors.keys():
        if colors[key] == 0 and (not dfs(adj_list, colors, 1, key)):
            raise Exception("not bipartite");

    s1 = []
    s2 = []
    for key in colors.keys():
        if colors[key] == 1:
            s1.append(key)
        else:
            s2.append(key)

    return s1, s2;

def dfs(adj, color, current_color, node):
    if color[node] != 0:
        return current_color == color[node]
    else:
        color[node] = current_color
        neighbours = adj[node]
        for neighbour in neighbours:
            if (not dfs(adj, color, -1 * current_color, neighbour[0])):
                return False
    return True


def export_pickel(data, file_name):
    with open(file_name + ".pickle", 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)