#!/usr/bin/env python
#coding=utf-8
#file: coins2sqlite.py

"""
Read a COINS csv file and put it into an Sqlite database.
"""

import os
import os.path
import csv
import sqlite3
import time
from optparse import OptionParser

import coinsfields

# filename reflects date, department, non-zero values (nz), and field subset (fs)
SQLITE_FILENAME_TEMPLATE = '../data/sqlite/coins_%(date)s_sqlite.db'


def write_description_table(connection, cursor, csv_reader, create, insert, verbose):
    if verbose:
        print
        print create
    cursor.execute(create)
    # read in the first row, which contains the column headings
    csv_reader.next()
    # read in the data
    reporting_interval = 50
    count = 0
    try:
        while True:
            row = csv_reader.next()
            if verbose and count % reporting_interval == 0:
                print 'row:', tuple(row)
            count += 1
            cursor.execute(insert, (row[0].decode('utf-8'), row[1].decode('utf-8')))
            connection.commit()
    except StopIteration:
        pass



def write_description_tables(connection, verbose):
    cursor = connection.cursor()

    csv_reader = csv.reader(open('../data/desc/data_type.csv', 'r'), 'excel')
    write_description_table(connection, cursor, csv_reader,
        'create table data_type (type, description)',
        'insert into data_type values (?,?)', verbose)

    csv_reader = csv.reader(open('../data/desc/account.csv', 'r'), 'excel')
    write_description_table(connection, cursor, csv_reader,
        'create table account (type, description)',
        'insert into account values (?,?)', verbose)

    csv_reader = csv.reader(open('../data/desc/department.csv', 'r'), 'excel')
    write_description_table(connection, cursor, csv_reader,
        'create table department (type, description)',
        'insert into department values (?,?)', verbose)

    csv_reader = csv.reader(open('../data/desc/counterparty.csv', 'r'), 'excel')
    write_description_table(connection, cursor, csv_reader,
        'create table counterparty (type, description)',
        'insert into counterparty values (?,?)', verbose)

    csv_reader = csv.reader(open('../data/desc/programme_object.csv', 'r'), 'excel')
    write_description_table(connection, cursor, csv_reader,
        'create table programme_object (type, description)',
        'insert into programme_object values (?,?)', verbose)

    csv_reader = csv.reader(open('../data/desc/programme_object_group.csv', 'r'), 'excel')
    write_description_table(connection, cursor, csv_reader,
        'create table programme_object_group (type, description)',
        'insert into programme_object_group values (?,?)', verbose)

    cursor.close()

    #cursor.execute('''create table data_subtype (data_subtype, data_subtype_description)''') - not used


def write_sqlite(input_filename, date, limit, verbose):
    """
    Read COINS .csv file

    Keyword arguments:
    input_filename -- the name of the COINS input file
    date -- the date period for the data, reflected in the output filename
    limit -- max number of lines of input to be read. Useful for debugging.
    verbose -- give detailed status updates.

    """
    csv_reader = csv.reader(open(input_filename, "rb"), 'excel', delimiter='@')
    if not os.path.isdir('../data/sqlite'):
        os.makedirs('../data/sqlite')
    sqlite_filename = SQLITE_FILENAME_TEMPLATE % {'date':date}
    if os.path.isfile(sqlite_filename):
        os.remove(sqlite_filename)

    connection = sqlite3.connect(sqlite_filename)
    write_description_tables(connection, verbose)

    cursor = connection.cursor()

    # read in the first row, which contains the column headings
    # eg Data_type, Data_type_description,
    csv_reader.next()
    # Create table

    cursor.execute('''create table coins (
        Data_type,
        Department_code,
        Account_code,
        data_subtype,
        Time,
        Counterparty_code,
        Programme_object_code,
        Programme_object_group_code,
        Accounting_Authority,
        Accounts_capital_current,
        Activity_code,
        Budget_Boundary,
        Budget_capital_current,
        Resource_Capital,
        Programme_admin,
        CGA_Body_Type,
        COFOG,
        Dept_Group,
        Estimate_line,
        ESA,
        Estimate_number,
        NAC,
        PESA,
        SBI,
        Sector,
        Territory,
        Value
        )''')
    start_time = time.time()
    reporting_interval = 50000
    row_count = 0
    # read in the data
    try:
        while True:
            row = csv_reader.next()
            t = (row[0], row[2], row[4], row[6], row[8], row[9],
                row[11], row[13], row[15], row[16], row[17], row[18], row[19],
                row[20], row[21], row[22], row[23], row[24], row[25], row[28],
                row[35], row[38], row[42], row[55], row[56], row[58],
                row[80])
            if verbose and row_count % reporting_interval == 0:
                elapsed_time = time.time() - start_time
                print('%s: %s' % (row_count, elapsed_time))
                print 'row tuple', t
                print
            row_count += 1
            cursor.execute('insert into coins values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', t)
            if limit > 0 and row_count > limit:
                break
    except StopIteration:
        pass
    connection.commit()
    cursor.close()
    print('Row count: %s' % row_count)


def process_options(arglist=None):
    """
    Process options passed either via arglist or via command line args.

    """
    parser = OptionParser(arglist)
    #parser.add_option("-f", "--file", dest="filename",
    #                  help="file to be converted", metavar="FILE")
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
        #input_filename = '../data/facts_2009_10_nz_1000.csv'
        input_filename = '../data/facts_2009_10_nz.csv'
    else:
        input_filename = args[0]
    limit = 0
    date = '2009_10'
    options.verbose = True
    write_sqlite(input_filename, date, limit, options.verbose)


if __name__ == "__main__":
    main()
