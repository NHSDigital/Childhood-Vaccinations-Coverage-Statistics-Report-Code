from child_vac_code.utilities.processing import (create_csv_output,
                                                 create_output_crosstab)

"""
This module contains all the user defined inputs for each tidy csv output.
The write arguments in get_csvs are defined as:

name : str
    Name of the output file.
write_type: str
    Determines the method of writing the output.
    All should be set to 'csv' for these outputs.
contents: list[str]
    The name of the function that creates the output.
    If more than one function is included, the outputs will be appended.
    Note that multiple contents keys can be added to the dictionary with
    different suffixes (e.g. contents_1), as long as the outputs are of the
    same length and order e.g.same organisation type. The outputs of each
    contents_ key will be joined before writing, retaining only the first
    version of duplicate columns.

"""


def get_csvs_cover():
    """
    Establishes each of the output csv files, and associated processes
    required for each tidy csv.
    Add or remove any from the list as required.

    Parameters:
        None
    Returns:
        Filename and function to be run for each csv.

    """
    all_csvs = [
        {"name": "childhood-vaccination-la-num-denom",
         "write_type": "csv",
         "contents": [create_csv_la_pop,
                      create_csv_la_vax]},
        {"name": "childhood-vaccination-table-11a",
         "write_type": "csv",
         "contents_pop_la": [create_csv_11a_pop],
         "contents_vac_la": [create_csv_11a_vac],
         "contents_cov_la": [create_csv_11a_cov]},
        {"name": "childhood-vaccination-table-11b-11c",
         "write_type": "csv",
         "contents_pop_la": [create_csv_11b_11c_pop],
         "contents_vac_la": [create_csv_11b_11c_vac],
         "contents_cov_la": [create_csv_11b_11c_cov]}
    ]

    return all_csvs


"""
The following functions contain the user defined inputs that determine the
dataframe content for each output.

output_type : str
    Either "Population" or "Vaccinated"
    Used to specify whether the output will have population or vaccination figures
filter_condition : str
    This is a non-standard, optional dataframe filter as a string.
    It may consist of one or more filters of the dataframe variables.
    Used to filter population groups for demographics such as age group.
    Should be formatted as ('Column_Name in ["variable"]')
breakdowns : list[str]
    Variable names that are to be included in the output
    These should be listed from the imported dataframe column names
    Should not include the numerator or denominator column names as these
    are already specified in the function
    This will determine the column order in the output.
sort_on: list[str]
    List of columns names to sort on (ascending).
column_rename : dict
    Optional dictionary for renaming of columns from the data source version
    to output requirement.
        NB numerator and denominator will need to have the same name if appending
        to form a df with one indicator column
org_type : str
    Determines which of the pre-defined org types will be reported on. Used in
    the filter_dataframe function in conjunction with filter_condition parameter
    Default is "LA"
ts_years: int
    Number of years to be used in the time series.
    Default is 1.
num_column: str
    Name of the column that holds the measure (coverage) numerator data
    Default is "Number_Vaccinated"
denom_column: str
    Name of the column that holds the measure (coverage) denominator data
    Default is "Number_Population"


Returns:
-------
    Each function returns a dataframe with the output for the csv.

"""


# To create the population values for the rest of the tables csv
def create_csv_la_pop(df):
    output_type = "Population"
    filter_condition = ('Vac_Type not in (@param.SELECTIVE_VACCS)')
    breakdowns = ["FinancialYear",
                  "Parent_Org_Code",
                  "Parent_Org_Name",
                  "Org_Code",
                  "Org_Name",
                  "Child_Age",
                  "Vac_Type"]
    sort_on = ["Parent_Org_Code", "Org_Name", "Child_Age", "Vac_Type"]
    column_rename = {"Vac_Type": "Indicator",
                     "Number_Population": "Value",
                     "FinancialYear": "CollectionYearRange"}
    return create_csv_output(df, filter_condition, output_type,
                             breakdowns, sort_on, column_rename)


# To create the vaccinated values for the rest of the tables csv
def create_csv_la_vax(df):
    output_type = "Vaccinated"
    filter_condition = ('Vac_Type not in (@param.SELECTIVE_VACCS)')
    breakdowns = ["FinancialYear",
                  "Parent_Org_Code",
                  "Parent_Org_Name",
                  "Org_Code",
                  "Org_Name",
                  "Child_Age",
                  "Vac_Type"]
    sort_on = ["Parent_Org_Code", "Org_Name", "Child_Age", "Vac_Type"]
    column_rename = {"Vac_Type": "Indicator",
                     "Number_Vaccinated": "Value",
                     "FinancialYear": "CollectionYearRange"}
    return create_csv_output(df, filter_condition, output_type,
                             breakdowns, sort_on, column_rename)


# To create csv for table 11b/11c population
def create_csv_11b_11c_pop(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["FinancialYear", "Parent_Org_Code", "Parent_Org_Name", "Org_Code",
            "Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code", "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {"FinancialYear": "CollectionYearRange",
                     "HepB_Group2_12m": "HepB_12m_Population",
                     "HepB_Group2_24m": "HepB_24m_Population"}
    row_subgroup = None
    column_subgroup = None
    filter_condition = ("Vac_Type in ['HepB_Group2_12m', 'HepB_Group2_24m']")
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  row_subgroup, column_subgroup,
                                  count_multiplier, ts_years)


# To create csv for table 11b/11c vaccinated
def create_csv_11b_11c_vac(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["FinancialYear", "Parent_Org_Code", "Parent_Org_Name", "Org_Code",
            "Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code", "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {"FinancialYear": "CollectionYearRange",
                     "HepB_Group2_12m": "HepB_12m_Vaccinated",
                     "HepB_Group2_24m": "HepB_24m_Vaccinated"}
    row_subgroup = None
    column_subgroup = None
    filter_condition = ("Vac_Type in ['HepB_Group2_12m', 'HepB_Group2_24m']")
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  row_subgroup, column_subgroup,
                                  count_multiplier, ts_years)


# To create csv for table 11b/11c coverage
def create_csv_11b_11c_cov(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear", "Parent_Org_Code", "Parent_Org_Name", "Org_Code",
            "Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code", "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {"FinancialYear": "CollectionYearRange",
                     "HepB_Group2_12m": "HepB_12m_Coverage",
                     "HepB_Group2_24m": "HepB_24m_Coverage"}
    row_subgroup = None
    column_subgroup = None
    filter_condition = ("Vac_Type in ['HepB_Group2_12m', 'HepB_Group2_24m']")
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  row_subgroup, column_subgroup,
                                  count_multiplier, ts_years)


# To create csv for table 11a population
def create_csv_11a_pop(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["FinancialYear", "Parent_Org_Code", "Parent_Org_Name", "Org_Code",
            "Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {"FinancialYear": "CollectionYearRange",
                     "BCG_3m": "BCG_3m_Population"}

    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create csv for table 11a vaccinated
def create_csv_11a_vac(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["FinancialYear", "Parent_Org_Code", "Parent_Org_Name", "Org_Code",
            "Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {"FinancialYear": "CollectionYearRange",
                     "BCG_3m": "BCG_3m_Vaccinated"}

    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create csv for table 11a coverage
def create_csv_11a_cov(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear", "Parent_Org_Code", "Parent_Org_Name", "Org_Code",
            "Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {"FinancialYear": "CollectionYearRange",
                     "BCG_3m": "BCG_3m_Coverage"}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)
