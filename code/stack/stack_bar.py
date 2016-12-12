import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from six.moves import zip

def stack_bar(ax, list_of_vals, color_cyle=None, **kwargs):
    """
    Generalized stacked bar graph.
    kwargs are passed through to the call to `bar`
    Parameters
    ----------
    ax : matplotlib.axes.Axes
       The axes to plot to
    list_of_vals : iterable
       An iterable of values to plot
    color_cycle : iterable, optional
       color_cycle is None, defaults
       to `cycle(['r', 'g', 'b', 'k'])`
    """
    if color_cyle is None:
        color_cyle = cycle(['r', 'g', 'b', 'k'])
    else:
        color_cycle = cycle(color_cycle)


    v0 = len(list_of_vals[0])
    if any(v0 != len(v) for v in list_of_vals[1:]):
           raise ValueError("All inputs must be the same length")

    edges = np.arange(v0)
    bottom = np.zeros(v0)
    for v, c in zip(list_of_vals, color_cyle):
        ax.bar(edges, v, bottom=bottom, color=c, **kwargs)
        bottom += np.asarray(v)


fig, ax = plt.subplots(1, 1)
values = [(20,35,30,35,27),(25,32,34,20,25),(3,4,5,6,7)]
stack_bar(ax, values, width=1)
