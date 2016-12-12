# CSE6242/CX4242 Homework 4 Decision Tree

import csv
import math
from collections import defaultdict
import numpy as np
from collections import Counter
import time

# Global Variables
input_file = 'hw4-task1-data.tsv'

# Read all the input file just once and store it
data = []


class node(object):
    """Class representing a tree's node"""
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children

    def __str__(self, level=0):
        ret = "  "*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'


class AttributeValue():
    """
        Class representing a attribute value with properties
        value: attribute value string
        p: number of records with that attribute value
        entropy: entropy of the attribute value
    """
    def __init__(self, value):
        self.value = value
        self.p = 0
        self.entropy = 0

    def inc(self):
        self.p += 1

    def setEntropy(self, entropy):
        self.entropy = entropy

    def getEntropy(self):
        return self.entropy

    def __str__(self):
        return "%s %d %f" % (self.value, self.p, self.entropy)


class Attribute():
    """
        Class representing a feature or an attribute of the record.
        It has the following properties:
        name: attribute name
        index: attribute index
        values: default dict of all the possible attribute values
        isContinnuous: boolean variable determining if the attr is continuous
        median: median of the value if its continuous
        IG: information gain of the attribute
        c: list of all possible continuous values
    """
    def __init__(self, name, index, values):
        self.name = name
        self.index = index
        self.values = defaultdict(lambda: None)
        for v in values:
            self.values[v] = AttributeValue(v)
        self.isContinuous = True if (len(values) == 1 and
                                     values[0] == "continuous") else False
        self.median = -1
        self.IG = -1
        self.c = []

    def setIG(self, ig):
        self.IG = ig

    def getIG(self):
        return self.IG

    def addValues(self, values):
        for v in values:
            self.values[v] = AttributeValue(v)

    def __str__(self):
        if(self.isContinuous is True):
            return "Attribute %s %d %s %f %s" % (self.name,
                                                 self.index,
                                                 map(str, [v for k, v in
                                                     self.values.items()
                                                     if v is not None]),
                                                 self.IG, self.isContinuous)
        else:
            return "Attribute %s %d %s %f %s" % (self.name,
                                                 self.index,
                                                 map(str, [v for k, v in
                                                     self.values.items()
                                                     if v is not None]),
                                                 self.IG, self.isContinuous)


# Implement your decision tree below
class DecisionTree():
    """
        Decision Tree class provided in the starting code
        base_entropy: entropy of the base data set
        attribute_list: default dict containing information about all attributes
    """
    def __init__(self):
        self.tree = {}
        self.base_entropy = -1
        self.attribute_list = defaultdict(lambda: None)

    # Calculates the entropy given the labels
    def entropy(self, true, false):
        if true == 0 or false == 0:
            return 0
        p = true/(true+false*1.0)
        return -p*(math.log(p, 2))-(1-p)*math.log(1-p, 2)

    # Reads from attribute.txt and initialized the attribute list
    def init_attribute_list(self):
        with open("attributes.txt") as attr:
            for index, line in enumerate(attr):
                self.attribute_list[index] = Attribute(line.split(":")[0],
                                                       index,
                                                       map(lambda x:
                                                           x.strip(". "),
                                                           line.split(":")[1].
                                                           strip().split(',')))
        return self.attribute_list

    # Populate the attribute list by reading the training data. Here we count
    # the number of occurences of each of the discrete attribute values
    # and calculate the median for continuous values
    def populate_attribute_list(self, training_data, discard_attr):
        for d in training_data:
            for attr_index, attr_value in enumerate(d):
                if(attr_index not in discard_attr):
                    a = self.attribute_list[attr_index]
                    if(a is not None):
                        av = a.values[attr_value]
                        if(a.isContinuous is False):
                            if(av is not None):
                                av.inc()
                        else:
                            a.c.append(attr_value)

        for attr_index, attr in self.attribute_list.items():
            if (attr is not None and attr_index not in discard_attr):
                if(attr.isContinuous is True):

                    attr.median = int(np.median(map(
                                      lambda x: int(x) if x != '?' else None,
                                      attr.c)))
                    attr.addValues([self.lte(attr.median),
                                    self.gt(attr.median)])

    # Utility function for node name for continuous variables
    # Ex: node name cane be <= 38 for age's child if 38 is the split median
    def lte(self, median):
        return '<= %d' % median

    # Utility function same as above except for greater than values
    def gt(self, median):
        return '> %d' % median

    # We iterate over the data list and do a second pass to find
    # the occurences of the median split for continuous variables
    def populate_continous_attribute_list(self, training_data, discard_attr):
        for d in training_data:
            for attr_index, attr_value in enumerate(d):
                if(attr_index not in discard_attr and attr_value != '?'):
                    a = self.attribute_list[attr_index]
                    if(a is not None):
                        if(a.isContinuous is True):
                            if(int(attr_value) > a.median):
                                a.values[self.gt(a.median)].inc()
                            else:
                                a.values[self.lte(a.median)].inc()

    # Filters the training data for a given attribute value
    def filter_training_data(self, training_data, attr_index, attr_value):
        return [d for d in training_data
                if self.compare(self.attribute_list[attr_index],
                                d, attr_value.value)]

    # Finds the entropy for a given data set given the labels as <=50K & >50K
    def get_entropy(self, training_data):
        f = Counter(d[-1] for d in training_data)
        a = f['<=50K']
        b = f['>50K']
        return self.entropy(a, b)

    # Populates the attribute list datastrucutre with each attribute entropy
    def populate_attribute_entropy(self, training_data, discard_attr):
        for attr_index, attr in self.attribute_list.items():
            if(attr_index not in discard_attr):
                if(attr is not None):
                    for attr_value_index, attr_value in attr.values.items():
                        if(attr_value is not None):
                            e = self.get_entropy(self.filter_training_data(
                                                 training_data,
                                                 attr_index, attr_value)
                                                 )
                            attr_value.entropy = e

    # Calculates the information IG for each attribute
    def calculate_attribute_ig(self, training_data, len_data, discard_attr):
        for attr_index, attr in self.attribute_list.items():
            s = 0
            total = 0
            if(attr is not None and attr_index not in discard_attr):
                for attr_value_index, attr_value in attr.values.items():
                    if attr_value is not None:
                        total += attr_value.p
                        s += float(attr_value.p * attr_value.entropy)
                if(total == 0):
                    return -1
                attr.IG = abs(self.base_entropy - s/total)

    # Another utility entropy function
    def calculate_node_entropy(self, training_data):
        false = [x for x in enumerate(training_data) if x[1][14] != "<=50K"]
        true = len(training_data) - len(false)
        return self.entropy(len(false), true)

    # Find the attribute with max information gain
    def max_ig_attribute(self, discard_attr):
        max_ig = -1
        max_ig_attr = None
        for index, attr in self.attribute_list.items():
            if(attr is not None and attr.index not in discard_attr):
                if(attr.IG > max_ig):
                    max_ig_attr = attr
                    max_ig = attr.IG

        return max_ig_attr

    # After narrowing down select the node result depending on which
    # label (<=50K or >50K) is in majority
    def get_result(self, training_data, tree_local):
        f = Counter(d[-1] for d in training_data)
        a = f['<=50K']
        b = f['>50K']
        result = '<=50K' if a > b else '>50K'
        tree_local.children = [node("Result")]
        tree_local.children[0].children = [node(result)]

    # Recursive function this builds the tree
    def learn(self, training_data, treelocal, discard_attr=[], level=0):
        len_data = len(training_data)
        if(len_data < 100):
            self.get_result(training_data, treelocal)
            return

        self.tree = None
        self.base_entropy = self.calculate_node_entropy(training_data)
        if(self.base_entropy == 0):
            self.get_result(training_data, treelocal)
            return

        c = self.calculate_attribute_ig(training_data, len_data, discard_attr)
        if(c == -1):
            self.get_result(training_data, treelocal)
            return

        max_ig_attr = self.max_ig_attribute(discard_attr)
        if not max_ig_attr:
            self.get_result(training_data, treelocal)
            return

        treelocal.children = [node(max_ig_attr.name)]
        treelocal.children[0].children = [node(v.value) for k, v in
                                          max_ig_attr.values.items()
                                          if v is not None
                                          and
                                          v.value != 'continuous']

        discard_attr.append(max_ig_attr.index)
        for child in treelocal.children[0].children:
            training_set = []
            training_set = [d for d in training_data if
                            self.compare(max_ig_attr,
                                         d,
                                         child.value)]
            discard_attr_local = discard_attr[:]
            self.learn(training_set, child, discard_attr_local, level+1)

    # Comapres a attribute value from the record to the attribute values
    # on which it is split on. This handles both continuous and discrete
    # attribute values
    def compare(self, attr, d, b):
        a = d[attr.index]
        if a == '?':
            return True
        if attr.isContinuous and a != '?':
            if b == self.lte(attr.median):
                return int(a) <= attr.median
            if b == self.gt(attr.median):
                return int(a) > attr.median
        else:
            return a == b

    # Gets the attribute index from the attribute_list defaultdict
    def get_attr_index(self, attr_name):
        for k, v in self.attribute_list.items():
            if(v.name == attr_name):
                return v.index

    # Classify function does simple traversal down the decision tree
    def classify(self, test_instance, node):
        while(node.value != "Result"):
            attr = self.attribute_list[self.get_attr_index(node.value)]
            for child_node in node.children:
                if self.compare(attr, test_instance, child_node.value):
                    node = child_node.children[0]
        return node.children[0].value


def run_decision_tree():

    # Load data set
    with open(input_file) as tsv:
        data = [tuple(line) for line in csv.reader(tsv, delimiter="\t")]
    print "Number of records: %d" % len(data)

    # Split training/test sets
    # You need to modify the following code for cross validation.
    K = 10

    # Stores accuracy of the 10 runs
    accuracy = []
    start = time.clock()
    for k in range(K):
        print "Doing fold ", k
        training_set = [x for i, x in enumerate(data) if i % K != k]
        test_set = [x for i, x in enumerate(data) if i % K == k]

        tree = DecisionTree()
        tree.init_attribute_list()
        tree.populate_attribute_list(training_set, discard_attr=[])
        tree.populate_continous_attribute_list(training_set, discard_attr=[])
        tree.populate_attribute_entropy(training_set, discard_attr=[])

        # Construct a tree using training set
        root_node = node("root")
        tree.learn(training_set, root_node)

        # Classify the test set using the tree we just constructed
        results = []
        for instance in test_set:
            result = tree.classify(instance[:-1], root_node.children[0])
            results.append(result == instance[-1])

        # Accuracy
        acc = float(results.count(True))/float(len(results))
        print "accuracy: %.4f" % acc
        accuracy.append(acc)
        del tree

    mean_accuracy = math.fsum(accuracy)/10
    print "Accuracy  %f " % (mean_accuracy)
    print "Took %f secs" % (time.clock() - start)
    # Writing results to a file (DO NOT CHANGE)
    f = open("result.txt", "w")
    f.write("accuracy: %.4f" % mean_accuracy)
    f.close()


if __name__ == "__main__":
    run_decision_tree()
