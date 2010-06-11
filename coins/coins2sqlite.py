#!/usr/bin/env python
#coding=utf-8
#file: coins2sqlite.py

"""
Read a COINS csv file and put it into an SQLite database.
"""

import os
import os.path
import csv
import sqlite3
import time
from optparse import OptionParser

import coinsfields


def write_description_table(connection, csv_reader, create, insert, verbose):
    """
    Read a COINS .csv data description files and write it out
    to a data description tables in the database.

    Keyword arguments:
    connection -- an SQLite connection to the database to be written.
    csv_reader -- a csv_reader over the description file.
    create -- SQL table creation string.
    insert -- SQL table insertion string.
    verbose -- give detailed status updates.

    """
    if verbose:
        print
        print create
    cursor = connection.cursor()
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
                print 'row:', row
            count += 1
            cursor.execute(insert, (row[0].decode('utf-8'), row[1].decode('utf-8')))
    except StopIteration:
        pass
    connection.commit()
    cursor.close()



def write_description_tables(connection, date, verbose):
    """
    Read COINS .csv data description files and write them out
    to the data description tables in the database. This is, in effect,
    a partial normalization of the database.

    Keyword arguments:
    connection -- an SQLite connection to the database to be written.
    date -- the date period for the data, reflected in the output filename.
    verbose -- give detailed status updates.

    """
    # Note: data_subtype, data_subtype_description- not used

    csv_reader = csv.reader(open('../data/desc/data_type_%s.csv' % date, 'r'), 'excel')
    write_description_table(connection, csv_reader,
        'create table data_type (type TEXT PRIMARY KEY, description TEXT)',
        'insert into data_type values (?,?)', verbose)

    csv_reader = csv.reader(open('../data/desc/account_%s.csv' % date, 'r'), 'excel')
    write_description_table(connection, csv_reader,
        'create table account (code TEXT PRIMARY KEY, description TEXT)',
        'insert into account values (?,?)', verbose)

    csv_reader = csv.reader(open('../data/desc/department_%s.csv' % date, 'r'), 'excel')
    write_description_table(connection, csv_reader,
        'create table department (code TEXT PRIMARY KEY, description TEXT)',
        'insert into department values (?,?)', verbose)

    csv_reader = csv.reader(open('../data/desc/counterparty_%s.csv' % date, 'r'), 'excel')
    write_description_table(connection, csv_reader,
        'create table counterparty (code TEXT PRIMARY KEY, description TEXT)',
        'insert into counterparty values (?,?)', verbose)

    csv_reader = csv.reader(open('../data/desc/programme_object_%s.csv' % date, 'r'), 'excel')
    write_description_table(connection, csv_reader,
        'create table programme_object (code TEXT PRIMARY KEY, description TEXT)',
        'insert into programme_object values (?,?)', verbose)

    csv_reader = csv.reader(open('../data/desc/programme_object_group_%s.csv' % date, 'r'), 'excel')
    write_description_table(connection, csv_reader,
        'create table programme_object_group (code TEXT PRIMARY KEY, description TEXT)',
        'insert into programme_object_group values (?,?)', verbose)


def write_coins_table(connection, csv_reader, limit, verbose):
    """
    Read COINS .csv file, write it out into an SQLite database.
    COINS data is split into separate tables according to data_type,
    this makes querying the database much quicker.

    Keyword arguments:
    connection -- an SQLite connection to the database to be written.
    csv_reader -- a csv_reader over the COINS file.
    date -- the date period for the data, reflected in the output filename.
    limit -- max number of lines of input to be read. Useful for debugging.
    verbose -- give detailed status updates.

    """
    cursor = connection.cursor()
    # read in the first row, which contains the column headings
    # eg Data_type, Data_type_description,
    csv_reader.next()

    start_time = time.time()
    reporting_interval = 50000
    row_count = 0
    # read in the data
    try:
        while True:
            row = csv_reader.next()
            row_count += 1
            t = (row[0], row[2], row[4], row[6], row[8], row[9],
                row[11], row[13], row[15], row[16], row[17], row[18], row[19],
                row[20], row[21], row[22], row[23], row[24], row[25], row[28],
                row[35], row[38], row[42], row[55], row[56], row[58],
                row[80])
            if verbose and row_count % reporting_interval == 0:
                elapsed_time = time.time() - start_time
                print('%s: %s' % (row_count, round(elapsed_time, 2)))
                #print 'row:', t
                #print
            if row[0] == 'Outturn':
                cursor.execute('insert into outturn values (%s)' % ('?,' * len(t))[:-1], t)
            elif row[0] == 'Plans':
                cursor.execute('insert into plans values (%s)' % ('?,' * len(t))[:-1], t)
                #cursor.execute('insert into plans values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', t)
            elif row[0][:8] == 'Forecast':
                cursor.execute('insert into forecasts values (%s)' % ('?,' * len(t))[:-1], t)
            elif row[0][:8] == 'Snapshot':
                cursor.execute('insert into snapshots values (%s)' % ('?,' * len(t))[:-1], t)
            else:
                print 'Error: unknown Data_type', row[0]
            if limit > 0 and row_count > limit:
                break
    except StopIteration:
        pass
    connection.commit()
    cursor.close()
    print('Row count: %s' % row_count)


def write_sqlite(sqlite_filename, input_filename, date, limit, verbose):
    """
    Read COINS .csv file, write it out into an SQLite database

    Keyword arguments:
    input_filename -- the name of the COINS input file.
    date -- the date period for the data, reflected in the output filename.
    limit -- max number of lines of input to be read. Useful for debugging.
    verbose -- give detailed status updates.

    """
    if verbose:
        print 'Reading:', input_filename
    connection = sqlite3.connect(sqlite_filename)
    write_description_tables(connection, date, False)
    cursor = connection.cursor()

    # Create coins table
    create = '''create table outturn (
        Data_type TEXT,
        Department_code TEXT,
        Account_code TEXT,
        data_subtype TEXT,
        Time TEXT,
        Counterparty_code TEXT,
        Programme_object_code TEXT,
        Programme_object_group_code TEXT,
        Accounting_Authority TEXT,
        Accounts_capital_current TEXT,
        Activity_code TEXT,
        Budget_Boundary TEXT,
        Budget_capital_current TEXT,
        Resource_Capital TEXT,
        Programme_admin TEXT,
        CGA_Body_Type TEXT,
        COFOG TEXT,
        Dept_Group TEXT,
        Estimate_line TEXT,
        ESA TEXT,
        Estimate_number TEXT,
        NAC TEXT,
        PESA TEXT,
        SBI TEXT,
        Sector TEXT,
        Territory TEXT,
        Value INT
        )'''

    # Create outturn table
    cursor.execute(create)

    # Create plans table
    create = create.replace('create table outturn', 'create table plans')
    cursor.execute(create)

    # Create forecasts table
    create = create.replace('create table plans', 'create table forecasts')
    cursor.execute(create)

    # Create snapshots table
    create = create.replace('create table forecasts', 'create table snapshots')
    cursor.execute(create)

    connection.commit()
    cursor.close()

    csv_reader = csv.reader(open(input_filename, "rb"), 'excel', delimiter='@')
    write_coins_table(connection, csv_reader, limit, verbose)


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
    Read in the COINS csv file, write out the records in a SQLite database.

    """
    (options, args) = process_options()
    if len(args) == 0:
        #input_filename = '../data/facts_2009_10_nz_1000.csv'
        #input_filename = '../data/facts_2009_10_nz.csv'
        input_filename = '../data/facts_2008_09_nz.csv'
    else:
        input_filename = args[0]
    limit = 0
    options.verbose = True

    if not os.path.isdir('../data/sqlite'):
        os.makedirs('../data/sqlite')
    date = '2008_09'
    input_filename = '../data/facts_%s_nz.csv' % date
    sqlite_filename = '../data/sqlite/coins_%s_sqlite.db' % date
    if os.path.isfile(sqlite_filename):
        os.remove(sqlite_filename)
    write_sqlite(sqlite_filename, input_filename, date, limit, options.verbose)


if __name__ == "__main__":
    main()
