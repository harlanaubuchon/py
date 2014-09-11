#!/usr/bin/env python
# encoding: utf-8
# reprizent.py
# Author: Harlan AuBuchon
# https://github.com/harlanaubuchon/

__author__ = 'harlanaubuchon'

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matchbook_reader as mb
from matplotlib.backends.backend_pdf import PdfPages
from mpltools import style
import csv


class Render():
    """ Plot Class for processing matplotlib graphs with csv files and outputs
    A single multi-page PDF or shows the plotted data.
    """

    def __init__(self, graph_type, file_name):
        self.plots = []
        self.graph_type = graph_type
        self.home = os.getcwd()
        self.path = os.path.join(self.home, 'data')
        self.file_name = os.path.join(self.path, file_name)
        self.colors = plt.cm.Set3(np.linspace(0, 1, 30))
        ### self.colors = ['#fa8174', '#8dd3c7', '#feffb3', '#bfbbd9', '#81b1d2', '#fdb462', '#b3de69', '#bc82bd',
        ###                '#ccebc4', '#ffed6f', 'w']
        self.lines = ['-', '--', ':', '-.']
        self.csv_array = {}
        self.CsvFile = mb.FileProcessor(self.file_name)
        self.prim_array_keys = []
        self.sec_array_keys = []
        self.plot_set = {}
        self.data_array = '%Y%m%d %H:%M'
        self.date_legend = '%B %d, %Y %H:%M'
        self.date_axis = '%m/%d/%y %H:%M:%S'
        self.y_label = 'Y Label'
        self.x_label = 'Time'
        self.y2_label = 'Secondary Axis Label'


    def setup_files(self):
        """
        Future:  Implement file setup to automatically key and template csv data.
        """
        pass


    def array_builder(self):
        for i in range(len(self.CsvFile.data_set)):
            key = "{0:s}:{1:s}".format(self.CsvFile.data_set[i][1], self.CsvFile.data_set[i][2])
            data_range = mdates.strpdate2num(self.data_array)(self.CsvFile.data_set[i][6])
            data_value = self.CsvFile.data_set[i][7]
            self.csv_array.setdefault(key, [[], []])
            self.csv_array[key][0].append(data_range)
            self.csv_array[key][1].append(data_value)

        return self.csv_array


    def prepare_plot(self, csv_file_name):
        if os.path.isfile(os.path.join(self.home, csv_file_name)):
            with open(os.path.join(self.home, csv_file_name)) as file_handle:
                csv_file = csv.reader(file_handle)
                for row_string in csv_file:
                    if row_string[1] == '1':
                        self.prim_array_keys.append(row_string[0])

                    if row_string[2] == '1':
                        self.sec_array_keys.append(row_string[0])


    def grapher(self, csv_array, ax, ax2):
        """
        grapher will read the python array built from the CSV file output of array_builder
        and produce twin plots one larger with an alpha value of 0.2

        Plot layout:
        left = 0.06
        bottom = 0.12
        right = 0.76
        top = 0.94
        wspace = 0.20
        hspace = 0.20
        """
        color_cnt = 0
        line_cnt = 0
        cycle_cnt = 0

        for array_key in self.prim_array_keys:
            #print "color_cnt = %s\nline_cnt = %s\ncycle_cnt = %s\n" % (color_cnt, line_cnt, cycle_cnt)
            ax.plot_date(x=np.array(csv_array[array_key][0]),
                         y=np.array(csv_array[array_key][1]),
                         fmt=self.lines[line_cnt],
                         label=array_key,
                         c=self.colors[color_cnt]
            )
            ax.plot_date(x=np.array(csv_array[array_key][0]),
                         y=np.array(csv_array[array_key][1]),
                         fmt=self.lines[line_cnt],
                         alpha=0.2,
                         lw=6.0,
                         c=self.colors[color_cnt]
            )

            if color_cnt < len(self.colors) - 1:
                color_cnt += 1

            else:
                color_cnt = 0
                cycle_cnt += 1

            if cycle_cnt == 1:
                if line_cnt < len(self.lines) - 1:
                    line_cnt += 1

                else:
                    line_cnt = 0

                cycle_cnt -= 1

        if len(self.sec_array_keys) > 0:
            for array_key_2 in self.sec_array_keys:
                ax2.plot_date(x=np.array(csv_array[array_key_2][0]),
                              y=np.array(csv_array[array_key_2][1]),
                              fmt=self.lines[line_cnt],
                              label=array_key_2,
                              c=self.colors[color_cnt]
                )
                ax2.plot_date(x=np.array(csv_array[array_key_2][0]),
                              y=np.array(csv_array[array_key_2][1]),
                              fmt=self.lines[line_cnt],
                              alpha=0.2,
                              lw=6.0,
                              c=self.colors[color_cnt]
                )

                if color_cnt < len(self.colors) - 1:
                    color_cnt += 1

                else:
                    color_cnt = 0
                    cycle_cnt += 1

                if cycle_cnt == 1:
                    if line_cnt < len(self.lines) - 1:
                        line_cnt += 1

                    else:
                        line_cnt = 0

                    cycle_cnt -= 1


    def preparePlot(self):
        for i in os.listdir(self.home):
            if i.startswith('prepare-plot'):
                self.plots.append(i)

        # TODO: Fix this
        # if len(self.plots) > 0:
        #     with open('prepare-plot_template.csv', 'w+') as csv_handle:
        #         csvwrite = csv.writer(csv_handle, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        #         csvwrite.writerow(["sublot_name", "primary_axis", "secondary_axis"])
        #         for i in self.csv_array.keys():
        #             csvwrite.writerow([i, 1, 0])


    def processPlot(self):
        self.preparePlot()
        if os.path.isfile(os.path.join(self.home, 'data_sets.csv')):
            with open(os.path.join(self.home, 'data_sets.csv')) as file_handle:
                csv_file = csv.reader(file_handle)
                row_cnt = 0
                for row_string in csv_file:
                    if row_cnt == 0:
                        pass
                    else:
                        self.plot_set[row_string[0]] = [row_string[1], row_string[2], row_string[3]]
                    row_cnt += 1


            sorted_set = self.plot_set.keys()
            sorted_set.sort()
            seq_cnt = 1

            for seq in sorted_set:
                print 'Processing - %s of %s' % (seq_cnt, len(sorted_set))
                seq_cnt += 1
                plot_text = self.plot_set[seq][2]

                for p in range(len(self.plots)):
                    print 'Processing set - %s of %s' % (p + 1, len(self.plots))
                    style.use('mpl_dark_harlan')
                    fig = plt.figure(p + 1)
                    ax = fig.add_subplot(111)
                    ax2 = ax.twinx()
                    ax_array = self.array_builder()
                    self.prepare_plot(self.plots[p])
                    self.grapher(ax_array, ax, ax2)

                    ax.set_xlim(left=mdates.strpdate2num(self.date_axis)(self.plot_set[seq][0]),
                                right=mdates.strpdate2num(self.date_axis)(self.plot_set[seq][1]))

                    plt.title('%s - %s' % (seq, (self.plots[p].split('_')[1].replace('-', ' ').replace('.csv', ''))))
                    ax.set_ylabel(self.y_label)

                    if len(self.sec_array_keys) == 1:
                        ax2.set_ylabel(self.sec_array_keys[0])
                    else:
                        ax2.set_ylabel(self.y2_label)

                    ax.set_xlabel(self.x_label)
                    ax.set_xticklabels(ax_array.keys()[0], rotation=45, fontsize=8)
                    ax.xaxis.set_major_formatter(mdates.DateFormatter(self.date_legend))
                    fig.autofmt_xdate()

                    plt.grid(True)
                    ax.legend(loc=2, borderaxespad=1., fontsize=10)
                    ax2.legend(loc=1, borderaxespad=1., fontsize=10)

                    # fig.text(.1, .1, plot_text, horizontalalignment='center')

                    self.prim_array_keys = []
                    self.sec_array_keys = []

                    fig.subplots_adjust(left=0.06, bottom=0.12, right=0.94, top=0.94, wspace=None, hspace=None)
                    fig.set_size_inches(22, 16, forward=True)

                    if self.graph_type.lower() == "pdf":
                        self.savePdf()

                    else:
                        plt.show()

                    plt.close()


        print 'Processing complete'


    def savePdf(self):
        with PdfPages('Complete_Plotted_Datasets.pdf') as ppdf:
            ppdf.savefig()


if __name__ == '__main__':
    X = Render('pdf', 'hourly_precipitation.csv')
    X.y_label = 'Precipitation in inches'
    X.processPlot()