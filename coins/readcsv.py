#!/usr/bin/env python
#coding=utf-8
#file: readcsv.py

"""
readcsv
"""

import csv
#from jinja2 import Template
from collections import defaultdict
from optparse import OptionParser


def read_csv(filename):
    """
    Read genetic marker allele frequency data from a .csv file

    Keyword arguments:
    filename -- the file to be read
    normalizer -- used to normalize the data, use 100 if the data are percentages, 1 if they are
    fractions in the range [0.0, 1.0]

    Format of file is:
    First row - each cell is a column heading
        Data_type@  Data_type_description@Department_code@Department_description@Account_code@Account_description@data_subtype@data_subtype_description@Time@Counterparty_code@Couterparty_description@Programme_object_code@Programme_object_description@
    Main table - from B1 - COINS data, delimited by @
        Snapshot30@ PLANS FEB08@SCT075@Scottish Government@41321100@Interest receivable - Student Loans@Plans New Budget Regime Draft Adjustments@@2009-10@CPID.NA@@Segment.NA@@Segment Root Member@@@A-DUM@@@B-CON@Resource@@Dept@@Dept075@@@@ESA-D41A@E-OAA@@@Interest/dividends@@@@@@S1001@@@@@@@@@@@@@@@@@@@Negative@@@@@@@@@@@@@@@@@@@@@@@0

    Interesting COINS fields:
        Data_type
        Data_type_description
        Department_code
        Department_description
        Account_code
        Account_description
        data_subtype
        data_subtype_description
        Time
        Programme_object_code
        Programme_object_description
        Programme_object_group_code
        Programme_object_group_description
        Resource_Capital
        Sector
        Value

    """
    data_type = {}
    department = {}
    account = {}
    data_subtype = {}
    Counterparty_code = {}
    reader = csv.reader(open(filename, "rb"), 'excel', delimiter='@')


    # read in the first row, which contains the column headings
    # eg Data_type, Data_type_description, Department_code, Department_description,
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

def department_table_html(data): #, caption, rowheaders, colheaders):
    """
    Format Department code and description into an HTML table

    Keyword arguments:
    data -- a 2D dict of the data to be formatted
    caption -- the table's caption
    colheaders -- the table's column headings

    """
    print "aaaaa"
    print len(data)
    for i in data:
        print i, data[i]
    return
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
                '<td>{{"%1.2e"|format(data[colheader][rowheader])|escape}}</td> '
            '{% endfor %}'
            '</tr>\n'
        '{% endfor %}'
        '</tbody>\n'
        '</table>\n</html>\n')
    return template.render(data=data, caption=caption, rowheaders=rowheaders, colheaders=colheaders)


def main():
    """
    Read in the COINS csv file
    Print out html tables
    department code and description

    """

    parser = OptionParser()
    parser.add_option("-v", action="store_true", dest="verbose", default=False, help="print status messages to stdout")
    (options, args) = parser.parse_args()

    # read in the COINS data
    (data_type, department, account, data_subtype, Counterparty_code) = read_csv("../data/clean2000.csv")
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
