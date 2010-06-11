#!/usr/bin/env python
#coding=utf-8
#file: coinssqlpesa.py

"""
Examples of SQL queries on the COINS database.
"""

import csv
import sqlite3
import locale
from jinja2 import Template
from collections import defaultdict
from optparse import OptionParser

# Taken from: "Public Expenditure Statistical Analysis 2009, Appendix B: Departmental Groups"
DEPARTMENTAL_GROUPS_2008_09 = [
    ('Children, Schools and Families', ('DES022', 'OIS022')),
    ('Health', ('DOH033', 'DPM085')),
    ('Transport', ('DFT004', 'ORR088')),
    ('Innovation, Universities and Skills', ('DIS063',)),
    ('CLG Communities and Local Government', ('DPM085',)),
    ('Home Office', ('HOF034',)), # missing 'Assets Recovery Agency'
    ('Justice', ('LCD047', 'PRO067', 'ELC011', 'NIC081', 'LRG045', 'SCO042', 'WOF091', 'TSC068')),
    ('Law Officers Departments', ('CPS016', 'SFO019', 'HGT089', 'RCP046')),
    ('Defence', ('MOD017',)),
    ('Foreign and Commonwealth Office', ('FCO027',)),
    ('International Development', ('DID030',)),
    ('Energy and Climate Change', ('DEC066', 'OGE020')),
    ('Business, Enterprise and Regularity Reform', ('BTI013', 'OFT074', 'PSC006', 'ECG025')), # missing 'Department for Business, Enterprise and Regulartory Reform', 'Office of Communications'
    ('Environment, Food and Rural Affairs', ('EFR003', 'OWS057')), # missing 'Forrestry Commision'
    ('Culture, Media and Sport', ('DCM048',)),
    ('Work and Pensions', ('DWP032', 'GEO064')),
    ('Scotland', ('SCT075',)), # used Scottish Government
    ('Wales', ('WAG090',)),
    ('Northern Ireland Executive', ('NIE099',)),
    ('Northern Ireland Office', ('NIO097',)),
    ('Chancellors Departments', ('HMT087', 'DNS049', 'GAD031', 'ILR041', 'CES014')), # missing 'National Investment and Loans Office', 'Royal Mint', and 'Office of Government Commerce'
    ('Cabinet Office', ('CAB010', 'COI010', 'CHC009', 'NSG062')), #missing 'Security and Intelligence Agencies'
    ('Independent Bodies', ('HOC036', 'HOL037', 'NAO050', 'ONS005', 'OPC060')) #used 'Office for National Statistics' instead of 'Statistics Board'
    ]


def table_html(data, caption, rowheaders, colheaders):
    """
    Format data into an HTML table

    Keyword arguments:
    data -- a 2D dict of the data to be formatted
    caption -- the table's caption
    rowheaders -- the table's row headings
    colheaders -- the table's column headings

    """
    template = Template('<table>\n'
        '<caption>{{caption}}</caption>\n'
        '<thead>\n'
        '<tr> '
        '<th></th> '
        '{% for colheader in colheaders %}'
            '<th>{{colheader|replace(" ", "<br />")}}</th> '
        '{% endfor %}'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '{% for rowheader in rowheaders %}'
            '<tr> '
            '<th>{{rowheader}}</th> '
            '{% for colheader in colheaders %}'
                '<td>{{data[colheader][rowheader]|escape}}</td> '
            '{% endfor %}'
            '</tr>\n'
        '{% endfor %}'
        '</tbody>\n'
        '</table>\n')
    return template.render(data=data, caption=caption, rowheaders=rowheaders, colheaders=colheaders)



def sqlite_totals(sqlite_filename):
    """
    Perform SQL queries to calucate various Resource, Capital, DEL and AME
    spending totals.

    Keyword arguments:
    sqlite_filename -- name of SQLite database file to be queried.

    """
    connection = sqlite3.connect(sqlite_filename)
    cursor = connection.cursor()

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


def sqlite_department_totals(sqlite_filename, date):
    """
    Perform SQL queries to calucate Capital DEL department
    spending totals.

    Keyword arguments:
    sqlite_filename -- name of SQLite database file to be queried.
    date -- reporting period (eg 2008_09)

    """
    connection = sqlite3.connect(sqlite_filename)
    cursor = connection.cursor()

    locale.setlocale(locale.LC_ALL, "")
    budget = 'DEL'
    rc = 'Capital'
    
    depts = []
    csv_reader = csv.reader(open('../data/desc/department_%s.csv' % date, 'r'))
    # skip the column headings
    row = csv_reader.next()
    try:
        while True:
            row = csv_reader.next()
            depts.append({'code': row[0], 'desc': row[1]})
    except StopIteration:
        pass

    for i in depts:
        dept = i['code']
        desc = i['desc']
        cursor.execute('''SELECT SUM(Value)
            FROM outturn
            WHERE Budget_Boundary=:budget and Resource_Capital=:rc
            and Department_code=:dept
            and (Data_subtype LIKE "%Approved%" or Data_subtype="Submitted (Outturn)")''',
            {'dept': dept, 'budget': budget, 'rc': rc})
        total = cursor.fetchone()[0]
        if total:
            print 'Dept %(dept)s (%(desc)s) %(budget)s %(rc)s: ' % {'dept': dept, 'desc': desc, 'budget': budget, 'rc': rc},
            print locale.format('%d', total, True)

    cursor.close()
    connection.close()


def sqlite_departmental_group_totals(sqlite_filename, groups, resource_capital, budget_boundary, verbose):
    """
    Perform SQL queries to calucate department group spending totals.

    Keyword arguments:
    sqlite_filename -- name of SQLite database file to be queried.
    groups -- list of departmental groups
    resource_capital -- 'Resource' or 'Capital' for resource or capital spending
    budget_boundary -- 'DEL' or 'AME' for DEL or AME spending
    verbose -- give detailed status updates.

    """
    connection = sqlite3.connect(sqlite_filename)
    cursor = connection.cursor()

    table = defaultdict(dict)
    row_headers = []
    column_headers = []
    col = 'COINS 2008-09 outturn'
    column_headers.append(col)
    col2009 = 'PESA 2009 estimate'
    col2010 = 'PESA 2010 outturn'
    column_headers.append(col2009)
    column_headers.append(col2010)
    
    locale.setlocale(locale.LC_ALL, "")
    
    total = 0
    caption = '%s %s by departmental group (millions)' % (resource_capital, budget_boundary)
    if verbose:
        print caption
    for i in groups:
        group = i[0]
        depts = i[1]
        cursor.execute('''SELECT SUM(Value)
            FROM outturn
            WHERE Budget_Boundary=? and Resource_Capital=?
            and Department_code IN (%s)
            and (Data_subtype LIKE "%%Approved%%" or Data_subtype="Submitted (Outturn)")
            ''' % ('?,' * len(depts))[:-1],
            (budget_boundary, resource_capital) + depts)
        subtotal = cursor.fetchone()[0]
        if not subtotal:
            subtotal = 0
        table[col][group] = locale.format('%d', round(subtotal/1000), True)
        table[col2009][group] = 0
        table[col2010][group] = 0
        row_headers.append(group)
        if verbose:
            print '%(group)s: ' % {'group': group}, locale.format('%d', round(subtotal/1000), True)
        total += subtotal
    if verbose:
        print 'Total', resource_capital, budget_boundary, locale.format('%d', round(total/1000), True)
        print
    html = table_html(table, caption, row_headers, column_headers)
    print html

    cursor.close()
    connection.close()
    return table


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
    print '<html>'    
    sqlite_departmental_group_totals(sqlite_filename, DEPARTMENTAL_GROUPS_2008_09, 'Resource', 'DEL', options.verbose)
    #sqlite_departmental_group_totals(sqlite_filename, DEPARTMENTAL_GROUPS_2008_09, 'Resource', 'AME', options.verbose)
    #sqlite_departmental_group_totals(sqlite_filename, DEPARTMENTAL_GROUPS_2008_09, 'Capital', 'DEL', options.verbose)
    #sqlite_departmental_group_totals(sqlite_filename, DEPARTMENTAL_GROUPS_2008_09, 'Capital', 'AME', options.verbose)
    print '</html>'


if __name__ == "__main__":
    main()
