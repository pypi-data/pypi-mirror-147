import random

def random_walk(adj_list, walk_len, start_node):
    walk = [start_node]
    while len(walk) < walk_len:
        cur = walk[-1]
        neighbours = adj_list[cur]
        if len(neighbours) > 0:
            rd = random.randint(0, len(neighbours) - 1)
            walk.append(neighbours[rd][0])
        else:
            break
    return walk