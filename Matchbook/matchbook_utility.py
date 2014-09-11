#matchbook_test.py
import matchbook_reader as r, matchbook_data as d, matchbook as m
#import multiprocessing as mp
import time


def main():
    startTime = time.localtime()
    print('Started - ' + time.strftime("%Y-%m-%dT%H:%M:%S", startTime))

    S = r.FileProcessor('test/select_test.csv')
    C = r.FileProcessor('test/compare_test.csv')
    F = m.Process(S.data_set, C.data_set, 100).fuzzyMatcher()

    #W = m.Process.csv_writer(F)

    endTime = time.localtime()
    print('Finished - ' + time.strftime("%Y-%m-%dT%H:%M:%S", endTime))
    print('Processed - %i records' %( ( len(S.data_set) * len(C.data_set) ) ))


if __name__ == '__main__':
    main()
