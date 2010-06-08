#!/usr/bin/env python
#coding=utf-8
#file: coinsdeptartments.py

"""
Extract the departmental data from a COINS csv file
"""

import csv
import time
from optparse import OptionParser

import coinsfields

# filename reflects date, department, non-zero values (nz), and field subset (fs)
DEPT_FILENAME_TEMPLATE = '../data/depts/coins_%(date)s_%(dept_code)s_nz_fs.csv'

def write_dept_csv(input_filename, date, dept_code, limit, verbose):
    """
    Read COINS .csv file

    Keyword arguments:
    input_filename -- the name of the COINS input file
    date -- the date period for the data, reflected in the output filename
    department_code -- code for department to be extracted.
    limit -- max number of lines of input to be read. Useful for debugging.
    verbose -- give detailed status updates.

    """
    csv_reader = csv.reader(open(input_filename, "rb"), 'excel', delimiter='@')
    output_filename = DEPT_FILENAME_TEMPLATE % {'date':date, 'dept_code':dept_code}
    csv_writer = csv.writer(open(output_filename, 'w'))
 
    # read in the first row, which contains the column headings
    # eg Data_type, Data_type_description,
    column_headings = csv_reader.next()
    csv_writer.writerow(column_headings.encode('utf-8'))

    start_time = time.time()
    reporting_interval = 50000
    row_count = 0
    dept_count = 0
    # read in the data
    try:
        while 1:
            row = csv_reader.next()
            row_count += 1
            if verbose and row_count % reporting_interval == 0:
                elapsed_time = time.time() - start_time
                print('%s: %s' % (row_count, elapsed_time))
            if row[coinsfields.DEPARTMENT_CODE] == dept_code:
                dept_count += 1
                csv_writer.writerow(row)
            if limit > 0 and dept_count > limit:
                break
    except StopIteration:
        pass
    print('Total row count: %s' % row_count)
    print('Deptartment row count: %s' % dept_count)


def write_all_depts_csv(input_filename, date, limit, verbose):
    """
    Read a COINS .csv file.
    Write out the data for each department in a separate file.

    Keyword arguments:
    input_filename -- the name of the COINS input file
    date -- the date period for the data, reflected in the output filename
    limit -- max number of lines of input to be read. Useful for debugging.
    verbose -- give detailed status updates.

    """

    dept_csv_writers = {}
    depts_reader = csv.reader(open('../data/desc/department.csv', 'r'))
    # skip the column headings
    row = depts_reader.next()
    try:
        while 1:
            # create a csv writer for each department
            row = depts_reader.next()
            dept = row[0]
            dept_code = dept.replace('/',' ')
            output_filename = DEPT_FILENAME_TEMPLATE % {'date':date, 'dept_code':dept_code}
            csv_writer = csv.writer(open(output_filename, 'w'))
            dept_csv_writers[dept] = csv_writer
    except StopIteration:
        pass

    csv_reader = csv.reader(open(input_filename, "rb"), 'excel', delimiter='@')
    column_headings = csv_reader.next()
    for i in dept_csv_writers:
        dept_csv_writers[i].writerow(column_headings)

    start_time = time.time()
    reporting_interval = 50000
    row_count = 0
    counts = {}
    for i in dept_csv_writers:
        counts[i] = 0
    # read in the data
    try:
        while 1:
            row = csv_reader.next()
            row_count += 1
            if verbose and row_count % reporting_interval == 0:
                elapsed_time = time.time() - start_time
                print('%s: %s' % (row_count, elapsed_time))
            dept = row[coinsfields.DEPARTMENT_CODE]
            dept_csv_writers[dept].writerow(row)
            counts[dept] += 1
            if limit > 0 and row_count > limit:
                break
    except StopIteration:
        pass
    print('Total row count: %s' % row_count)
    for i in sorted(dept_csv_writers):
        print('%(dept)s row count: %(count)s' % {'dept':i, 'count':counts[i]})



def process_options(arglist=None):
    """
    Process options passed either via arglist or via command line args.

    """

    parser = OptionParser(arglist)
    #parser.add_option("-f", "--file", dest="filename",
    #                  help="file to be converted", metavar="FILE")
    parser.add_option("-c", "--code", dest="dept_code",
                      help="department code", metavar="DEPT_CODE")
    parser.add_option("-v", action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")

    (options, args) = parser.parse_args()
    return options, args


def main():
    """
    Read in the COINS csv file, write out the records for a single department

    """

    (options, args) = process_options()
    if len(args) == 0:
        input_filename = '../data/facts_2009_10_nz_fs_1000.csv'
    else:
        input_filename = args[0]
    limit = 0
    date = '2009_10'
    options.verbose = True
    if options.dept_code == None:
        write_all_depts_csv(input_filename, date, limit, options.verbose)
    else:
        write_dept_csv(input_filename, date, options.dept_code, limit, options.verbose)


if __name__ == "__main__":
    main()
