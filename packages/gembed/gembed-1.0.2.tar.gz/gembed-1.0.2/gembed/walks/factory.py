from .random_walk import random_walk
from .baised_walk import baised_walk
from gembed.utils import fetch_bipartite_graph_node
from tqdm import trange

import random

def walker(adj_list, walks, walk_len, walker):
    print("running walker...")
    result = []
    for i in trange(walks):
        if(walker == 'random_walk'):
            for v in adj_list.keys():
                result.append(random_walk(adj_list, walk_len, v))
        elif walker == 'baised_walk':
            # create bipartie graph
            s1, s2 = fetch_bipartite_graph_node(adj_list)
            nodes = []
            if len(s1) > len(s2):
                nodes = s1
            else:
                nodes = s2

            random.shuffle(nodes)
            for node in nodes:
                result.append(baised_walk(adj_list, walk_len, node))
        else:
            raise Exception("Invalid walker")
    return result
