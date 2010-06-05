#!/usr/bin/env python
#coding=utf-8
#file: readcoinscsv.py

"""
Read a COINS .csv file
"""

import csv
from jinja2 import Template
#from collections import defaultdict
from optparse import OptionParser


def read_coins_csv(filename):
    """
    Read COINS .csv file

    Keyword arguments:
    filename -- the file to be read

    Format of file is:
    First row - each cell is a column heading
        Data_type@  Data_type_description@Department_code@Department_description@Account_code@Account_description@data_subtype@data_subtype_description@Time@Counterparty_code@Couterparty_description@Programme_object_code@Programme_object_description@
    Main table - from B1 - COINS data, delimited by @
        Snapshot30@ PLANS FEB08@SCT075@Scottish Government@41321100@Interest receivable - Student Loans@Plans New Budget Regime Draft Adjustments@@2009-10@CPID.NA@@Segment.NA@@Segment Root Member@@@A-DUM@@@B-CON@Resource@@Dept@@Dept075@@@@ESA-D41A@E-OAA@@@Interest/dividends@@@@@@S1001@@@@@@@@@@@@@@@@@@@Negative@@@@@@@@@@@@@@@@@@@@@@@0

    Interesting COINS fields:
        0  - Data_type
        1  - Data_type_description
        2  - Department_code
        3  - Department_description
        4  - Account_code
        5  - Account_description
        6  - data_subtype
        7  - data_subtype_description
        8  - Time
        9  - Counterparty_code
        10 - Couterparty_description
        11 - Programme_object_code
        12 - Programme_object_description
        13 - Programme_object_group_code
        14 - Programme_object_group_description
        20 - Resource_Capital
        22 - CGA_Body_Type
        24  -Dept_Group
        56 - Sector
        80 - Value
    interesting_fields = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,20,22,24,56,80]

    """
    data_type = {}
    department = {}
    account = {}
    data_subtype = {}
    Counterparty_code = {}
    reader = csv.reader(open(filename, "rb"), 'excel', delimiter='@')


    # read in the first row, which contains the column headings
    # eg Data_type, Data_type_description,
    # Department_code, Department_description,
    # Account_code, Account_description...
    row = reader.next()
    #for i in range(1, len(row) - 1):
    #    data.append({'marker': row[i], 'alleles': {}})

    # read in the data
    try:
        while 1:
            row = reader.next()
            data_type[row[0]] = row[1]
            department[row[2]] = row[3]
            account[row[4]] = row[5]
            data_subtype[row[6]] = row[7]
            Counterparty_code[row[8]] = row[9]
            #print "aa",row[2],row[3]
    except StopIteration:
        pass
    return data_type, department, account, data_subtype, Counterparty_code


def print_dict(data):
    """
    Format Department code and description into an HTML table

    """
    for i in data:
        print i, data[i]
    return


def department_table_html(data, caption, rowheaders, colheaders):
    """
    Format Department code and description into an HTML table

    Keyword arguments:
    data -- a 2D dict of the data to be formatted
    caption -- the table's caption
    colheaders -- the table's column headings

    """
    template = Template('<html>\n<table>\n'
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
                '<td>{{"%s"|format(data[colheader][rowheader])|escape}}</td> '
            '{% endfor %}'
            '</tr>\n'
        '{% endfor %}'
        '</tbody>\n'
        '</table>\n</html>\n')
    return template.render(data=data, caption=caption,
        rowheaders=rowheaders, colheaders=colheaders)


def process_options(arglist=None):
    """
    Process options passed either via arglist or via command line args.

    """

    parser = OptionParser(arglist)
    #parser.add_option("-f","--file",dest="filename",
    #                  help="file to be converted",metavar="FILE")
    #parser.add_option("-d","--date",dest="date",
    #                  help="published DATE",metavar="DATE")
    parser.add_option("-v", action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")

    (options, args) = parser.parse_args()
    return options, args


def main():
    """
    Read in the COINS csv file
    Print out html tables
    department code and description

    """

    (options, args) = process_options()
    if len(args) == 0:
        input_filename = '../data/clean2000.csv'
    else:
        input_filename = args[0]
    #output_filename = 'fact_2009_10_2000.csv'
    # read in the COINS data
    (data_type, department, account, data_subtype, Counterparty_code) = read_coins_csv(input_filename)
    print "\ndata type"
    print_dict(data_type)
    print "\ndepartment"
    print_dict(department)
    print "\naccount"
    print_dict(account)
    print "\ndata subtype"
    print_dict(data_subtype)
    print "\n counterparty code"
    print_dict(Counterparty_code)


if __name__ == "__main__":
    main()
