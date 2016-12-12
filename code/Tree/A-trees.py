#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# http://docs.sqlalchemy.org/en/latest/orm/self_referential.html

import json

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(engine)
session = Session()


class Node(Base):
    __tablename__ = 'node'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('node.id'))
    name = Column(String(32), nullable=False, unique=True)
    value = Column(Integer, CheckConstraint('value >= 0'))
    children = relationship('Node', backref=backref('parent', remote_side=[id]))

    def __repr__(_):
        return '<Node {}, {}, {}>'.format(_.name, _.value, _.children)


class NodeEncoder(json.JSONEncoder):
    def default(_, o):
        return {'label': '{}: {}'.format(o.name, o.value), 'children': o.children}


def sumTreeValuesDownwardsRecursively(node):
    return node.value + sum(map(sumTreeValuesDownwardsRecursively, node.children))

def sumTreeValuesDownwardsIteratively(node):
    stack = list(node.children)
    acc = node.value

    while stack:
        cur = stack.pop()
        acc += cur.value
        stack.extend(cur.children)

    return acc


def sumTreeValuesUpwardsRecursively(node):
    return node.value + sumTreeValuesUpwardsRecursively(node.parent) if node.parent else node.value

def sumTreeValuesUpwardsIteratively(node):
    acc = node.value

    cur = node
    while cur.parent:
        acc += cur.parent.value
        cur = cur.parent

    return acc


#        10
#       root
#      /    \
#     20    30
#    left  right
#            |
#           40
#          rright
def makeTree():
    root = Node(name="root", value=10)
    left = Node(name="left", value=20)
    right = Node(name="right", value=30)
    rright = Node(name="rright", value=40)
    right.children.append(rright)
    root.children.extend([left, right])
    return root


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    root = makeTree()
    session.add(root)
    session.commit()

    print(root)

    # recursive and iterative functions compute the same, specify impl
    sumDown = sumTreeValuesDownwardsIteratively
    sumUp = sumTreeValuesUpwardsIteratively

    right = session.query(Node).filter_by(name='right').first()

    print("down sum(root)={}, sum(right)={}".format(sumDown(root), sumDown(right)))
    print("up sum(root)={}, sum(right)={}".format(sumUp(root), sumUp(right)))

    print(json.dumps(root, cls=NodeEncoder, indent=2))
