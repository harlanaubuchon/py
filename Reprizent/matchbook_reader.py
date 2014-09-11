#!/usr/bin/env python
# encoding: utf-8
# csvreader.py
# Author: Harlan AuBuchon
# https://github.com/harlanaubuchon/

import csv# import reader
#import pdb; pdb.set_trace()
#from openpyxl import load_workbook

class FileProcessor(object):
    """Data object for CSV and future Excel File processing. 
       Initializes a data_set and last row_no with filename alone.
       Optional arguments for special handling can be passed in as 
       keyword arguments. The keywords keep the init simple and 
       flexible for other uses.
    """
    
    def __init__(self, filename, **kwargs):
        self.filename = str(filename)
        self.file_type = self.filename.lower().split('.')[-1:][0]
        self._data_set = []
        self.row_no = 0
        self.worksheet = None
        self.keyword_args = {'delimiter':',',
                             'quotechar':'"'
                             }
        for key, value in kwargs.items():
            self.keyword_args[key] = value

        self.method_calls = {'csv':'self._csv_reader()', 
                             'txt':'self._csv_reader()',
                             'xls':'self._excel_reader()', 
                             'xlsx':'self._excel_reader()'
                             }

        if self.file_type in self.method_calls:
            eval(self.method_calls[self.file_type])
        else:
            raise Exception("Unknown File type: '%s'" %self.file_type)


    @property
    def data_set(self):
        """ Class Properties! """
        return self._data_set


    @data_set.setter
    def data_set(self, value):
        self._data_set = value
    

    def _get_args(self, _keyword):
        """ This returns the optional arguments initialized in the Class """ 
        return self.keyword_args.get(_keyword)
    
 
    def _csv_reader(self):
        """ CSV File reader """

        with open(self.filename) as file_handle:
            csv_file = csv.reader(file_handle, **self.keyword_args)
            for row_string in csv_file:
                row_string.insert(0, self.row_no)
                self.data_set.append(row_string)
                self.row_no += 1
        self.data_set.pop(0)


    def _excel_reader(self):
        """ Excel Reader: Not yet implemented (Excel is very strange...)"""
        raise Exception

