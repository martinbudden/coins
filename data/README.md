Coins Data Documentation
========================

Using the COINS utilities
-------------------------

Before running any of these utilities the HM Treasury COINS files should be downloaded, unzipped and placed in the "data" directory. After downloading and unzipping the COINS data released on 4th June 2010 the "data" directory should include some or all of the four files:

* fact_table_extract_2009_10.txt
* fact_table_extract_2008_09.txt
* adjustment_table_extract_2009_10.txt
* adjustment_table_extract_2008_09.txt


File formats
------------

The fact_table_extract_*.txt files are in UTF-16 format with records delimited by carriage return and fields delimited by '@'.


Overview of COINS data
----------------------

The structure of the COINS data is explained in  [HM Treasury - Understanding the COINS data](http://www.hm-treasury.gov.uk/d/coins_guidance_040610.pdf).

The documents on the [Public Expenditure Statistical Analyses 2010](http://www.hm-treasury.gov.uk/pespub_pesa10_natstats.htm) page are useful. The meaning of the terms used (DEL, AME, outrun etc) is explained in the [PESA 2010 National Statistics release](http://www.hm-treasury.gov.uk/pespub_pesa10_natstats.htm), in the 'How to use PESA' section and Chapter 1 'Departmental Budgets'.

The documents on the [Public Expenditure Statistical Analyses 2009](http://www.hm-treasury.gov.uk/pespub_pesa09.htm) page are also useful, in particular the Introduction and Chapter 1 of [Public ExpenditureStatistical Analyses 2009](http://www.hm-treasury.gov.uk/d/pesa_180609.pdf)

###Very brief summary

A clear distinction is made between current and capital spending, based on Generally Accepted Accounting Practice (GAAP). The "Resource_Capital" field has a value of "Resource" or "Capital" to reflect this.

Departments are given firm three year spending limits called Departmental Expenditure Limits (DELs) within which they prioritise resources and plan ahead. Spending that cannot reasonably be subject to firm multi-year limits, or that relates to certain non-cash transactions, is included in Annually Managed Expenditure (AME). DEL and AME together make up TME (Total Managed Expenditure). The "Budget_Boundary" field has a value of "DEL", "AME" or "Not DEL/AME" to reflect this.

The Treasury maintains data for recorded spending, planned spending and forecast spending. The "Data_type" field has values that reflect this, including "Outturn", "Plans" "Forecast Outturn <month>" (eg "Forecast Outturn March").

Spending is by department. The "Department_code" field reflects this.

