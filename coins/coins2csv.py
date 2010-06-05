#!/usr/bin/env python
#coding=utf-8
#file: coins2csv.py

"""
Convert COINS text file from UTF-16 to UTF-8
"""

import codecs


def main():
    """
    Parse options and call example function.
    """

    input = codecs.open('fact_table_extract_2009_10.txt','r','utf_16_le','ignore')
    output = codecs.open('clean2000.csv','w','utf_8','ignore')
    i = 0
    for line in input:
        #output.write("%s\n" % line.replace(u'NULL','').replace('@',',').strip())
        output.write("%s\n" % line.replace(u'NULL','').strip())
        i += 1
        if i > 2000:
            return


if __name__ == "__main__":
    main()
