import json
from queue import Queue
import boto3


# dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

def BFS(adj_list, start_node, target_node):
    # according to mp3 FAQ
    if start_node == target_node:
        return 0

    # Set of visited nodes to prevent loops
    visited = set()
    queue = Queue()

    # Add the start_node to the queue and visited list
    queue.put(start_node)
    visited.add(start_node)

    # start_node has not parents
    parent = dict()
    parent[start_node] = None

    # Perform step 3
    path_found = False
    while not queue.empty():
        current_node = queue.get()
        if current_node == target_node:
            path_found = True
            break

        if current_node in adj_list.keys():
            for next_node in adj_list[current_node]:
                if next_node not in visited:
                    queue.put(next_node)
                    parent[next_node] = current_node
                    visited.add(next_node)

    # Path reconstruction
    path = []
    if path_found:
        path.append(target_node)
        while parent[target_node] is not None:
            path.append(parent[target_node])
            target_node = parent[target_node]
        path.reverse()
    return len(path) - 1


def add_path_dynamo_db(source, destination, distance, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('ShortestPaths')

    response = table.put_item(
        Item={
            'source': source,
            'destination': destination,
            'distance': distance
        }
    )
    return response


# Driver program to test above functions

if __name__ == '__main__':

    graph = '{"graph": "Chicago->Urbana,Urbana->Springfield,Chicago->Lafayette"}'
    graph_dict = json.loads(graph)
    # print(graph_dict)
    graph_str = graph_dict['graph']
    edges = graph_str.split(',')
    # print(edges)
    graph_dict1 = dict()
    city_list = []
    for i in edges:
        i2 = i.split('->')
        if i2[0] in graph_dict1:
            graph_dict1[i2[0]].append(i2[1])
        else:
            graph_dict1[i2[0]] = [i2[1]]
        city_list.append(i2[0])
        city_list.append(i2[1])

    # print(graph_dict1.items())
    # print(BFS(graph_dict1, 'Chicago', 'Springfield'))
    # print(BFS(graph_dict1, 'Chicago', 'Lafayette'))

    # list implementation
    unique_city_list = []
    for city in city_list:
        if city not in unique_city_list:
            unique_city_list.append(city)

    i = 0  # iterator
    while i < len(unique_city_list):
        source = unique_city_list[i]
        # print(source + source + "{distance}".format(distance=BFS(graph_dict1, source, source)))
        add_path_dynamo_db(source, source, BFS(graph_dict1, source, source))
        if i < len(unique_city_list):
            temp_dest_list = unique_city_list[i + 1:]
            for dest in temp_dest_list:
                add_path_dynamo_db(source, dest, BFS(graph_dict1, source, dest))
                add_path_dynamo_db(dest, source, BFS(graph_dict1, dest, source))
                # print(source + dest + "{distance}".format(distance=BFS(graph_dict1, source, dest)))
                # print(dest + source + "{distance}".format(distance=BFS(graph_dict1, dest, source)))
        i += 1
