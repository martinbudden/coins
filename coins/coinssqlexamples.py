#!/usr/bin/env python
#coding=utf-8
#file: coinssqlexamples.py

"""
Examples of SQL queries on the COINS database.
"""

import sqlite3
import locale
from optparse import OptionParser


def sqlite_examples(sqlite_filename):
    """
    Perform example Sqlite queries.

    Keyword arguments:
    verbose -- give detailed status updates.

    """
    connection = sqlite3.connect(sqlite_filename)
    cursor = connection.cursor()

    print "One row from the 'data_type' table:"
    cursor.execute('''SELECT * FROM data_type''')
    print cursor.fetchone()
    print

    print "One row from the 'account' table:"
    cursor.execute('''SELECT * FROM account''')
    print cursor.fetchone()
    print

    print "One row from the 'department' table:"
    cursor.execute('''SELECT * FROM department''')
    print cursor.fetchone()
    print

    print "One row from the 'counterparty' table:"
    cursor.execute('''SELECT * FROM counterparty''')
    print cursor.fetchone()
    print

    print "One row from the 'counterparty' table:"
    cursor.execute('''SELECT * FROM counterparty''')
    print cursor.fetchone()
    print

    print "One row from the 'programme_object' table:"
    cursor.execute('''SELECT * FROM programme_object''')
    print cursor.fetchone()
    print

    print "One row from the 'programme_object_group' table:"
    cursor.execute('''SELECT * FROM programme_object_group''')
    print cursor.fetchone()
    print

    print "One row from the 'coins' table:"
    cursor.execute('''SELECT * FROM outturn''')
    print cursor.fetchone()
    print

    print "outturn Distinct Data_types"
    cursor.execute('''SELECT DISTINCT Data_type FROM outturn''')
    for row in cursor:
        print row[0]
    print

    print "outturn Distinct Data_subtypes"
    cursor.execute('''SELECT DISTINCT Data_subtype FROM outturn''')
    for row in cursor:
        print row[0]
    print

    print "outturn count"
    cursor.execute('''SELECT COUNT(*) FROM outturn''')
    print 'COUNT:', cursor.fetchone()[0]
    print

    print "plans count"
    cursor.execute('''SELECT COUNT(*) FROM plans''')
    print 'COUNT:', cursor.fetchone()[0]
    print

    print "CHC009 DEL outturn"
    dept = 'CHC009'
    cursor.execute('''SELECT Department_code, department.description,
        Value,
        data_subtype,
        Account_code, account.description,
        Counterparty_code,
        Time, Budget_Boundary,
        Resource_Capital,
        Dept_Group,
        CGA_Body_Type,
        COFOG,
        PESA,
        Territory
        FROM outturn
        JOIN department
        ON department.code=outturn.Department_code
        JOIN account
        ON account.code=outturn.Account_code
        WHERE Data_type=:data and Department_code=:dept and Budget_Boundary=:budget and Resource_Capital="Capital"
        and (Data_subtype LIKE "%Approved%" or Data_subtype="Submitted (Outturn)")
        ORDER BY Department_code''',
        {'data': 'Outturn', 'dept': dept, 'budget': 'DEL'})
    print cursor.fetchone()
    for row in cursor:
        print row
    print

    print "CHC009 DEL outturn TOTAL"
    cursor.execute('''SELECT SUM(Value)
        FROM outturn
        WHERE Department_code=:dept and Budget_Boundary=:budget and Resource_Capital="Capital"
        and (Data_subtype LIKE "%Approved%" or Data_subtype="Submitted (Outturn)")''',
        {'dept': dept, 'budget': 'DEL'})
    print 'TOTAL:', cursor.fetchone()[0]
    print

    locale.setlocale(locale.LC_ALL, "")
    cursor.execute('''SELECT SUM(Value)
        FROM outturn
        WHERE Budget_Boundary="DEL" and Resource_Capital="Capital"
        and (Data_subtype LIKE "%Approved%" or Data_subtype="Submitted (Outturn)")''')
    print 'TOTAL DEL Capital: ', locale.format('%d', cursor.fetchone()[0], True)

    cursor.execute('''SELECT SUM(Value)
        FROM outturn
        WHERE Budget_Boundary="AME" and Resource_Capital="Capital"
        and (Data_subtype LIKE "%Approved%" or Data_subtype="Submitted (Outturn)")''')
    print 'TOTAL AME Capital: ', locale.format('%d', cursor.fetchone()[0], True)

    cursor.execute('''SELECT SUM(Value)
        FROM outturn
        WHERE Budget_Boundary="DEL" and Resource_Capital="Resource"
        and (Data_subtype LIKE "%Approved%" or Data_subtype="Submitted (Outturn)")''')
    print 'TOTAL DEL Resource:', locale.format('%d', cursor.fetchone()[0], True)

    cursor.execute('''SELECT SUM(Value)
        FROM outturn
        WHERE Budget_Boundary="AME" and Resource_Capital="Resource"
        and (Data_subtype LIKE "%Approved%" or Data_subtype="Submitted (Outturn)")''')
    print 'TOTAL AME Resource:', locale.format('%d', cursor.fetchone()[0], True)
    print

    cursor.close()
    connection.close()


def sqlite_examples2(sqlite_filename):
    """
    Perform example Sqlite queries.

    Keyword arguments:
    verbose -- give detailed status updates.

    """
    connection = sqlite3.connect(sqlite_filename)
    cursor = connection.cursor()

    print "forecasts Distinct Data_types"
    cursor.execute('''SELECT DISTINCT Data_type
        FROM forecasts''')
    for row in cursor:
        print row[0]
    print

    print "snapshots Distinct Data_types"
    cursor.execute('''SELECT DISTINCT Data_type
        FROM snapshots''')
    for row in cursor:
        print row[0]
    print

    print "forecasts count"
    cursor.execute('''SELECT COUNT(*) FROM forecasts''')
    print 'COUNT:', cursor.fetchone()[0]
    print

    print "snapshots count"
    cursor.execute('''SELECT COUNT(*) FROM snapshots''')
    print 'COUNT:', cursor.fetchone()[0]
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
        sqlite_filename = '../data/sqlite/coins_2008_09_sqlite.db'
    else:
        sqlite_filename = args[0]
    sqlite_examples(sqlite_filename)


if __name__ == "__main__":
    main()
