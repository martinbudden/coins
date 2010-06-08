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
    15 - Accounting_Authority
    16 - Accounts_capital_current
    17 - Activity_code
    18 - Budget_Boundary
    19 - Budget_capital_current
    20 - Resource_Capital
    21 - Programme_admin
    22 - CGA_Body_Type
    23 - COFOG
    24 - Dept_Group
    Estimate_line
    Estimate_line_last_year
    Estimate_line_next_year
    ESA
    Estimates_AinA
    Estimates_capital_current
    EU
    Income_Category
    LG
    LG_Body_Type
    Estimate_number
    Estimate_number_last_year
    Estimate_number_next_year
    NAC
    Near_Cash_Non_Cash
    NHS_Body_Type
    PC_Body_Type
    PESA
    PESA_1_1
    PESA_AEF_Grants
    PESA_Capital_Support
    PESA_Current_Grants
    PESA_Delivery
    PESA_Non_AEF_Grants
    PESA_Services
    PESA_Tables
    PESA_Transfer
    Request_for_resources
    Request_for_resources_last_year
    Request_for_resources_next_year
    SBI
    Sector
    SIGNAGE
    Territory
    Cbal
    Grant_Provision
    Levy_Funded
    Local_Government_Use_only
    Net_Subhead
    Non_ID_Exceptions
    NotOCS
    Obal
    Outside TES
    Pension
    PESA_1_1_CAP
    PESA_1_1_EC_Payments
    PESA_1_1_Local_Exp
    PESA_1_1_Nat_Lottery
    PESA_1_1_Tax_Credits
    PESA_1_2_NHS
    PESA_1_4_Locally_Financed
    PESA_BBC
    PESA_STU_LOANS
    Social_Fund
    Trust_Debt_Remuneration
    Value
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
ACCOUNTING_AUTHORITY = 15
ACCOUNTS_CAPITAL_CURRENT = 16
ACTIVITY_CODE = 17
BUDGET_BOUNDARY = 18
BUDGET_CAPITAL_CURRENT = 19
RESOURCE_CAPITAL = 20
PROGRAMME_ADMIN = 21
CGA_BODY_TYPE = 22
COFOG = 23
DEPT_GROUP = 24
ESTIMATE_LINE = 25
ESTIMATE_LINE_LAST_YEAR = 26
ESTIMATE_LINE_NEXT_YEAR = 27
ESA = 28
ESTIMATES_AINA = 29
ESTIMATES_CAPITAL_CURRENT = 30
EU = 31
INCOME_CATEGORY = 32
LG = 33
LG_BODY_TYPE = 34
ESTIMATE_NUMBER = 35
ESTIMATE_NUMBER_LAST_YEAR = 36
ESTIMATE_NUMBER_NEXT_YEAR = 37
NAC = 38
NEAR_CASH_NON_CASH = 39
NHS_BODY_TYPE = 40
PC_BODY_TYPE = 41
PESA = 42
PESA_1_1 = 43
PESA_AEF_GRANTS = 44
PESA_CAPITAL_SUPPORT = 45
PESA_CURRENT_GRANTS = 46
PESA_DELIVERY = 47
PESA_NON_AEF_GRANTS = 48
PESA_SERVICES = 49
PESA_TABLES = 50
PESA_TRANSFER = 51
REQUEST_FOR_RESOURCES = 52
REQUEST_FOR_RESOURCES_LAST_YEAR = 53
REQUEST_FOR_RESOURCES_NEXT_YEAR = 54
SBI = 55
SECTOR = 56
SIGNAGE = 57
TERRITORY = 58
VALUE = 80


# subset of interesting fields in the COINS database
FIELD_SUBSET_0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 24, 25,
    ESA, ESTIMATE_NUMBER, NAC, PESA, SBI, SECTOR, TERRITORY, VALUE]
