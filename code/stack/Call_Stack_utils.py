#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def cheese(frame=None, slient=False):
    import sys
    import tempfile
    import webbrowser
    import pygraphviz as pgv

    if not frame:
        frame = sys._getframe().f_back

    G = pgv.AGraph(strict=False, directed=True)

    call_sequence = []

    subgraph_dict = {}

    while frame:
        code = frame.f_code
        filename = code.co_filename
        firstlineno = code.co_firstlineno
        function = code.co_name

        if filename not in subgraph_dict:
            subgraph_dict[filename] = filename
            subgraph_dict[filename] = G.add_subgraph(
                name='cluster' + filename,
                label=filename
            )
        subgraph = subgraph_dict[filename]

        node_name = '{}:{}:{}'.format(filename, firstlineno, function)
        if not subgraph.has_node(node_name):
            subgraph.add_node(
                node_name,
                label='{}:{}'.format(firstlineno, function)
            )

        call_sequence.append(frame)
        frame = frame.f_back

    call_sequence.reverse()

    for index in range(len(call_sequence) - 1):
        caller_frame = call_sequence[index]
        caller_filename = caller_frame.f_code.co_filename
        caller_firstlineno = caller_frame.f_code.co_firstlineno
        caller_function = caller_frame.f_code.co_name
        caller_lineno = caller_frame.f_lineno
        caller_subgraph = subgraph_dict[caller_filename]

        called_frame = call_sequence[index + 1]
        called_filename = called_frame.f_code.co_filename
        called_firstlineno = called_frame.f_code.co_firstlineno
        called_function = called_frame.f_code.co_name
        called_subgraph = subgraph_dict[called_filename]

        if index == 0:
            color = 'green'
        elif index == len(call_sequence) - 2:
            color = 'red'
        else:
            color = 'black'

        G.add_edge(
            '{}:{}:{}'.format(caller_filename,
                              caller_firstlineno,
                              caller_function),
            '{}:{}:{}'.format(called_filename,
                              called_firstlineno,
                              called_function),
            color=color,
            label='#{} at {}'.format(index + 1, caller_lineno)
            # ltail=caller_subgraph.name,
            # lhead=called_subgraph.name,
        )

    fd, name = tempfile.mkstemp('.png')

    G.draw(name, prog='dot')
    G.close()

    if not slient:
        webbrowser.open('file://' + name)

    return name
