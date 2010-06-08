#!/usr/bin/env python
#coding=utf-8
#file: coins2utf8.py

"""
Converts COINS text files from UTF-16 to UTF-8
"""

from optparse import OptionParser
import codecs
import time

import coinsfields

def _normalize_time_field(time_val):
    """
    Convert time field value to normalized form.

    """
    _map = {
        'April 2009 MTH': u'2009.04',
        'May 2009 MTH': u'2009.05',
        'June 2009 MTH': u'2009.06',
        'July 2009 MTH': u'2009.07',
        'August 2009 MTH': u'2009.08',
        'September 2009 MTH': u'2009.09',
        'October 2009 MTH': u'2009.10',
        'November 2009 MTH': u'2009.11',
        'December 2009 MTH': u'2009.12',
        'January 2010 MTH': u'2010.01',
        'February 2010 MTH': u'2010.02',
        'March 2010 MTH': u'2010.03'
    }
    return _map.get(time_val, time_val)


def convert_to_utf8(output_filename, input_filename, output_fields, limit, verbose):
    """
    Convert file from utf16 to utf8.

    Keyword arguments:
    output_filenname -- the name of the converted file
    input_filenname -- the name of file to be converted

    """
    if verbose:
        print
        print "Creating:", output_filename
    input_file = codecs.open(input_filename, 'r', 'utf_16_le', 'ignore')
    delimiter = '@'

    output_file = codecs.open(output_filename, 'w', 'utf_8', 'ignore')

    start_time = time.time()
    reporting_interval = 1000

    # read in the column headers
    line = input_file.next()
    line = line.replace(u'NULL','').strip()
    fields = line.split(delimiter)
    out_line = ''
    for i in output_fields[:-1]:
        out_line += fields[i] + delimiter
    out_line += fields[output_fields[-1]]
    output_file.write("%s\n" % out_line)

    # read in the data
    try:
        count = 0
        zero_count = 0
        non_zero_count = 0
        bad_row_count = 0
        while 1:
            count += 1
            line = input_file.next()
            line = line.replace(u'NULL','').strip()
            fields = line.split(delimiter)
            if len(fields) != coinsfields.FIELD_COUNT:
                bad_row_count += 1
                print "Skipping row with %d columns" % len(fields)
                print line
                continue
            if fields[coinsfields.VALUE] == '0':
                zero_count += 1
                continue
            non_zero_count += 1
            fields[coinsfields.TIME] = _normalize_time_field(fields[coinsfields.TIME])
            out_line = ''
            for i in output_fields[:-1]:
                out_line += fields[i] + delimiter
            out_line += fields[output_fields[-1]]
            output_file.write("%s\n" % out_line)
            if verbose and count % reporting_interval == 0:
                elapsed_time = time.time() - start_time
                print('%s: %s' % (count, elapsed_time))
            if limit > 0 and non_zero_count >= limit:
                break
    except StopIteration:
        pass

    elapsed_time = time.time() - start_time
    print('Elapsed: %s' % elapsed_time)
    print('Number of rows: %s' % count)
    print('Number of rows with zero value: %s' % zero_count)
    print('Bad row count: %s' % bad_row_count)
    print
    return


def process_options(arglist=None):
    """
    Process options passed either via arglist or via command line args.

    """
    parser = OptionParser(arglist)
    #parser.add_option("-f", "--file", dest="filename",
    #                  help="file to be converted",metavar="FILE")
    #parser.add_option("-d", "--date", dest="date",
    #                  help="published DATE", metavar="DATE")
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
    verbose = True
    output_filename = '../data/facts_2009_10_nz_fs_1000.csv'
    convert_to_utf8(output_filename, input_filename, coinsfields.FIELD_SUBSET_0, 1000, verbose)
    output_filename = '../data/facts_2009_10_nz_1000.csv'
    convert_to_utf8(output_filename, input_filename, range(coinsfields.FIELD_COUNT), 1000, verbose)

    output_filename = '../data/facts_2009_10_nz.csv'
    convert_to_utf8(output_filename, input_filename, range(coinsfields.FIELD_COUNT), 0, verbose)
    input_filename = '../data/fact_table_extract_2008_09.txt'
    output_filename = '../data/facts_2008_09_nz.csv'
    convert_to_utf8(output_filename, input_filename, range(coinsfields.FIELD_COUNT), 0, verbose)


if __name__ == "__main__":
    main()
