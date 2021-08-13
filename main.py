import csv
import json

def read_airlines(filename='airlines.dat'):
    airlines = {}  # Map from code -> name
    with open(filename, encoding="utf8") as f:
        reader = csv.reader(f)
        for line in reader:
            airlines[line[4]] = line[1]
    return airlines

def read_airports(filename='airports.dat'):
    # Return a map of code -> name
    airports = {}
    with open(filename, encoding="utf8") as f:
        reader = csv.reader(f)
        for line in reader:
            airports[line[4]] = line[1]
    return airports

def read_routes(filename='routes.dat'):
    # Return a map from source -> list of destinations
    routes = {}
    with open(filename) as f:
        reader = csv.reader(f)
        for line in reader:
            if line[2] not in routes:
                routes[line[2]] = {line[4]}
            else:
                routes[line[2]].add(line[4])
    for key, value in routes.items():
        routes[key] = list(value)

    return routes

def find_paths(routes, start, end, max_segments=0):
    # excluding destination (end) from the data base of connections
    def without_dest(dictionary: dict, exception):
        routes_without_dest = {}
        for key, values in dictionary.items():
            if key not in exception:
                routes_without_dest[key] = values
        return routes_without_dest

    #creating a data base to find foutes
    data = without_dest(routes, end)

    #graph search algorithm
    final = []
    queue = []
    checked = []
    queue.append([start])
    checked.append(start)
    while queue != []:
        path = queue.pop(0)
        node = path[-1]
        if node == end:
            final.append(path)
        elif node in data:
            for i in data[node]:
                if i not in checked:
                    if i != end:
                        checked.append(i)
                        path_copy = path.copy()
                        path_copy.append(i)
                        queue.append(path_copy)
                    else:
                        path_copy = path.copy()
                        path_copy.append(i)
                        queue.append(path_copy)
                else:
                    continue

    #applying how many transfers are allowed
    selected_paths = []
    output = "no flight has been found"
    for i in final:
        if (len(i) - 2) <= max_segments:
            selected_paths.append(i)
    #puting everything into dictinaty
    final_paths = {}
    for i in range(len(selected_paths)):
        final_paths[i + 1] = final_paths.get(i + 1, selected_paths[i])


    if final_paths != {}:
        return final_paths
    else:
        return output

def rename_path(paths, airports):
    #changing XXX symbols to names of airports
    for key, value in paths.items():
        list = []
        for i in range(len(value)):
            x = airports[value[i]]
            list.append(x)
        paths[key] = list
    # saving data in output.jason file
    with open('output.json', 'w') as outfile:
        json.dump(paths, outfile, indent=2)
    return paths

def main(source, dest, max_segments=0):
    routes = read_routes()
    airports = read_airports()
    paths = find_paths(routes, source, dest, max_segments)
    output = rename_path(paths, airports)
    return output


main_result = main('SFO', 'BOS', 1)

print(main_result)


