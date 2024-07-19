from pathlib import Path
import os
import logging
import shutil
import pandas as pd
import numpy as np
import math
import datetime
from itertools import chain, combinations
from decimal import Decimal, ROUND_HALF_UP, getcontext


def create_folder(directory):
    """
    Creates a empty folder where it doesn't already exist
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def remove_folder(directory):
    """
    Removes the specified folder and all it's contents
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)
    else:
        pass


def get_project_root() -> Path:
    """
    Return the project root path from any file in the project.

    Example:
        from child_vac_code.utilities.helpers import get_project_root
        root_path = get_project_root()
    """
    return Path(__file__).parent.parent.parent


def get_year_range(end_year: str, year_span: int):
    """
    Create list of year strings, given an end year and a number of years to go back
    Based on financial start year format DDMMMYYYY

    Example:
        get_year_range('01APR2021',2)
        returns -> ['01APR2021','01APR2020']
    """
    year_range = []

    for n_year in range(year_span):
        year = (str(int(end_year[5:9])-(n_year)))
        year = "01APR" + year
        year_range.append(year)
        n_year += 1

    # List oldest year first
    return year_range[::-1]


def create_year_list(df, year_field):
    """
    Creates a list of years contained in a dataframe. This list can be used
    within loops in functions used to create time series tables.

    Parameters
    ----------
    df : pandas.DataFrame
    year_field : list[str]
        Variable name that holds year data

    Returns
    -------
    years : list
        Returns a list of years, order by oldest first

    """
    # Creates a list of years in the dataframe to loop through, oldest year first
    years = set(df[year_field].values)
    years = list(years)
    years.sort()

    return years


def lookup_column(df, from_column, lookup, new_column):
    """
    Add a new dataframe column by looking up values in a dictionary

    Parameters
    ----------
    df : pandas.DataFrame
    from_column: str
        name of the column containing the original values
    lookup: dict
        contains the lookup from and to values
    new_column: str
        name of the new column containing the values to be added

    Returns
    -------
    df : pandas.DataFrame
        with added column
    """
    # create the lookup dataframe from the lookup input
    df_lookup = pd.DataFrame(list(lookup.items()))
    df_lookup.columns = [from_column, new_column]

    # add the new column based on the lookup dataframe
    df = df.merge(df_lookup, how='left',
                  on=[from_column])

    return df


def replace_col_value(df, col_names, replace_value):
    """
    Will replace all values in a column(s) with a specified default value

    Parameters
    ----------
    df : pandas.DataFrame
    col_names : list[str]
        Names of columns where rate values to be replaced
    replace_value : str
        Value to replace existing rate values (e.g ":")

    Returns
    -------
    df : pandas.DataFrame
        With updated values for specified columns
    """

    for col in col_names:
        df[col] = replace_value

    return df


def remove_rows(df, remove_values):
    """
    Will remove rows from dataframe that contain the specified values

    Parameters
    ----------
    df : pandas.DataFrame
    remove_values : list[str]
        list of values based on which the rows will be removed if found
        in any dataframe columns.

    Returns
    -------
    df : pandas.DataFrame
        With rows removed
    """
    for condition in remove_values:
        df = df[~df.eq(condition).any(axis=1)]

    return df


def excel_cell_to_row_num(cell):
    '''
    Convert Excel cell reference to Excel row number for use in
    xlwings (e.g. A1 = 1, C23 = 23).

    Parameters
    ----------
    cell: str
        Excel cell reference (e.g. "A1")
    Returns
    -------
    int
        Number indicating the equivalent Excel row number
    '''
    # Convert the cell reference to row number
    row_num = int(''.join(filter(str.isdigit, cell)))

    return row_num


def excel_cell_to_col_num(cell):
    '''
    Convert Excel cell reference to Excel numeric column position for use in
    xlwings (e.g. A1 = 1, C23 = 2).

    Parameters
    ----------
    cell: str
        Excel cell reference (e.g. "A1")
    Returns
    -------
    int
        Number indicating the equivalent Excel column number
    '''
    # Convert the cell reference to column letter(s)
    col = ''.join(filter(str.isalpha, cell))

    # return the excel column number
    col_num = 0
    for c in col:
        col_num = col_num * 26 + (ord(c.upper()) - ord('A')) + 1

    return col_num


def excel_col_letter_to_col_num(col):
    '''
    Converts an Excel column letter into the Excel column number e.g. if the
    column letter is D, then the output will be 4.

    Parameters
    ----------
    col: str
        Excel column letter

    Returns
    -------
    order of letter value: int
        Excel column number
    '''
    column_number = ord(col[0])-ord('A') + 1
    if len(col) == 1:
        column_number
    if len(col) == 2:
        column_number = (int(math.pow(26, len(col)-1) * column_number
                             + excel_col_letter_to_col_num(col[1:])))

    return column_number


def excel_col_to_df_col(col, write_cell):
    '''
    Converts an Excel column letter into a dataframe column position based on
    a starting cell (write_cell) in Excel e.g. if the column letter is D, and the
    write_cell is B10, then the output will be 2 (3rd column in dataframe)

    Parameters
    ----------
    col: str
        Excel column letter
    write_cell: str
        cell that identifies start of where df will be written

    Returns
    -------
    order of letter value: int
        number indicating which position to insert new column into dataframe
    '''
    if len(col) == 1:
        return (ord(col[0])) - (ord(write_cell[0]))
    if len(col) == 2:
        return (int(math.pow(26, len(col)-1)*(ord(col[0]) - ord('A') + 1)
                    + excel_col_to_df_col(col[1:], write_cell)))


def validate_value_with_list(check_name, value, valid_values):
    """
    Checks a string against a list of strings and aborts the process if it is not
    found in the list.

    Parameters
    ----------
    check_name: str
        Name of the item being checked that will be returned in the system
        exit message.
    value: str
        Value to be checked.
    valid_values: list[str]
        Contains the valid values to check against.
    """
    if value not in valid_values:
        raise ValueError(f'An invalid value has been entered in the {check_name}\
                         input. Only {valid_values} are valid values')


def add_percent_or_rate(df, new_column_name, numerator,
                        denominator, multiplier=1):
    """
    Adds a percent or rate to a dataframe based on specified column inputs.

    Parameters
    ----------
    df : pandas.DataFrame
    new_column_name: str
        Name of the new calculated column.
    numerator: str
        Name of dataframe column that contains the numerator values
    denominator: str
        Name of dataframe column that contains the denominator values
    multiplier: int
        Value by which the calculated field will be multiplied by e.g. set to
        100 for percents. If no multiplier is needed then the parameter should
        be excluded or set to 1.

    Returns
    -------
    pandas.DataFrame
    """
    if numerator not in df:
        raise ValueError(f"The column {numerator} is needed to create\
                         {new_column_name} but is not in the dataframe")
    if denominator not in df:
        raise ValueError(f"The column {denominator} is needed to create\
                         {new_column_name} but is not in the dataframe")

    df[new_column_name] = ((df[numerator]/df[denominator] * multiplier))

    return df


def add_column_difference(df,
                          new_column_name="Difference"):
    """
    Adds a difference column to a dataframe based on the last 2 columns.

    Parameters
    ----------
    df : pandas.DataFrame
    new_column_name: str
        Name of the new calculated column. Set by default to 'Difference'

    Returns
    -------
    pandas.DataFrame
    """
    # Select the last 2 columns in the dataframe
    df_columns = df.iloc[:, -2:]
    from_column = df_columns.iloc[:, 0]
    to_column = df_columns.iloc[:, 1]
    # Extract the column names of the 2 columns on which the calculation will
    # be performed
    from_column_name = from_column.name
    to_column_name = to_column.name

    # Check for numeric values in the 2 columns
    if from_column.dtypes not in ["integer", "float"]:
        raise ValueError(f"A difference calculation is being performed on column\
                         ({from_column_name}) that contains non-numeric values")
    if to_column.dtypes not in ["integer", "float"]:
        raise ValueError(f"A difference calculation is being performed on column\
                         ({to_column_name}) that contains non-numeric values")

    # Add a new column with the calculated difference
    df[new_column_name] = (to_column - from_column)

    return df


def add_subtotals(df, columns,
                  total_name="Grand_Total"):
    """
    Add row totals and sub-totals to a dataframe for all specified dataframe
    column combinations.

    Parameters
    ----------
    df : pandas.DataFrame
    columns: list[str]
        Columns to use in the breakdowns (e.g. age, sex, etc)
    total_name: str
        Default value to be assigned where totals are added.

    Returns
    -------
    pandas.DataFrame

    """

    # List to store the different sub-groups
    total_dfs = []

    # Combinations of columns to be replaced with total_name
    # Firstly don't replace any, then replace a single column, then 2 columns, etc
    # E.g. [[], ["sex"], ["age"], ["sex", "age"], ...]
    n_replacements = len(columns) + 1
    replace_combinations = [combinations(columns, n) for n in range(n_replacements)]
    replace_combinations = chain.from_iterable(replace_combinations)

    for columns_to_replace in replace_combinations:
        # Make a copy of dataframe with default values for non-grouped columns
        # inserted (e.g. replace values in 'sex' with total_name)
        default_df = df.copy()

        for col in columns_to_replace:
            default_df[col] = total_name

        # Aggregate the column values / counts
        default_df = default_df.groupby(columns).sum().reset_index()

        # Add each of the subgroup dataframes just created to the total dataframe
        # list
        total_dfs.append(default_df)

    # Add each dataframe from the list of dataframes together
    return pd.concat(total_dfs, axis=0).reset_index(drop=True)


def add_subgroup_rows(df, breakdown, subgroup):
    """
    Combines groups of values in specified dataframe column into a subgroup
    and adds new rows to the dataframe with the grouped value.

    Parameters
    ----------
    df : pandas.DataFrame
        Data with breakdowns and counts
    breakdown: list[str]
        The column(s) present in the dataframe on which the data is aggregated
        i.e. the non count/measure columns
        This can include the column to which the subgroup function is being
        applied.
    subgroup: dict(dict(str, list))
        Contains the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
        e.g. {"AgeBand": {'53<71': ['53-54', '55-59', '60-64', '65-69', '70']}}

    Returns
    -------
    pandas.DataFrame with subgroup added to target column

    """
    # Extract the target column, and the subgroup info (a 2nd dictionary nested
    # within the subgroup dictionary)
    for subgroup_column, subgroup_info in subgroup.items():
        # For each set of items in subgroup info
        for subgroup_code, subgroup_values in subgroup_info.items():
            # Then add new rows for the subgroup
            df_subgroup = df[df[subgroup_column].isin(subgroup_values)].copy(deep=True)
            df_subgroup[subgroup_column] = subgroup_code
            df_subgroup = (
                df_subgroup.groupby([*breakdown])
                .sum()
                .reset_index()
            )
            df = pd.concat([df, df_subgroup], ignore_index=True)

    return df


def add_subgroup_columns(df, subgroup):
    """
    Combines groups of specified columns into a single summed column

    Parameters
    ----------
    df : pandas.DataFrame
        Data with a breakdown
    subgroup: dict(str, list)
        Contains new column name that will be assigned to the grouping,
        and the columns that will form the group.

    Returns
    -------
    pandas.DataFrame with subgroup column(s) added

    """
    for subgroup_name, subgroup_cols in subgroup.items():
        df[subgroup_name] = df[subgroup_cols].sum(axis=1)

    return df


def order_by_list(df, column, order):
    """
    Orders the dataframe based on a custom list applied to a specified column

    Parameters
    ----------
    df : pandas.DataFrame
        Data with a breakdown
    column: str
        Column name to be ordered on.
    order: list[str]
        List that contains the custom order for the specified column
    Returns
    -------
    pandas.DataFrame with subgroup column(s) added

    """
    # Create a dummy df with the required list and the column name to sort on
    dummy = pd.Series(order, name=column).to_frame()

    # Use left merge on the dummy to return a sorted df
    ordered_df = pd.merge(dummy, df, on=column, how='left')

    return ordered_df


def group_numeric_values(df, source_field, group_name,
                         group_info, default_value):
    '''
    Creates a new column in the dataframe based on an existing one by grouping
    numeric values in the existing column

    Parameters
    ----------
    df : pandas.DataFrame
    source_field : str
        Name of the dataframe variable that contains the value on which the
        grouped values are based
    group_name : str
        Name of the column that will hold the grouped information (if it
        doesn't already exist then it will be created.
    group_info : dict
        Dictionary containing the labels and ranges for each group
    default_value : str
        String of the default value upon column creation. Can be set to
        None if not required. This can also be used to edit an existing
        column (as per group_name) if it is already present.

    Returns
    -------
        pandas.Dataframe with new column added or modified
    '''
    if default_value is not None:
        df[group_name] = default_value

    for range_label, range_info in group_info.items():
        for range_start, range_end in range_info.items():
            df.loc[df[source_field].between(range_start, range_end),
                   group_name] = range_label

    return df


def add_group_to_df(df, group_on, group_value, count_columns):
    '''
    Groups a dataframe on a single column and appends it back to the original
    dataframe with a user defined value.

    Parameters
    ----------
    df : pandas.DataFrame
    group_on : str
        Name of the dataframe variable that contains the data to be grouped.
    group_value : float
        Value that will be assigned to the grouped data. e.g. if grouping
        "males" and "females" then this might be "All". Data type should be
        the same as that in the group_on column.
    count_columns : str[list]
        List of one or more dataframe variable(s) containing the data counts.

    Returns
    -------
        pandas.Dataframe with grouped data appended.

    '''
    # Identify the position of the group on column in the dataframe. Used for
    # inserting a new group_on column into the grouped dataframe later
    insert_position = df.columns.get_loc(group_on)

    # Create a list of dataframe columns and exclude the group on and count
    # columns
    all_fields = df.columns.values.tolist()
    fields_to_remove = [group_on] + count_columns
    grouped_fields = list(set(all_fields) - set(fields_to_remove))

    # Create a new dataframe grouped on the required column
    df_grouped = df.groupby(grouped_fields,
                            as_index=False)[count_columns].sum()
    # Insert a new column to represent the grouped data and apply the user
    # defined value
    df_grouped.insert(insert_position, group_on, group_value)

    # Append the grouped data to the original dataframe
    return pd.concat([df, df_grouped], ignore_index=True)


def suppress_column(column_to_suppress,
                    lower=1, upper=7, base=5):
    """Follows HES disclosure control guidance.
    https://digital.nhs.uk/data-and-information/data-tools-and-services/data-services/hospital-episode-statistics/change-to-disclosure-control-methodology-for-hes-and-ecds-from-september-2018
    For sub-national counts, suppress the values of a count column
    based on upper and lower bounds, and round the values above the upper bound
    to the nearest base.

    If not national level, then apply suppression and rounding as per below logic.
    If more than or equal to lower bound and less than or equal to upper bound,
    then replace the values with "*".
    If more than upper value, then round to the nearest 5.

    Parameters
    ----------
    col_to_suppress: pd.Series
        A numeric series that should be suppressed
    lower: int
        Lower bound - default is 1
        Used to filter for values more than or equal to 1 (>=1).
    upper: int
        Upper bound - default is 7
        Used to filter for values less than or equal to 7 (<=7).
    base: int - default is 5
        Round to the nearest base.
        E.g. a value of 21 or 22 would round to 20,
        while value of 23 or 24 would round to 25.

    Returns
    -------
    pd.Series

    """
    # Copy of the column to suppress
    suppression = column_to_suppress.copy(deep=True)

    # Filter data between lower and upper bound that should be suppressed
    # for sub-national level
    should_suppress = (column_to_suppress.between(lower, upper, inclusive="both"))
    # Filter data above upper limit to be rounded for sub-national level
    should_round = (column_to_suppress > upper)

    # Suppression and rounding logic for relevant data defined by above filters
    # if data should be suppressed, replace with *
    suppression.loc[should_suppress] = "*"

    # If data should be rounded, round to the nearest base
    suppression.loc[should_round] = (
        suppression[should_round]
        .apply(
            lambda p: base * round(p/base)
        )
    )

    return suppression


def add_organisation_type(df, org_code_column,
                          include_level=True, missing_value="None"):
    """
    Adds a new organisation type and level columns to a dataframe
    based on the entity codes in the organisation reference data.
    This should include all organisation types that are processed by the
    pipeline. Add more as required.

    Parameters
    ----------
    df : pandas.DataFrame
    org_code_column: str
        Name of the column that contains the organisation codes
    include_level: bool
        Determines if the 'Org_Level' column will be added.
        Set to True by default.
    missing_value: str
        Value that will be returned if no organisation type can be assigned.
        Set to "None" by default.

    Returns
    -------
    df_population : pandas.DataFrame

    """
    # Set the names of the new columns
    col_org_type = "Org_Type"
    col_org_level = "Org_Level"

    # Set the new columns as the default missing value
    df[col_org_type] = missing_value
    df[col_org_level] = missing_value

    # Set the Org Type
    df.loc[df[org_code_column].str.startswith(("E01")),
           [col_org_type, col_org_level]] = ["LSOA", "LSOA"]
    df.loc[df[org_code_column].str.startswith(("E06", "E07", "E08", "E09", "E10")),
           [col_org_type, col_org_level]] = ["LA", "Local"]
    df.loc[df[org_code_column].str.startswith(("E12")),
           [col_org_type, col_org_level]] = ["LA_parent", "Regional"]
    df.loc[df[org_code_column].str.startswith(("E38")),
           [col_org_type, col_org_level]] = ["CCG", "Local"]
    df.loc[df[org_code_column].str.startswith(("E54")),
           [col_org_type, col_org_level]] = ["ICB", "Local"]
    df.loc[df[org_code_column].str.startswith(("E40")),
           [col_org_type, col_org_level]] = ["ICB_parent", "Regional"]
    df.loc[df[org_code_column].str.startswith(("E92")),
           [col_org_type, col_org_level]] = ["National", "National"]

    if not include_level:
        df = df.drop(columns=[col_org_level])

    return df


def fyear_to_year_start_end(fyear):
    '''
    From a standard financial year (YYYY-YY) creates year start and year end
    outputs in date format (yyyy-mm-dd)

    Parameters
    ----------
    fyear : str
        Financial year in format YYYY-YY

    Returns
    -------
        tuple
    '''
    # Create fy start and end dates from the financial year input
    fy_start = datetime.date(int(fyear[:4]), 4, 1)
    fy_end = datetime.date(int(fyear[:4]) + 1, 3, 31)

    return (fy_start, fy_end)


def round_half_up(argument, decimals=0):
    """
    Round a given number, n, to a given number of decimal places, rounding up
    on >=5, and down on <5. E.g. (1.5, 0) = 2, (2.44, 1) = 2.4. Will round negative
    numbers away from 0. E.g. (-0.5, 0) = -1, (-1.234, 2) == -1.23.

    A guide to using the Decimal module can be found here:
    https://docs.python.org/3/library/decimal.html

    Parameters
    ----------
    n : float
        Number to be rounded
    decimals : integer, optional
        Number of decimal places to round to. The default is 0.

    Returns
    -------
    float

    """

    # Set the context for rounding, the precision, and the method of rounding
    context = getcontext().copy()
    context.prec = decimals + 10
    context.rounding = ROUND_HALF_UP

    # Recursively applies the function to the column elements
    if isinstance(argument, pd.Series):
        df_rounded = argument.apply(
            lambda x: argument.inf
            if x == np.inf
            else round_half_up(x, decimals)
        )
        return df_rounded

    # Creates a Decimal object from the given number n, with the given
    # number of decimal places. The quantize method rounds to the nearest
    # integer, using the 'ROUND_HALF_UP' method
    n_rounded = float(context.create_decimal(str(argument)).quantize(
        Decimal('0.' + '0'*decimals), context=context))

    return n_rounded


def fyearstart_to_fyear(year_start):
    '''
    From a financial year start date (ddmmmyyyy) creates financial year (yyyy-yy)

    Parameters
    ----------
    year_start : str
        Financial year start date in format ddmmmyyyy (e.g. '01APR2021')

    Returns
    -------
    fyear : str
        Financial year in format yyyy-yy (e.g. '2021-22')
    '''
    # Create start year and end year from the financial year start input
    start_year = year_start[5:9]
    end_year = str(int(start_year) + 1)[2:4]

    # Combine to create the financial year
    fyear = start_year + "-" + end_year

    return fyear


def expected_column_check(df, input_name, expected_cols):
    """
    Checks whether a dataframe contains the expected columns specified, and raises an
    error and aborts the process if it doesn't

    Parameters
    ----------
    df : pandas.DataFrame
        Containing columns to be validated
    input_name: str
        Name of input data being checked (used in error message)
        e.g. "Alcohol source data"
    expected_cols: list[str]
        Columns expected to be found in the dataframe

    Raises
    ------
    ValueError
        Message to alert users that expected columns were not found in dataframe

    Returns
    -------
    None.

    """

    # Get columns from dataframe to check
    cols_to_check = df.columns

    # Check dataframe contains all expected columns
    missing_cols = []
    for col in expected_cols:
        if col not in cols_to_check:
            missing_cols.append(col)

    # If any expected columns not found, raise ValueError and print missing columns
    if len(missing_cols) != 0:
        raise ValueError(
            f"Error - {input_name} does not contain expected columns {missing_cols}")


def invalid_row_check(df, val_type, invalid_condition, val_groups, output_path,
                      invalid_message, output_limit=None, fyear=None):
    """
    Checks for any invalid rows in a DataFrame based on condition specified,
    then outputs those rows to the .csv file specified by 'output_path'
    and prints a message to the user.

    Parameters
    ----------
    df : pandas.DataFrame
        Data to be validated
    val_type: str
        Type of validation - valid options are 'error' or 'warning'.
        In both cases the invalid rows are outputted and the invalid_message printed,
        but 'error' means the process is aborted, while 'warning' means the process
        will continue
    invalid_condition : str
        Condition that defines what an invalid value is e.g.
        "Org_code.isnull()" if null values in Org_code column need to be flagged
    val_groups : list[str]
        Columns to group output by - this will also filter only for unique
        values in those combined rows and sort by those columns
        e.g. rows where Org_code is null, outputted by unique combos of
        ["DH_geography_code", "Category"]
    output_path : str
        Filepath (including name) of .csv file to save invalid rows output to
    invalid_message : str
        Message to be displayed to users when invalid rows are discovered
        - a formatted string can be used when references to other parameters
        is needed e.g 'f"Org_code values for submitting ICBs could not be found,
        invalid rows have been outputted to {output_path}"'
    output_limit: int, optional
        Number of rows to limit the output to e.g if set to 1, only one invalid
        row will be outputted to file.

        Default is None - means all rows will be outputted
    fyear : str, optional
        Expected financial year of extract (yyyy-yy) generated based on the
        financial year start specified in parameters file

        Default is None - only needed for validation checks where year being
        checked is generated by process and not in parameters file

    Raises
    ------
    warning or ValueError
        Message to warn users of invalid rows, where their details have been saved,
        and any recommended actions

    Returns
    -------
    None.

    """

    # Check val_type specified is valid
    validate_value_with_list("val_type", val_type, ["error", "warning"])

    # Filter data for invalid rows
    df_invalid = df.query(invalid_condition)

    # If output limit specified, select only rows required
    if output_limit is not None:
        df_invalid = df_invalid.head(output_limit)

    if val_groups is not None:
        # Filter/group/sort results by validation groupings
        df_invalid = df_invalid[val_groups].drop_duplicates().sort_values(by=val_groups)

    # Delete validation output file if already exists
    if os.path.exists(output_path):
        os.remove(output_path)

    # If invalid rows have been found
    if not df_invalid.empty:
        # For 'error' validation types
        if val_type == "error":
            # Output invalid rows to validation checks area and raise ValueError
            # - this will abort the process
            df_invalid.to_csv(output_path, index=False)
            raise ValueError(invalid_message)

        # For 'warning' validation types
        elif val_type == "warning":
            # Output invalid rows to validation checks area and raise warning
            # - this won't abort the process
            df_invalid.to_csv(output_path, index=False)
            logging.info(invalid_message)


def get_year_range_fy(end_year: str, year_span: int):
    """
    Create list of financial year strings, given an end year and a number
    of years to go back.

    List will include end_year value

    Example:
        get_year_range("2020-21",2)
        returns -> ["2020-21","2019-20"]

    NOTE - can only correctly create ranges containing years from 2000-01 onwards

    Parameters
    ----------
    end_year: str
        end of year range in format yyyy-yy
    year_span: int
        number of years in range

    Returns
    -------
    list[str] : list of years

    """
    # Create empty list to populate with years in range
    year_range = []

    # Create range of year numbers based on year_span e.g. 3 = 0, 1, 2
    # Loop through each year number
    for n_year in range(year_span):
        # Create financial year start and end values based on the
        # year number and the end_year
        year_start = str(int(end_year[0:4])-(n_year))
        year_end = str(int(end_year[5:7])-(n_year))

        # If year_end is less than 2 digits, add a 0 at the start
        if len(year_end) < 2:
            year_end = year_end.zfill(2)

        # Create new year and append to list
        year = year_start + "-" + year_end
        year_range.append(year)

    # Return list of years, ordered so oldest year first
    return year_range[::-1]


def flag_outliers_percentiles(df, col_to_check, percentile_lower,
                              percentile_upper):
    """
    Flag outlier values in a dataframe column based on the lower
    and upper percentiles specified e.g. 5th and 95th

    This function uses the numpy percentile function to get the values
    in the existing data related to the percentiles specified,
    and then flags values in the data when they are either lower or higher
    than those existing values
    e.g. if 5th percentile value in data = 68.123 and 95th = 92.123
    then all values < 68.123 or > 92.123 are flagged as outliers

    Parameters
    ----------
    df : pandas.DataFrame
        Source data to check for outliers
    col_to_check : str
        Name of column to check for outliers
    percentile_lower : int
        Lower percentile e.g. 5
    percentile_upper : int
        Upper percentile e.g. 95

    Returns
    -------
    df : pandas.DataFrame
        Source data with a new column 'Outlier_Check' added flagging
        any outliers within the checked column with a 1

    """
    # Order column values in ascending order
    df.sort_values(by=[col_to_check], ascending=True, inplace=True)

    # Get percentile values from data
    percentile_lower_value = np.percentile(df[col_to_check],
                                           percentile_lower,
                                           interpolation="lower")

    percentile_upper_value = np.percentile(df[col_to_check],
                                           percentile_upper,
                                           interpolation="higher")

    # Add outlier flag where values are higher/lower than percentile values
    df["Outlier_Check"] = 0
    df.loc[(df[col_to_check] > percentile_upper_value) |
           (df[col_to_check] < percentile_lower_value),
           "Outlier_Check"] = 1

    return df


def add_column_perc_difference(df, from_column, to_column,
                               new_column_name="perc_difference"):
    """
    Adds a percentage difference column to a dataframe based on two
    defined columns

    Parameters
    ----------
    df : pandas.DataFrame
        Contains the two defined columns
    from_column : str
        Name of the column representing the 'from' data in the change comparison
        e.g. if comparing 2021-22 data with 2022-23, would be 2021-22 column
    to_column : str
        Name of the column representing the 'to' data in the change comparison
        e.g if comparing 2021-22 data with 2022-23, would be 2022-23 column
    new_column_name: str
        Name of the new calculated column. Set by default to 'perc_difference'

    Returns
    -------
    pandas.DataFrame
    """
    # Check for numeric values in the 2 columns
    if df[from_column].dtypes not in ["integer", "float"]:
        raise ValueError(
            f"A difference calculation is being performed on column ({from_column}) that contains non-numeric values")
    if df[to_column].dtypes not in ["integer", "float"]:
        raise ValueError(
            f"A difference calculation is being performed on column ({to_column}) that contains non-numeric values")

    # Add a new column with the calculated difference
    df[new_column_name] = ((df[to_column] - df[from_column])/df[from_column])*100

    # Where both to and from values are 0, set percentage difference to 0
    df.loc[(df[to_column] == 0) & (df[from_column] == 0), new_column_name] = 0

    return df


def add_average_of_columns_year(df, end_column, number_cols,
                                year_format, new_column_name="YearAverage"):
    """
    Adds an average value column to a dataframe based on a specified subset of
    year columns

    Parameters
    ----------
    df : pandas.DataFrame
        Containing year columns to calculate average from - all columns should
        be named per the year and have the same format (see year_format below)
    end_column: str
        The name of the final year column used to define the subset of data the average
        will be calculated from (e.g "01APR2022" or "2022-23")
    number_cols: int
        The number of columns to be used to calculate the average (e.g to calculate
        a 3 year average, number_cols will equal 3)

        NOTE - this includes 0's but excludes null values
        e.g. if a value for one of the year columns is null, then the average
        will be based on the other 2 years of data, but if it is 0 then it will
        remain as a 3 year average
    year_format: str
        Indicates the format of the year columns.
        Allowed values:
            "fyear_start" (DDMMMYYYY format e.g. 01APR2022)
            "fyear" (YYYY-YY format e.g. 2022-23)
    new_column_name: str, optional
        Name of the new calculated column.
        Default value is "YearAverage"

    Returns
    -------
    df : pandas.DataFrame
        Containing input data with an average value column added
    """

    # Check valid year format supplied
    validate_value_with_list("add_average_of_columns_year function year_format",
                             year_format, ["fyear_start", "fyear"])

    # Create list of column names to be used when calculating average
    # based on year format specified
    if year_format == "fyear_start":
        column_list = get_year_range(end_column, number_cols)
    elif year_format == "fyear":
        column_list = get_year_range_fy(end_column, number_cols)

    # Check all columns required for average are in dataframe
    expected_column_check(df, "add_average_of_columns_year input dataframe", column_list)

    # Use column name list to create a subset of the dataframe from which the mean
    # will be calculated from
    df_columns = df[column_list]

    for column in df_columns:
        if df[column].dtypes not in ["integer", "int64", "float"]:
            raise ValueError(
                f"add_average_of_columns_year function is being performed on column ({column}) that contains non-numeric values")

    # Calculate the mean for the subset of columns
    average_columns = df_columns.mean(axis=1)
    # Append mean as a field to the original full dataframe
    df[new_column_name] = average_columns

    return df


def flag_values_outsidelimits(df, col_to_check, lower_limit, upper_limit,
                              include_limits=True):
    """
    Flag values in a dataframe column outside the lower and upper limits specified.
    By default it flags where value is less than or equal to lower limit or
    greater than or equal to upper limit
    e.g. values of -5, -6, 5 or 6 would be flagged if the lower limit
    was -5 and the upper limit was 5

    To exclude limit values (e.g. switch to < and >) set include_limits to False

    Parameters
    ----------
    df : pandas.DataFrame
        Source data to apply flags to
    col_to_check : str
        Name of column containing values to check
    lower_limit : int
        Lower value to flag values against e.g. -5
    upper_limit : int
        Upper value to flag values against e.g. -5
    include_limits : bool
        Sets whether limit values are included when check is performed
        Default is True (limit values are included)

    Returns
    -------
    df : pandas.DataFrame
        Source data with a new column 'BreachFlag' added flagging
        any breach values with a 'Y'

    """
    # Set default flag value for no breach
    df["BreachFlag"] = "N"

    if include_limits:
        # Update value to 'Y' where value is <= lower limit or >= upper limit
        df.loc[(df[col_to_check] <= lower_limit) |
               (df[col_to_check] >= upper_limit), "BreachFlag"] = "Y"
    elif include_limits is False:
        # Update value to 'Y' where value is < lower limit or > upper limit
        df.loc[(df[col_to_check] < lower_limit) |
               (df[col_to_check] > upper_limit), "BreachFlag"] = "Y"

    return df
