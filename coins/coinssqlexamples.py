#!/usr/bin/env python
#coding=utf-8
#file: coinssqlexamples.py

"""
Examples of SQL queries on the COINS database.
"""

import sqlite3
from optparse import OptionParser


def sqlite_examples(sqlite_filename, verbose):
    """
    Perform example Sqlite queries.

    Keyword arguments:
    verbose -- give detailed status updates.

    """
    connection = sqlite3.connect(sqlite_filename)
    cursor = connection.cursor()

    print "One row from the 'data_type' table:"
    cursor.execute('''select * from data_type''')
    print cursor.fetchone()
    print

    print "One row from the 'account' table:"
    cursor.execute('''select * from account''')
    print cursor.fetchone()
    print

    print "One row from the 'department' table:"
    cursor.execute('''select * from department''')
    print cursor.fetchone()
    print

    print "One row from the 'counterparty' table:"
    cursor.execute('''select * from counterparty''')
    print cursor.fetchone()
    print

    print "One row from the 'counterparty' table:"
    cursor.execute('''select * from counterparty''')
    print cursor.fetchone()
    print

    print "One row from the 'programme_object' table:"
    cursor.execute('''select * from programme_object''')
    print cursor.fetchone()
    print

    print "One row from the 'programme_object_group' table:"
    cursor.execute('''select * from programme_object_group''')
    print cursor.fetchone()
    print

    print "One row from the 'coins' table:"
    cursor.execute('''select * from coins''')
    print cursor.fetchone()
    print

    dept = 'DIS063'
    cursor.execute('''select Value, Dept_Group from coins 
        where Data_type=:data and Department_code=:dept and Budget_Boundary=:budget''',
        {'data': 'Outturn', 'dept': dept, 'budget': 'DEL'})
    for row in cursor:
        print row
    print


    cursor.close()
    connection.close()


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
    Perform example queries on the COINS Sqlite database.

    """
    (options, args) = process_options()
    if len(args) == 0:
        sqlite_filename = '../data/sqlite/coins_2009_10_sqlite.db'
    else:
        sqlite_filename = args[0]
    options.verbose = True
    sqlite_examples(sqlite_filename, options.verbose)


if __name__ == "__main__":
    main()
