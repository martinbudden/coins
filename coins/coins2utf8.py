#!/usr/bin/env python
#coding=utf-8
#file: coins2utf8.py

"""
Converts COINS text files from UTF-16 to UTF-8
"""

from optparse import OptionParser
import codecs
import time


def convert_to_utf8(output_filename, input_filename, limit, verbose):
    """
    Convert file from utf16 to utf8.

    Keyword arguments:
    output_filenname -- the name of the converted file
    input_filenname -- the name of file to be converted

    """
    input_file = codecs.open(input_filename, 'r', 'utf_16_le', 'ignore')
    output_file = codecs.open(output_filename, 'w', 'utf_8', 'ignore')
    start_time = time.time()
    reporting_interval = 100
    count = 0
    interesting_fields = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,20,22,24,56,80]

    # read in the column headers
    line = input_file.next()
    line = line.replace(u'NULL','').strip()
    fields = line.split('@')
    out_line = line
    output_file.write("%s\n" % out_line)
    for i in interesting_fields:
        print fields[i],
    print
    #for i in range(1, len(row) - 1):
    #    data.append({'marker': row[i], 'alleles': {}})

    # read in the data
    try:
        while 1:
            line = input_file.next()
            line = line.replace(u'NULL','').strip()
            fields = line.split('@')
            if fields[80] != '0':
                out_line = line
                output_file.write("%s\n" % out_line)
                count += 1
                if verbose and count % reporting_interval == 0:
                    elapsed_time = time.time() - start_time
                    print('%s: %s' % (count, elapsed_time))
                if count > limit and limit > 0:
                    break
    except StopIteration:
        pass

    elapsed_time = time.time() - start_time
    print('Elapsed: %s' % elapsed_time)
    print('Count: %s' % count)
    return

    for line in input_file:
        line = line.replace(u'NULL','').strip()
        fields = line.split('@')
        for i in interesting_fields:
            print fields[i],'X',
        return
        if fields[80] != '0':
            output_file.write("%s\n" % line)
            count += 1
            if verbose and count % reporting_interval == 0:
                elapsed_time = time.time() - start_time
                print('%s: %s' % (count, elapsed_time))
            if count > limit and limit > 0:
                break
    elapsed_time = time.time() - start_time
    print('Elapsed: %s' % elapsed_time)
    print('Count: %s' % count)


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
    Parse options and convert file.
    """

    (options, args) = process_options()
    if len(args) == 0:
        input_filename = '../data/fact_table_extract_2009_10.txt'
    else:
        input_filename = args[0]
    output_filename = '../data/fact_2009_10_1000.csv'
    convert_to_utf8(output_filename, input_filename, 1000, True)


if __name__ == "__main__":
    main()
