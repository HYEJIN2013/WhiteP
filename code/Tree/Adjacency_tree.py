# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.encoding import python_2_unicode_compatible
import json


@python_2_unicode_compatible
class Node(object):
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.tree = kwargs['tree']
        self.parent_id = kwargs['parentId']
        self.title = kwargs['title']

    def __repr__(self):
        return '<Node: {}>'.format(self.title).encode('utf-8')

    def __str__(self):
        return self.title

    def is_root(self):
        return not self.parent_id

    def get_parent(self):
        return self.tree.items[self.parent_id]

    def get_ancestors(self):
        node, path = self, []
        while 42:
            path.insert(0, node.title)
            if node.is_root():
                break
            node = node.get_parent()
        return path


class Tree(object):
    def __init__(self, dictionary):
        self.items = {k: Node(id=k, tree=self, **v) for k, v in dictionary.items()}

    def get_parents(self, category_id):
        return self.items[category_id].get_ancestors()


with open('categories.json') as f:
    categories = json.load(f)


tree = Tree(categories)

print({k: v.get_ancestors() for k, v in t.items.items()})
