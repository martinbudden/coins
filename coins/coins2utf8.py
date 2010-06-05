#!/usr/bin/env python
#coding=utf-8
#file: coins2utf8.py

"""
Converts COINS text files from UTF-16 to UTF-8
"""

from optparse import OptionParser
import codecs


def convert_to_utf8(output_filename, input_filename, limit, verbose):
    """
    Convert file from utf16 to utf8.

    Keyword arguments:
    output_filenname -- the name of the converted file
    input_filenname -- the name of file to be converted

    """
    input_file = codecs.open(input_filename, 'r', 'utf_16_le', 'ignore')
    output_file = codecs.open(output_filename, 'w', 'utf_8', 'ignore')
    i = 0
    for line in input_file:
        output_file.write("%s\n" % line.replace(u'NULL','').strip())
        i += 1
        if i > limit and limit > 0:
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
        input_filename = 'fact_table_extract_2009_10.txt'
    else:
        input_filename = args[0]
    output_filename = 'fact_2009_10_2000.csv'
    convert_to_utf8(output_filename, input_filename, 2000, False)


if __name__ == "__main__":
    main()
