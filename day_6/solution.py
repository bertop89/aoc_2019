from collections import defaultdict


def direct_orbits(parsed_input):
    orbits_dict = defaultdict(list)
    orbits_unique = set()
    for parent, son in parsed_input:
        orbits_dict[parent].append(son)
        orbits_unique.add(parent)
        orbits_unique.add(son)
    return orbits_dict, orbits_unique


def compute_descendents(unique_orbit, orbits_dict):
    if len(orbits_dict[unique_orbit]) == 0:
        return 0
    else:
        all = []
        for son in orbits_dict[unique_orbit]:
            all.append(1 + compute_descendents(son, orbits_dict))
        return sum(all)


#input_file = open('./input.txt','r')
input_file = open('./input_test.txt','r')
parsed_input = input_file.readlines()
parsed_input = [x.replace('\n', '').split(')') for x in parsed_input]
orbits_dict, orbits_unique = direct_orbits(parsed_input)

# part 1
print(sum([ compute_descendents(unique_orbit, orbits_dict) for unique_orbit in orbits_unique]))

# part 2
orbits_dict_both = orbits_dict.copy()
for k, v in orbits_dict.items():
    for e in v:
        if k not in orbits_dict_both[e]:
            orbits_dict_both[e].append(k)

def compute_shortest_path(orbits_dict_both, start, end):
    open_paths = [[start]]
    shortest_path = list(range(1000))
    while len(open_paths) > 0:
        current_path = open_paths.pop()
        if len(current_path) < len(shortest_path):
            for next_move in orbits_dict_both[current_path[-1]]:
                if next_move == end and len(current_path)+1 < len(shortest_path):
                    shortest_path = current_path + [next_move]
                elif next_move not in current_path:
                    open_paths.append(current_path + [next_move])
    return shortest_path

print(len(compute_shortest_path(orbits_dict_both, 'K', 'I')))