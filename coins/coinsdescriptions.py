#!/usr/bin/env python
#coding=utf-8
#file: coinsdescriptions.py

"""
Read a COINS .csv and output the codes and their descriptions to .csv files.
eg department_code and department_description are placed in data/desc/departments.csv
"""

import os
import csv
import time
from optparse import OptionParser

import coinsfields

def read_coins_csv(filename, date, verbose):
    """
    Read COINS .csv file

    Keyword arguments:
    filename -- the file to be read

    Format of file is:
    First row - each cell is a column heading
        Data_type@Data_type_description@Department_code@Department_description@Account_code@Account_description@data_subtype@data_subtype_description@Time@Counterparty_code@Couterparty_description@Programme_object_code@Programme_object_description@
    Main table - from B1 - COINS data, delimited by @
        Snapshot30@ PLANS FEB08@SCT075@Scottish Government@41321100@Interest receivable - Student Loans@Plans New Budget Regime Draft Adjustments@@2009-10@CPID.NA@@Segment.NA@@Segment Root Member@@@A-DUM@@@B-CON@Resource@@Dept@@Dept075@@@@ESA-D41A@E-OAA@@@Interest/dividends@@@@@@S1001@@@@@@@@@@@@@@@@@@@Negative@@@@@@@@@@@@@@@@@@@@@@@0

    """
    data_type = {}
    department = {}
    account = {}
    data_subtype = {}
    counterparty = {}
    programme_object = {}
    programme_object_group = {}
    if verbose:
        print 'Reading:', filename
    reader = csv.reader(open(filename, "rb"), 'excel', delimiter='@')

    # read in the first row, which contains the column headings
    # eg Data_type, Data_type_description,
    # Department_code, Department_description,
    # Account_code, Account_description...
    column_headings = reader.next()

    start_time = time.time()
    reporting_interval = 50000
    row_count = 0
    try:
        while True:
            row_count += 1
            if verbose and row_count % reporting_interval == 0:
                elapsed_time = time.time() - start_time
                print('%s: %s' % (row_count, round(elapsed_time, 2)))
            row = reader.next()
            data_type[row[coinsfields.DATA_TYPE]] = row[coinsfields.DATA_TYPE_DESCRIPTION]
            department[row[coinsfields.DEPARTMENT_CODE]] = row[coinsfields.DEPARTMENT_DESCRIPTION]
            account[row[coinsfields.ACCOUNT_CODE]] = row[coinsfields.ACCOUNT_DESCRIPTION]
            data_subtype[row[coinsfields.DATA_SUBTYPE]] = row[coinsfields.DATA_SUBTYPE_DESCRIPTION]
            counterparty[row[coinsfields.COUNTERPARTY_CODE]] = row[coinsfields.COUTERPARTY_DESCRIPTION]
            programme_object[row[coinsfields.PROGRAMME_OBJECT_CODE]] = row[coinsfields.PROGRAMME_OBJECT_DESCRIPTION]
            programme_object_group[row[coinsfields.PROGRAMME_OBJECT_GROUP_CODE]] = row[coinsfields.PROGRAMME_OBJECT_GROUP_DESCRIPTION]
    except StopIteration:
        pass

    print "data type"
    write_data_csv('../data/desc/data_type_%s.csv' % date, data_type,
        column_headings[coinsfields.DATA_TYPE], column_headings[coinsfields.DATA_TYPE_DESCRIPTION])

    print "department"
    write_data_csv('../data/desc/department_%s.csv' % date, department,
        column_headings[coinsfields.DEPARTMENT_CODE], column_headings[coinsfields.DEPARTMENT_DESCRIPTION])

    print "account"
    write_data_csv('../data/desc/account_%s.csv' % date, account,
        column_headings[coinsfields.ACCOUNT_CODE], column_headings[coinsfields.ACCOUNT_DESCRIPTION])

    print "data subtype"
    write_data_csv('../data/desc/data_subtype_%s.csv' % date, data_subtype,
        column_headings[coinsfields.DATA_SUBTYPE],
        column_headings[coinsfields.DATA_SUBTYPE_DESCRIPTION])

    print "counterparty"
    write_data_csv('../data/desc/counterparty_%s.csv' % date, counterparty,
        column_headings[coinsfields.COUNTERPARTY_CODE],
        column_headings[coinsfields.COUTERPARTY_DESCRIPTION])

    print "program_object"
    write_data_csv('../data/desc/programme_object_%s.csv' % date, programme_object,
        column_headings[coinsfields.PROGRAMME_OBJECT_CODE],
        column_headings[coinsfields.PROGRAMME_OBJECT_DESCRIPTION])

    print "programme_object_group"
    write_data_csv('../data/desc/programme_object_group_%s.csv' % date, programme_object_group,
        column_headings[coinsfields.PROGRAMME_OBJECT_GROUP_CODE],
        column_headings[coinsfields.PROGRAMME_OBJECT_GROUP_DESCRIPTION])
    print


def write_data_csv(filename, data, field_name, field_description):
    """
    Write data out as a .csv file.

    """
    csv_writer = csv.writer(open(filename, 'w'))
    csv_writer.writerow([field_name, field_description])
    for i in sorted(data.keys()):
        csv_writer.writerow([i, data[i]])
    return


def process_options(arglist=None):
    """
    Process options passed either via arglist or via command line args.

    """
    parser = OptionParser(arglist)
    #parser.add_option("-f", "--file", dest="filename",
    #                  help="file to be converted", metavar="FILE")
    #parser.add_option("-d", "--date", dest="date",
    #                  help="published DATE", metavar="DATE")
    parser.add_option("-v", action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")

    (options, args) = parser.parse_args()
    return options, args


def main():
    """
    Read in the COINS csv file.
    Write out code and description .csv files.

    """
    (options, args) = process_options()
    if len(args) == 0:
        input_filename = '../data/facts_2008_09_nz.csv'
    else:
        input_filename = args[0]

    if not os.path.isdir('../data/desc'):
        os.makedirs('../data/desc')
    options.verbose = True
    read_coins_csv(input_filename, '2008_09', options.verbose)
    input_filename = '../data/facts_2009_10_nz.csv'
    read_coins_csv(input_filename, '2009_10', options.verbose)


if __name__ == "__main__":
    main()
