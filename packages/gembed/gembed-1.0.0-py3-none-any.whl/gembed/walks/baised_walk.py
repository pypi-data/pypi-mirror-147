import random

def baised_walk(adj_list, walk_len, start_node):
    walk = [start_node]

    while len(walk) < walk_len:
        cur = walk[-1]
        neighbours = adj_list[cur]
        if len(neighbours) > 0:
            rand = random.uniform(0, 1)
            # cummulative sum
            sum = 0
            found = 0
            for neighbour in neighbours:
                weight = neighbour[1]
                sum += weight
                if sum >= rand:
                    walk.append(neighbour[0])
                    found = 1
                    break;
            if found == 0:
                break
        else:
            break
    return walk
