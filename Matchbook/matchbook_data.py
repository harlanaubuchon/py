#!/usr/bin/env python
# encoding: utf-8
# csvdata.py
# Author: Harlan AuBuchon
# https://github.com/harlanaubuchon/

import re

class Data(object):
    'Base class representing imported csv data for processing'
    
    def __init__(self, selection, comparison, intersect_column):
        self._comparison = comparison
        self._selection = selection
        self.i_column = int(intersect_column)
        if len(self._selection) > 1:
            self.single_list = False
        else:
            self.single_list = True


    def _display_data(self):
        'Debugging method for displaying raw data as selected'
        if self.single_list == True:
            return(self.selection[0][self.i_column])
        else:
            for select_string in self.selection:
                return(select_string[self.i_column])


    @property
    def selection(self):
        return self._selection

    @selection.setter
    def selection(self, value):
        self._selection = value


    @property
    def comparison(self):
        return self._comparison


    @comparison.setter
    def comparison(self, value):
        self._comparison = value
    
    
    def get_list_form(self, _f, _row):

    	return _f[_row][self.i_column][0]

    def get_canonical_form(self, _f, _row):

        return re.findall("[\w']+", _f[_row][self.i_column][0])