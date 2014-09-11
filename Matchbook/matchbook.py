#!/usr/bin/env python
# encoding: utf-8
# matchbook.py
# Author: Harlan AuBuchon
# https://github.com/harlanaubuchon/

import matchbook_reader as r, matchbook_data as d
from fuzzywuzzy import fuzz
import csv


class Process():
    """ Matchbook Class for processing fuzzy matches"""
    def __init__(self, selection, comparison, ratio):
        self.selection = selection
        self.comparison = comparison
        self.ratio = ratio
        self.min_ratio = 67
        self.match_exact = []
        self.match_fuzzy = []
        self.match_none = []
        self.results = []
        self._CSV_COLUMNS = ['S_ROW', 
                             'SELECT_NAME', 
                             'S_CODE', 
                             'C_ROW', 
                             'COMPARE_NAME', 
                             'C_CODE', 
                             'SCORE']

    def fuzzyMatcher(self):
        """ Fuzzy matching logic, returns two files with results """

        selectSize = len(self.selection)
        for s in self.selection:
            #incCounter()
            sRow, sList, sCode = s
            for c in self.comparison:
                #incCounter()
                cRow, cList, cCode = c
                scoreValue = fuzz.token_sort_ratio(sList, cList)
                dataSet = [sRow, sList, sCode, cRow, cList, cCode, scoreValue]
                if scoreValue >= self.ratio:
                    #print('Hit: Select row %s on Compare row %s with score of %s' %(sRow, cRow, scoreValue))
                    self.match_exact.append(dataSet)

                if scoreValue < self.ratio and scoreValue > self.min_ratio:
                    #print('Fuzzy: Select row %s on Compare row %s with score of %s' %(sRow, cRow, scoreValue))
                    self.match_fuzzy.append(dataSet)

                """ Don't use this unless you want a result set equal to selection * comparison!!! """
                #if scoreValue < self.min_ratio:
                    #print('No Match: Select row %s on Compare row %s with score of %s' %(sRow, cRow, scoreValue))
                #    self.match_none.append(dataSet)

            status = round( ((sRow / selectSize) * 100), 0)
            print('Row %s of %s - Percentage complete - %s' %(sRow, selectSize, status) + '%')
        
        self.csv_writer()
        return self.match_exact, self.match_fuzzy ##, self.match_none


    def csv_writer(self):

        with open('results_exact.csv', 'w+', newline='', encoding='utf8') as csvresult:
            csvrow = []
            csvwrite = csv.writer(csvresult, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            csvwrite.writerow(self._CSV_COLUMNS)
            if len(self.match_exact) > 0:
                for i in self.match_exact:
                    sRow, sList, sCode, cRow, cList, cCode, scoreValue = i
                    csvrow = [sRow, sList, sCode, cRow, cList, cCode, scoreValue]
                    csvwrite.writerow(csvrow)

        with open('results_fuzzy.csv', 'w+', newline='', encoding='utf8') as csvresult:
            csvrow = []
            csvwrite = csv.writer(csvresult, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            csvwrite.writerow(self._CSV_COLUMNS)
            if len(self.match_fuzzy) > 0:
                for i in self.match_fuzzy:
                    sRow, sList, sCode, cRow, cList, cCode, scoreValue = i
                    csvrow = [sRow, sList, sCode, cRow, cList, cCode, scoreValue]
                    csvwrite.writerow(csvrow)


