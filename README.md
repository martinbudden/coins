Coins
=====

This repository contains utilities to read HM Treasury COINS (Combined Online Information System) files, and to convert them to more usable formats.


Installation
------------

Install the [git](http://git-scm.com/download) version control system

Download this repository:

    git clone git@github.com:martinbudden/coins.git

Install python, if you do not already have it.


Usage
-----

Before running any of these utilities the HM Treasury COINS files should be downloaded, unzipped and placed in the "data" directory. After downloading and unzipping the COINS data released on 4th June 2010 the "data" directory should include the four files:

* fact_table_extract_2009_10.txt
* fact_table_extract_2008_09.txt
* adjustment_table_extract_2009_10.txt
* adjustment_table_extract_2008_09.txt

These files are in unicode format and need to be converted to UTF-8 format for easier usage. Run coins2utf8.py to do this:

    python coins2utf8.py

This currently only operates on the fact_table_extract_*.txt files. It currently does three operations:

* converts the file to UTF-8 csv format (field delimiter is still '@')
* extracts only those records where the 'Value' field is non-zero

The output of coins2utf8.py is the files facts_2008_09_nz.csv and facts_2009_10_nz.csv. Note that 'nz' stands for 'non-zero'. The file facts_2009_10_s1000.csv is also produced - this is a small file of 1000 records which can be loaded into a spreadsheet to get a feel for the data. (Note that the field delimiter is '@' and this needs to be specified when loading the file, not also that one of the departmental_codes is 'DEC066', which may be interpreted as a date - be sure to set the 'Column type' for this column to be 'TEXT' when loading the file into a spreadsheet.)

Next run coinsdescriptions.py. This extracts varies COINS codes and descriptions (eg department_code and department_description) and places them in .csv files the data/desc directory. These files are standard .csv files and can be loaded into (say) Excel.

    python coinsdescriptions.py

This completes the preliminary preprocessing of the coins files. You may now run coins2csv.py to produce .csv files that can be directly loaded into Excel, or coins2sqlite.py which produces an Sqlite database of the coins data.


###Producing COINS files that can be loaded into Excel

Run coins2csv.py. This uses the the facts_*_nz.csv files output from coins2utf8.py to produce a .csv file for the data_types 'outturn', 'forecasts', 'plans' and 'snapshots'.

    python coins2csv.py

Most of these .csv files are small enough (less than 65,535 rows) to be loaded into Excel. These files are in the data/csv directory, and are named: 

    coin_<date_period>_<data_type>_nz.csv, eg coins_2009_10_outturn_nz.csv.


###Producing a COINS SQLite database

Run coins2sqlite.py. This uses the the facts_*_.csv files output from coins2utf8.py and the description .csv files produced by coinsdescription.py, to produce an SQLite database that can be queried.

    python coins2sqlite.py

This produces the files coins_2008_09_sqlite.db and coins_2009_10_sqlite.db in the data/sqlite directory

###Example SQL queries

Run coinssqlexamples.py. This executes a number of example queries on the COINS SQLite datbase, coins_2009_10_sqlite.db.

    python coinssqlexamples.py

###Recreating government PESA reports

Run coinssqlpesa.py. This produces HTML tables of the 2008-09 government departmental group spending figures. The tables include two empty columns than can be manually filled with the actual PESA data, so that the figures can be compared.

    python coinssqlpesa.py

Data Source
-----------

* [HM Government Combined Online Information System](http://data.gov.uk/dataset/coins)
* [HM Treasury - Understanding the COINS data](http://www.hm-treasury.gov.uk/d/coins_guidance_040610.pdf)


Treasury Information
--------------------

HM Treasury publish documents that may help to understand COINS and, and how that data may be used and aggregated. These include:

* [Public spending planning and control - a brief introduction](http://www.hm-treasury.gov.uk/psr_spend_plancontrol.htm)
* [Consolidated Budgeting Guidance](http://www.hm-treasury.gov.uk/psr_bc_consolidated_budgeting.htm)
* [Classification papers](http://www.hm-treasury.gov.uk/psr_bac_classification_papers.htm)
* Information on the Supply Estimates process at: [Financial reporting - Parliamentary Supply Estimates](http://www.hm-treasury.gov.uk/psr_estimates_index.htm)

Slightly differing approaches are taken to some data recording and outputs for the Devolved Administrations. Some information on that, by means of concordats, is available here: [Devolved Assemblies](http://www.hm-treasury.gov.uk/psr_devolved_assemblies.htm)

HM Treasury publishes a number of documents based COINS data. Public Spending Statistics are available here: [Statistics on Public Finance and Spending](http://www.hm-treasury.gov.uk/finexp_index.htm).


Checking Data
-------------

[PESA 2010 section 1 - Budgets](http://www.hm-treasury.gov.uk/pesa2010_section1.htm) gives the outrun DEL, AME, Capital and Resource outrun figures for 2004-05 to 2008-09. Outrun figures from the COINS 2008/09 Fact table can be checked against these tables.

[Public Expenditure Statistical Analyses 2009](http://www.hm-treasury.gov.uk/pespub_pesa09.htm) gives the outrun DEL, AME, Capital and Resource outrun figures for 2003-04 to 2007-08 and the estimated outrun for 2008-09 and the planned outruns for 2009-10 and 2010-2011. Forecast figures from the COINS 2009/10 Fact table can be checked against these tables.

I've briefly outlined what some of the fields in the COINS data mean in the [data/README.md](http://github.com/martinbudden/coins/blob/master/data/README.md) file.


Useful links
------------

* [Where Does My Money Go?](http://www.wheredoesmymoneygo.org/)
* Where Does My Money Go? - [A User Guide to COINS](http://www.wheredoesmymoneygo.org/data/coins/)
* Open Knowledge Foundation Blog - [The Hunt For COINS](http://blog.okfn.org/2010/02/22/the-hunt-for-coins/)
* Open Knowledge Foundation Blog - [COINS: A Users Guide](http://blog.okfn.org/2010/06/04/coins-a-users-guide/)
* What Do They Know [COINS database schema](http://www.whatdotheyknow.com/request/25039/response/67260/attach/3/100111%20COINS%20Schema%20for%20FOI%209%201049.xls)
* EtherPad - [Coins open notepad](http://pad.okfn.org/coins)
* Google spreadsheet of [COINS Schema overview:](http://spreadsheets.google.com/ccc?key=0Ah8UkI7xG7eWdHpYMnhaWmR5NVdNUG9yTkNfQVlUTWc&hl=en_GB)


Coding resources
----------------

* Open Knowledge Foundation(okfn) [coins python scripts](http://bitbucket.org/okfn/coins)
