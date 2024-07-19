import logging
import pandas as pd
import xlwings as xw
from datetime import datetime

from child_vac_code.utilities import helpers, processing
import child_vac_code.parameters as param

"""
This module contains all the functions used to validate the childhood vaccinations data
The write arguments in get_validations are defined as:

name : str
    Excel worksheet where data is to be written.
write_type: str
    Determines the method of writing the output. Valid options for Excel are:
    excel_static: Writes data to Excel where the length of the data is
    static. Use for timeseries data with a limited number of years to show.
    e.g. time series data fixed to 3 years
    (write_cell must be populated).
    excel_variable: Writes data to Excel where the length of the data is
    variable (write_cell must be populated).
    excel_add_year: Adds a new year (row) to a time series before writing.
    If used then write_cell/year_check_cell should be set as the first year
    in the time series, and include_row_labels should be set to True.
    Can only be used where year values are in rows.
write_cell: str
    Identifies the cell location in the Excel worksheet where the data
    will be pasted (top left of data).
    If write_type is excel_add_year then this is not used (set to None).
include_row_labels: bool
    Determines if the row labels will be written.
empty_cols: list[str]
    A list of letters representing any empty (section separator) excel
    columns in the worksheet. Empty columns will be inserted into the
    dataframe in these positions. Default is None.
year_check_cell: str
    Cell location
    If the output is a time series table, this identifies the cell
    location in the Excel worksheet that contains the latest year value for a
    fixed length time series, or
    where write_type is excel_add_year, then the first year value in the time
    series.
    Used to determine if the new year value already exists i.e. is an update
    rather than an additional data year.
years_as_rows: bool
    Set to true if years in a time series table are arranged in rows (vertical).
    Only used if year_check_cell is not None.
    Set to False if years are arranged in columns (horizontal) or year_check_cell is None
contents: list[str]
    The name of the function that creates the output.
    If more than one function is included, the outputs will be appended.
    Note that multiple contents keys can be added to the dictionary with
    different suffixes (e.g. contents_1), as long as the outputs are of the
    same length and order e.g.same organisation type. The outputs of each
    contents_ key will be joined before writing, retaining only the first
    version of duplicate columns.
    Note that where adding multiple contents keys, the include_row_label
    argument must be consistent for all the functions called (will only return
    one version of the labels if set to True)

"""


def get_validations_main():
    """
    Establishes the functions (contents) required for each main validation output,
    and the arguments needed for the write process.

    Parameters:
        None

    """

    all_outputs = [
        # Primary vaccination numerator <= secondary
        {"name": "SubsetBreaches",
         "write_type": "excel_variable",
         "include_row_labels": False,
         "write_cell": "A2",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents": [create_primary_secondary_num_check],
         },
        # Numerator and denominator the same
        {"name": "NumDenom_Same",
         "write_type": "excel_variable",
         "include_row_labels": False,
         "write_cell": "A2",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents": [create_num_denom_same_check],
         },
        # YoY checks
        {"name": "YoY_Check",
         "write_type": "excel_variable",
         "include_row_labels": False,
         "write_cell": "A2",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents": [create_yoy_check],
         },
    ]

    return all_outputs


"""
The following functions are used to create the contents referenced above

NOTE - this excludes the create_outliers function which uses its own write
process within the function below

"""


def create_outliers(df_combined):
    """
    Creates the outliers output for the childhood vaccinations data
    and outputs it to the outliers file in the Validations folder.

    Current outlier checks (values flagged with a 1 in Outlier_Check column):
        - any coverage value that is < 5th percentile or > 95th percentile
        coverage value for this year

    Parameters
    ----------
    df_combined : pandas.DataFrame
        Contains the childhood vaccinations data for the current year (raw data)
        and historical years to check for outliers

    Returns
    -------
    None - outlier data is outputted to Excel file in Validations folder

    """
    logging.info("Creating the outliers output and writing to Validations folder")

    # Create crosstab of data for years required for outliers
    df = df_combined
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Org_Code", "Org_Name", "Org_Type", "Data_Type", "Child_Age", "Vac_Type"]
    columns = "FinancialYear"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = "Vac_Type not in ({0})".format(param.EXCLUDE_VACCS_VAL)
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = param.TS_YEARS_VAL_OUTLIERS

    df_output = processing.create_output_crosstab(df, org_type, output_type,
                                                  rows, columns, sort_on,
                                                  row_order, column_order,
                                                  column_rename, filter_condition,
                                                  row_subgroup, column_subgroup,
                                                  count_multiplier,
                                                  ts_years).reset_index()

    # Convert the financial year start to financial year
    fyear = helpers.fyearstart_to_fyear(param.FYEAR_START)

    # Remove any rows where an org didn't supply data for a vaccination this year
    df_output = df_output[df_output[fyear].notnull()]

    # Calculate coverage difference
    df_output = helpers.add_column_difference(
        df_output, "Coverage_Diff")

    # Get list of vaccinations to check (from vac_type column)
    # (sorted descending so last vac_type outputted first in Excel)
    vac_types = sorted(df_output["Vac_Type"].drop_duplicates(), reverse=True)

    # Open new empty Excel file
    wb = xw.Book()

    # For each vac_type coverage value assign outlier flag and output to new Excel file
    for vac_type in vac_types:
        # Filter data for vac type to be checked
        df_outlier = df_output[df_output["Vac_Type"] == vac_type].copy()

        # Flag outliers for coverage this year (5th/95th percentile)
        df_outlier = helpers.flag_outliers_percentiles(df_outlier,
                                                       fyear,
                                                       5, 95)

        # Re-order by coverage descending for output
        df_outlier.sort_values(by=[fyear], ascending=False, inplace=True)

        # Insert datestamp
        df_outlier.insert(0, "DATESTAMP", datetime.now())

        # Add sheet for vac_type
        sht = wb.sheets.add(vac_type)

        # Output data to sheet
        sht.range("A1").options(index=False).value = df_outlier

    # Delete default sheet
    wb.sheets["Sheet1"].delete()

    # Save file as outliers file in Validations folder
    wb.save(param.OUTLIER_FILEPATH)


def create_yoy_check(df_combined):
    """
    Creates the Year on Year check output for the childhood vaccinations data

    Parameters
    ----------
    df_combined : pandas.DataFrame
        Contains the childhood vaccinations data for the current year (raw data)
        and historical years to perform year on year checks on

    Returns
    -------
    df_output : pandas.DataFrame
        Contains results of YoY checks for this year, with any breaches
        flagged with a 'Y'

    """
    logging.info("Creating the YoY check output")

    # Get list of measures to check and YoY breach limits
    measures_to_check = param.YOY_MEASURE_TO_CHECK
    yoy_breach_limits = param.YOY_BREACH_LIMITS

    # Convert the financial year starts to financial year
    fyear = helpers.fyearstart_to_fyear(param.FYEAR_START)
    fyear_prev = helpers.fyearstart_to_fyear(param.FYEAR_START_PREV)

    # Create empty list for appending YoY check outputs
    total_dfs = []

    # Run YoY check for each specified measure and append df to list
    for measure in measures_to_check:
        df = df_combined
        org_type = "LA"
        rows = ["Org_Code", "Org_Name", "Org_Type", "Data_Type", "Child_Age", "Vac_Type"]
        columns = "FinancialYear"
        sort_on = None
        row_order = None
        column_order = None
        column_rename = None
        row_subgroup = None
        column_subgroup = None
        filter_condition = "Vac_Type not in ({0})".format(param.EXCLUDE_VACCS_VAL)
        row_subgroup = None
        column_subgroup = None
        count_multiplier = None
        ts_years = param.TS_YEARS_VAL_MAIN_YOY
        output_type = measure

        df_yoy = processing.create_output_crosstab(df, org_type, output_type,
                                                   rows, columns, sort_on,
                                                   row_order, column_order,
                                                   column_rename, filter_condition,
                                                   row_subgroup, column_subgroup,
                                                   count_multiplier,
                                                   ts_years).reset_index()

        # Remove any rows where an org didn't supply data for a vaccination this year
        df_yoy = df_yoy[df_yoy[fyear].notnull()]

        # If population, add eligible population labels for main vaccinations
        # as set in parameters.py
        if measure == "Population":
            for pop_label, vac_type in param.POPULATION_VACCINES_VAL.items():
                df_yoy.loc[df_yoy["Vac_Type"] == vac_type, "Vac_Type"] = pop_label

            # Filter for eligible population rows
            df_yoy = df_yoy[df_yoy["Vac_Type"].str.endswith("Eligible_Pop")]

        # Add YoY change columns
        if measure in ["Population"]:
            df_yoy = helpers.add_column_perc_difference(df_yoy, fyear_prev, fyear,
                                                        "YoY_Change")

        if measure in ["Coverage"]:
            df_yoy = helpers.add_column_difference(df_yoy, "YoY_Change")

        # Add breach flags based on values in parameters.py
        for measure_to_check, limits in yoy_breach_limits.items():
            if measure == measure_to_check:
                lower_limit = limits[0]
                upper_limit = limits[1]

                df_yoy = helpers.flag_values_outsidelimits(df_yoy,
                                                           "YoY_Change",
                                                           lower_limit,
                                                           upper_limit)

        # Add average for time series
        df_yoy = helpers.add_average_of_columns_year(df_yoy, fyear,
                                                     ts_years,
                                                     "fyear")

        # Add validation description
        df_yoy["Validation_Desc"] = "YoY_" + measure

        # Append df to list
        total_dfs.append(df_yoy)

    # Combine YoY data for all measures
    df_output = pd.concat(total_dfs, axis=0).reset_index(drop=True)

    # Create absolute YoY change field for sorting
    df_output["YoY_Change_abs"] = df_output["YoY_Change"]
    df_output.loc[df_output["YoY_Change"] < 0,
                  "YoY_Change_abs"] = (df_output["YoY_Change"] * -1)

    # Sort so breaches with largest YoY changes at top
    df_output.sort_values(by=["BreachFlag", "YoY_Change_abs", "Org_Name", "Vac_Type"],
                          inplace=True,
                          ascending=[False, False, True, True])

    # Insert financial year and datestamp columns at front
    df_output.insert(0, "ThisFinancialYear", fyear)
    df_output.insert(0, "DATESTAMP", datetime.now())

    # Remove absolute year change column from output
    df_output.drop("YoY_Change_abs", axis=1, inplace=True)

    return df_output


def create_primary_secondary_num_check(df_combined):
    """
    Creates the 'primary/secondary numerator' check output for the
    childhood vaccinations raw data, which selects any rows where the
    number vaccinated for the primary course is less than or equal to the
    number vaccinated for the secondary course
    e.g. where numerator for DTaP_IPV_Hib_5y <= the booster DTaP_IPV_5y

    Parameters
    ----------
    df_combined : pandas.DataFrame
        Contains the childhood vaccinations data for the current year (raw data)
        and historical years

    Returns
    -------
    df_output : pandas.DataFrame
        Contains data for this year where primary course vaccine numerator is
        less than or equal to secondary course
    """
    logging.info("Creating the primary/secondary course numerator check output")

    # Convert the financial year start to financial year
    fyear = helpers.fyearstart_to_fyear(param.FYEAR_START)

    # Filter data to current year
    df = df_combined[df_combined["FinancialYear"] == fyear].copy()

    # Get dictionary of primary and secondary course vaccines to check
    vaccs_to_check = param.PRIM_SECOND_NUM_VACCS_TO_CHECK

    # Setup empty list for combining dfs
    total_dfs = []

    for primary_vacc, secondary_vacc in vaccs_to_check.items():
        # Filter for vac types
        df_filter = df[df["Vac_Type"].isin([primary_vacc, secondary_vacc])].copy()

        # Generalise vaccine name
        df_filter.replace([primary_vacc, secondary_vacc],
                          ["Measure1", "Measure2"],
                          inplace=True)

        # Pivot so one column of vaccinated and population per vac type
        df_pivot = pd.pivot_table(df_filter,
                                  values=["Number_Vaccinated", "Number_Population"],
                                  index=["FinancialYear", "Org_Code", "Org_Name",
                                         "Org_Type", "Data_Type"],
                                  columns="Vac_Type"
                                  )

        # Collapse multi index so one level of columns and rename
        df_pivot = df_pivot.set_axis(["_".join(c) for c in df_pivot.columns],
                                     axis='columns', inplace=False)

        # Filter for rows where primary vacc is <= secondary vacc
        df_check = df_pivot[df_pivot["Number_Vaccinated_Measure1"]
                            <= df_pivot["Number_Vaccinated_Measure2"]].copy()

        # Add vaccine labels
        df_check["Measure1"] = primary_vacc
        df_check["Measure2"] = secondary_vacc

        # Add check label
        df_check["Breach_Reason"] = f"Number vaccinated for {primary_vacc} is <= {secondary_vacc}"

        # Append to list of dfs
        total_dfs.append(df_check)

    # Combine all check outputs
    df_output = pd.concat(total_dfs).reset_index()

    # Add 'no breaches found' row if dataframe is empty
    if df_output.empty:
        df_new_row = pd.DataFrame({"FinancialYear": ["NO BREACHES FOUND"]})
        df_output = pd.concat([df_output, df_new_row])

    # Select columns
    df_output = df_output[["FinancialYear", "Org_Code", "Org_Name",
                           "Org_Type", "Data_Type", "Measure1",
                           "Number_Population_Measure1",
                           "Number_Vaccinated_Measure1",
                           "Measure2", "Number_Population_Measure2",
                           "Number_Vaccinated_Measure2",
                           "Breach_Reason"]
                          ].sort_values(by=["Org_Name", "Breach_Reason"])

    # Insert datestamp
    df_output.insert(0, "DATESTAMP", datetime.now())

    return df_output


def create_num_denom_same_check(df_combined):
    """
    Creates the 'numerator/denominator the same' check output for the
    childhood vaccinations raw data, which selects any rows where the
    number vaccinated (numerator) is the same as the population (denominator)

    Parameters
    ----------
    df_combined : pandas.DataFrame
        Contains the childhood vaccinations data for the current year (raw data)
        and historical years

    Returns
    -------
    df_output : pandas.DataFrame
        Contains data for this year where numerator and denominator
        are the same
    """
    logging.info("Creating the numerator/denominator the same check output")

    # Convert the financial year start to financial year
    fyear = helpers.fyearstart_to_fyear(param.FYEAR_START)

    # Set filters to filter data to current year, exclude non required vaccines,
    # where numerator = denominator, and denominator not zero
    current_year = (df_combined["FinancialYear"] == fyear)
    exclude_vaccines = (~df_combined["Vac_Type"].isin(param.EXCLUDE_VACCS_VAL))
    num_denom_same = (df_combined["Number_Population"] ==
                      df_combined["Number_Vaccinated"])
    pop_not_zero = (df_combined["Number_Population"] != 0)

    # Apply filters
    df_output = df_combined[current_year & exclude_vaccines & num_denom_same &
                            pop_not_zero].copy()

    # Add 'no breaches found' row if dataframe is empty
    if df_output.empty:
        df_new_row = pd.DataFrame({"FinancialYear": ["NO BREACHES FOUND"]})
        df_output = pd.concat([df_output, df_new_row])

    # Select columns
    df_output = df_output[["FinancialYear", "Org_Code", "Org_Name",
                           "Org_Type", "Data_Type", "Child_Age", "Vac_Type",
                           "Number_Population", "Number_Vaccinated"]
                          ].sort_values(by=["Org_Name", "Vac_Type"])

    # Insert datestamp
    df_output.insert(0, "DATESTAMP", datetime.now())

    return df_output
