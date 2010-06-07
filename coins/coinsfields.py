#!/usr/bin/env python
#coding=utf-8
#file: coinsfields.py

"""
Constants relating to COINS fields

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
    24 - Dept_Group
    56 - Sector
    80 - Value

"""

#Column numbers for COINS fields (zero based)
FIELD_COUNT = 81
DATA_TYPE = 0
DATA_TYPE_DESCRIPTION = 1
DEPARTMENT_CODE = 2
DEPARTMENT_DESCRIPTION = 3
ACCOUNT_CODE = 4
ACCOUNT_DESCRIPTION = 5
DATA_SUBTYPE = 6
DATA_SUBTYPE_DESCRIPTION = 7
TIME = 8
COUNTERPARTY_CODE = 9
COUTERPARTY_DESCRIPTION = 10
PROGRAMME_OBJECT_CODE = 11
PROGRAMME_OBJECT_DESCRIPTION = 12
PROGRAMME_OBJECT_GROUP_CODE = 13
PROGRAMME_OBJECT_GROUP_DESCRIPTION = 14
RESOURCE_CAPITAL = 20
CGA_BODY_TYPE = 21
DEPT_GROUP = 24
SECTOR = 56
VALUE = 80

# subset of interesting fields in the COINS database
FIELD_SUBSET_0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 20, 22, 24, 56, 80]
