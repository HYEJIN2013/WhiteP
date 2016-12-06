# coding: utf-8
from collections import Counter
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


def add_final_vertices(g):
    g.add_weighted_edges_from((v, v + u'_finish', 1.0) for v in g.nodes())


def evaluate_letters():
    g = get_graph()
    add_final_vertices(g)
    pr = nx.pagerank(g)

    for a, b in sorted(pr.items(), key=lambda x: x[1]):
        if a[1:] == '_finish':
            print a[0], b

evaluate_letters()
