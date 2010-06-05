#!/usr/bin/env python
#coding=utf-8
#file: coins2utf8.py

"""
Converts COINS text files from UTF-16 to UTF-8
"""

from optparse import OptionParser
import codecs
import time

TIME_FIELD = 8
VALUE_FIELD = 80

def _normalize_time_field(time_val):
    """
    Convert time field value to normalized form.

    """

    _map = {
        'January 2010 MTH': u'2010-01',
        'February 2010 MTH': u'2010-02',
        'March 2010 MTH': u'2010-03',
        'April 2009 MTH': u'2009-04',
        'May 2009 MTH': u'2009-05',
        'June 2009 MTH': u'2009-06',
        'July 2009 MTH': u'2009-07',
        'August 2009 MTH': u'2009-08',
        'September 2009 MTH': u'2009-09',
        'October 2009 MTH': u'2009-10',
        'November 2009 MTH': u'2009-11',
        'December 2009 MTH': u'2009-12'
    }
    return _map.get(time_val, time_val)


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
    reporting_interval = 1000
    interesting_fields = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 20, 22, 24, 56, 80]

    # read in the column headers
    line = input_file.next()
    line = line.replace(u'NULL','').strip()
    fields = line.split('@')
    out_line = ''
    for i in interesting_fields[:-1]:
        out_line += fields[i] + '@'
    out_line += fields[interesting_fields[-1]]
    output_file.write("%s\n" % out_line)
    print out_line

    # read in the data
    try:
        count = 0
        while 1:
            line = input_file.next()
            line = line.replace(u'NULL','').strip()
            fields = line.split('@')
            if fields[VALUE_FIELD] != '0':
                fields[TIME_FIELD] = _normalize_time_field(fields[TIME_FIELD])
                out_line = ''
                for i in interesting_fields[:-1]:
                    out_line += fields[i] + '@'
                out_line += fields[interesting_fields[-1]]
                output_file.write("%s\n" % out_line)
                count += 1
                if verbose and count % reporting_interval == 0:
                    elapsed_time = time.time() - start_time
                    print('%s: %s' % (count, elapsed_time))
                if limit > 0 and count >= limit:
                    break
    except StopIteration:
        pass

    elapsed_time = time.time() - start_time
    print('Elapsed: %s' % elapsed_time)
    print('Count: %s' % count)
    return


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
    output_filename = '../data/fact_2009_10.csv'
    #convert_to_utf8(output_filename, input_filename, 0, True)


if __name__ == "__main__":
    main()
