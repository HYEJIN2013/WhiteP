"""
This is conceived to be a module usable within ipython form which you can
explore hdf rfi data with some more utilities for interpreting the right
formats of time and metainfo
"""

import tables
import datetime

import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

def name_to_time(name):
    return datetime.datetime.strptime(name, "time%Y_%m_%d_%H_%M_%S")

def timestamp_string(row):
    timestamp = datetime.datetime.fromtimestamp(row["time"])
    subseconds = round(row["subtime"] * 1.0 / 200000000, 3)
    return timestamp.strftime("%H:%M:%S") + ("%.3f" % subseconds)[1:]

def integration_to_seconds(integration):
    clock = 1.0 / 200000000
    return round(integration * clock * 1024, 3)

class RFIData(object):
    def __init__(self, filename):
        self.hdf_file = tables.openFile(filename)
        self.datasets = [(name_to_time(node._v_name), node)
                        for node in self.hdf_file.listNodes("/")]

    def _dataset(self, index):
        return self.datasets[index][1]

    def close(self):
        self.hdf_file.close()

    def list_datasets(self):
        print "#\ttime"
        for i, ds in enumerate(self.datasets):
            print "%i\t%s" % (i, ds[0])

    def list_scans(self, dataset):
        print "#\ttime\t\t\tintegraion\toverflow\tshift\tgain"
        i = 0
        for row in self._dataset(dataset).Data.iterrows():
            print "%s\t%s\t%.3f\t%i\t%i\t%i" % (i, timestamp_string(row), 
                                                integration_to_seconds(row["integration"]),
                                                row["overflow"], row["shift"], row["gain"])
            i += 1

    def plot(self, dataset, scan=None, log=False):
        bandwidth = float(self._dataset(dataset)._f_getAttr("Bandwith"))
        channels = int(self._dataset(dataset)._f_getAttr("Channels"))
        if not scan == None:
            data = self._dataset(dataset).Data[scan]["channels"]
            row = self._dataset(dataset).Data[scan]
            xaxis = np.linspace(0, bandwidth, channels)
            #mask = ma.negative(ma.masked_all(data.shape))
            #mask[0] = False
            mask = np.zeros(data.shape)
            mask[0] = 1
            if not log:
                plot_data = ma.array(data, mask=mask)
                plt.ylabel("counts (linear scale)")
            else:
                plot_data = ma.array(10 * np.log10(data), mask=mask)
                plt.ylabel("counts (log scale)")
            plt.plot(xaxis, plot_data)
            plt.xlabel("Frequency (MHz)")
            textbox =  "%s\nintegration: %.3fsec.\noverflow: %i\nshift: %i\ngain: %i" % (
                                                timestamp_string(row), 
                                                integration_to_seconds(row["integration"]),
                                                row["overflow"], row["shift"], row["gain"])
            plt.title("DATASET %i SCAN %i" % (dataset, scan))
            plt.figtext(0.7, 0.7, textbox,
                        bbox = dict(facecolor='white', 
                                    edgecolor = 'black',
                                    pad = 10.0,
                                    color = 'black'))
            plt.show()
        else:
            data = self._dataset(dataset).Data.col("channels")
            mask = np.zeros(data.shape)
            mask[:,0] = 1
            if not log:
                plot_data = ma.array(data, mask=mask)
            else:
                plot_data = ma.array(10 * np.log10(data), mask=mask)
            plt.imshow(plot_data, aspect="auto")
            plt.show()
