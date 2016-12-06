# coding: utf-8
from collections import Counter
from random import choice
import networkx as nx


def get_cities():
    with open('cities.txt') as f:
        for line in f:
            yield line.strip().decode('utf8').lower()


def get_edge(city):
    return city[0], city.strip(u'ъыь')[-1]


def get_weighted_edges(cities):
    counter = Counter(get_edge(city) for city in cities if not city.startswith(u'ы'))
    return [(a, b, float(weight)) for (a, b), weight in counter.iteritems()]


def get_graph():
    cities = get_cities()
    edges = get_weighted_edges(cities)
    g = nx.DiGraph()
    g.add_weighted_edges_from(edges)
    return g


def get_out_weight(graph, vertex):
    return sum(d['weight'] for u, v, d in graph.out_edges(vertex, data=True))


def choose_next_vertex(graph, vertex):
    possible_moves = [n for n in graph.neighbors(vertex) if graph[vertex][n]['weight'] > 0]
    if not possible_moves:
        return None
    scores = min((get_out_weight(graph, n), n) for n in possible_moves)
    return scores[1]


def run_shiritori_algorithm():
    g = get_graph()
    current_letter = choice(g.nodes())
    i = 0
    while True:
        next_letter = choose_next_vertex(g, current_letter)
        if not next_letter:
            print current_letter, i
            break
        g[current_letter][next_letter]['weight'] -= 1
        i += 1
        current_letter = next_letter

run_shiritori_algorithm()
