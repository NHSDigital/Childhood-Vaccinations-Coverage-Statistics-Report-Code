import pandas as pd
import numpy as np
import logging
import child_vac_code.parameters as param
from child_vac_code.utilities import helpers

logger = logging.getLogger(__name__)


def select_org_ref_data(org_type, columns):
    """
    Extracts the valid sub regional (local) level organisation reference
    data based on the org_type argument.

    Parameters
    ----------
    org_type: str
        Level of organisation required.
    columns : list[str]
        List of column names that are needed for the output. Function will use
        the information to extract the required organisation details (column names)
        from the org ref data.

    Returns
    -------
    df: pandas.DataFrame
        Containing only the organisation reference data for the required level

    """
    logging.info("Extracting the required type of organisation data")

    # Read in the organisation reference data from the cached folder.
    df_org_ref = pd.read_feather('cached_dataframes/df_org_ref.ft')

    # Check that a valid org_type has been used - exists in the organisation
    # reference data as added in pre_processing by helpers.add_organisation_type
    org_type_valid = df_org_ref[df_org_ref["Org_Level"] == "Local"]
    org_type_valid = org_type_valid["Org_Type"].unique().tolist()
    helpers.validate_value_with_list("Org_Type",
                                     org_type,
                                     org_type_valid)

    # Extract the required organisation types
    df_org_type = df_org_ref[df_org_ref["Org_Type"] == org_type]

    # For LA outputs, retain the upper tier LA's only
    df_org_type = df_org_type[df_org_type["Entity_code"] != "E07"]

    # Adjustment for standard columns required for some outputs
    # so that they are populated for any organisations with no data

    if "FinancialYear" in columns:
        # Add a financial year column from the parameter input
        fyear = helpers.fyearstart_to_fyear(param.FYEAR_START)
        df_org_type["FinancialYear"] = fyear

    # Check for any item in columns that do appear in the org ref data and
    # drop these from the org ref extract requirement
    columns = [item for item in columns if item in df_org_type.columns]

    # Extract the details (column names) needed for the output
    df_orgs = df_org_type[columns].copy()

    return df_orgs


def merge_org_ref_data(df, join_on, org_type, columns):
    """
    For local level outputs, joins the processed data for the output with the
    valid organisation details for the reporting period. All valid organisations
    will be outputted, even where no data exists for them.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the processed local level output data.
    join_on: str
        Column containing the local level organisation codes that will be
        used to join to the organisation ref data.
    org_type: str
        Level of organisation required for the output. Valid options are
        currently "LA".
    columns : list[str]
        List of column names that are needed for the output. Function will use
        the information to extract the required organisation details (column names)
        from the org ref data.

    Returns
    -------
    df: pandas.DataFrame

    """
    logging.info("Joining with organisation reference data")

    # For the required org type, extract the valid organisations with the
    # details needed
    df_valid_orgs = select_org_ref_data(org_type, columns)

    # Where any organisation details (apart from the org code to be joined on)
    # are present in the source data, drop these. They will be replaced with
    # organisation details from the reference data.
    cols_to_keep = df.columns.difference(df_valid_orgs.columns).tolist()
    cols_to_keep = [join_on] + cols_to_keep

    # Merge the organisation details with the data.
    df = (pd.merge(df_valid_orgs, df[cols_to_keep],
                   how="left", on=join_on))

    return df


def check_for_sort_on(sort_on, rows):
    """
    Check if the sort_on option has been used, and if so re-defines the row/breakdown
    content required for processing, in order that columns only needed for
    sorting are included, but then dropped later (cols_to_remove).

    Parameters
    ----------
    sort_on : list[str]
        list of columns names to sort on (ascending).
    rows : list[str]
        Column name(s) that holds the row/breakdown labels to be included
        in the output
    Returns
    -------
    df : pandas.DataFrame
    """

    if sort_on is not None:
        # Combine the rows and sort_on lists to ensure all are included for
        # processing (created as a set to remove fields appearing in both
        # lists)
        rows_all = set(rows + sort_on)
        # Identify any columns that are only used to sort on (will not be
        # included in the final output)
        cols_to_remove = list(set(rows_all) - set(rows))
        # Now redefine rows to also include the column(s) used for sorting only
        rows = rows + cols_to_remove
    # Else set the cols_to_remove list as empty
    else:
        cols_to_remove = []

    return (rows, cols_to_remove)


def sort_for_output_defined(df, rows, sort_info):
    """
    Sorts the dataframe in the user defined order required for the output.
    Ordering will be applied to any row content defined in the sort_info dictionary.

    Parameters
    ----------
    df : pandas.DataFrame
    rows : list(str)
        Variable name(s) that holds the row labels to be included
        in the output
    sort_info: dict(str, list)
        Dictionary with lists of row content that determines the inclusions and sorting.
        Contains the column name(s) and defined order of content for sorting.

    Returns
    -------
    df : pandas.DataFrame
    """

    # Apply the sort on order for each column included in the sort_info
    for sort_column, sort_order in sort_info.items():
        # Check the index position of the column to be sorted
        idx_position = df.columns.get_loc(sort_column)
        # Set the rows input as the index
        df.set_index(rows, inplace=True)
        # Re sort the column based on the sort order. Requires different
        # syntax for multi index dataframe.
        if df.index.nlevels > 1:
            df = df.reindex(sort_order, level=idx_position)
        else:
            df = df.reindex(sort_order)

        # Reset the index as per the original state
        df.reset_index(inplace=True)

    return df


def sort_for_output(df, sort_on, cols_to_remove, include_row_total=False,
                    total_name="Grand_total"):
    """
    Sorts the dataframe on specified columns required for the output.
    Drops columns only used for sorting.

    Parameters
    ----------
    df : pandas.DataFrame
    sort_on: list[str]
        Columns that will be sorted on (ascending).
    cols_to_remove : list[str]
        List containing the names of any columns to be removed (i.e. those only
        used for sorting).
    include_row_total: bol
        Determines if the grand total row will be included in the output.
        Set to True by default.
    total_name: str
        Name that was assigned to the total row that will be removed if not
        required.

    Returns
    -------
    df : pandas.DataFrame
    """
    # If total is not required then drop rows that contain the total name
    if include_row_total is False:
        df = helpers.remove_rows(df, [total_name])

    # Sort the dataframe based on columns defined by sort_on input
    df = df.sort_values(by=sort_on, ascending=True)

    # Move the total to the bottom of the dataframe (if present)
    if include_row_total:
        df = pd.concat([df[df.eq(total_name).any(axis=1)],
                        df[~df.eq(total_name).any(axis=1)]])

    # Drop any columns only used for sorting and not output to table
    if len(cols_to_remove) > 0:
        df.drop(columns=cols_to_remove, inplace=True)

    return df


def filter_dataframe(df, org_type, filter_condition, ts_years,
                     year_column="FinancialYear"):
    """
    Filters a dataframe by any standard filters, and by any additional optional
    filters required.

    Parameters
    ----------
    df : pandas.DataFrame
    org_type : str
        Determines which of the pre-defined org types will be reported on.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some tables. It may consist of one or more filters of the
        dataframe variables.
    ts_years : Num
        Defines the number of years required in the table.
    year_column : str
        Name of the column that contains the years to be filtered on.

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to the conditions input to the function.

    """
    # Filter dataframe on Org_Type where not None
    if org_type is not None:
        # Create a list of valid org types from the asset
        valid_org_types = df["Org_Type"].drop_duplicates().tolist()
        # Check for invalid org_type argument against the input value
        helpers.validate_value_with_list("Org_Type", org_type,
                                         valid_org_types)
        # Filter dataframe to org type
        df = df[df["Org_Type"] == org_type]

    # Filter dataframe to number of years defined in ts_years
    fyear = helpers.fyearstart_to_fyear(param.FYEAR_START)
    year_range = helpers.get_year_range_fy(fyear, ts_years)
    df = df[(df[year_column].isin(year_range))]

    # Apply the optional general filter
    if filter_condition is not None:
        df = df.query(filter_condition)

    return df


def apply_hepb_suppression(df, eligible_col, vaccinated_col, coverage_col):
    """
    Applies 2 pass suppression for HepB data to the following specification:
    a. Suppress all data (i.e. eligible population, number vaccinated and
    coverage) where the eligible population is 1 or 2.
    b. Where the eligible population is greater than 2 and the number of
    children vaccinated is 0 or 1, suppress the number of children vaccinated
    and the coverage.
    Suppression character is "*"


    Parameters
    ----------
    df : pandas.Dataframe
    eligible_col: str
        Name of the column that holds the eligible data.
    vaccinated_col: str
        Name of the column that holds the vaccinated data.
    coverage_col: str
        Name of the column that holds the coverage data.

    Returns
    -------
    df : pandas.Dataframe (suppressed)

    """

    # Initialise boolean flag for condition 1
    df["To_Suppress_con1"] = 0
    # Initialise boolean flag for condition 2
    df["To_Suppress_con2"] = 0
    # Set condition 1 flag
    df["To_Suppress_con1"] = (np.where((df[eligible_col] == 1) |
                                       (df[eligible_col] == 2),
                              1, df["To_Suppress_con1"]))

    # Set condition 2 flag
    df["To_Suppress_con2"] = (np.where((df[eligible_col] > 2) &
                                       (df[vaccinated_col] <= 1),
                                       1, df["To_Suppress_con2"]))

    # Mark suppressed if true
    df.loc[df["To_Suppress_con1"] == 1, [eligible_col,
                                         vaccinated_col,
                                         coverage_col]] = "*"
    df.loc[df["To_Suppress_con2"] == 1, [vaccinated_col,
                                         coverage_col]] = "*"

    # Drop suppress flag columns
    df.drop(columns=["To_Suppress_con1", "To_Suppress_con2"], inplace=True)

    return df


def create_output_crosstab(df, org_type, output_type, rows, columns, sort_on,
                           row_order, column_order, column_rename,
                           filter_condition, row_subgroup, column_subgroup,
                           count_multiplier, ts_years=1, rounding=False,
                           num_column="Number_Vaccinated",
                           denom_column="Number_Population"):
    """
    Will create a crosstab output based on any breakdown, and for any number of
    years.
    Measures are added if included in the row or column order and only
    fields required in the final output are included when writing to the file.

    Parameters
    ----------
    df : pandas.DataFrame
    org_type : str
        Determines which of the pre-defined org types will be reported on.
    output_type : str
        Determines which of the pre-defined output types will be reported on.
    rows : list[str]
        Variable name(s) that holds the row labels (e.g. regions) that are
        to be included in the output.
    columns : str
        Variable name that holds the information to be displayed in the output
        column headers (i.e. the measure(s))
    sort_on: list[str]
        List of columns names to sort on (ascending).
        Can include columns that will not be displayed in the output.
        Function will use either this OR row_order for sorting.
    row_order: dict(str, list)
        Dictionary with lists of row content that determines the inclusions
        and sorting. Contains the column name(s) and defined order of content
        in which data will be presented in the output. Allows for full control
        of row ordering (can only include row values that exist in the
        collection). Function will use either this OR sort_on for sorting.
    column_order: list[str]
        List of column descriptions that determines the order they will be
        presented in the output.
    column_rename : dict
        Optional dictionary for renaming of columns from the data source version
        to output requirement.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some tables. It may consist of one or more filters of the
        dataframe variables.
    row_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row content.
        Contain the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the
        grouping(s), and the original subgroup values that will form the group.
    column_subgroup: dict(str, list)
        Optional input where a grouped option is reported, requiring a new
        subgroup based on column content.
        Contains the new value(s) that will be assigned to the
        new grouping(s), and the values (from the 'columns' variable) that
        will form the group.
    count_multiplier: num
        All counts will be multiplied by this value in the output e.g. for
        thousands set to 0.001. Set to None if no multiplier is needed.
    ts_years: int
        Number of years to be used in the time series.
        Default is 1.
    num_column: str
        Name of the column that holds the measure (coverage) numerator data
    denom_column: str
        Name of the column that holds the measure (coverage) denominator data
    rounding: integer/bool
        Number of decimal places to round columns in column_order to.
        The default is False (no rounding applied)
    Returns
    -------
    df : pandas.DataFrame
        in the form of a crosstab, with aggregated counts
    """

    # Apply standard and optional filters to dataframe
    df_filtered = filter_dataframe(df, org_type, filter_condition, ts_years)

    # If sort_on is used, need to account for columns only used for sorting
    rows, cols_to_remove = check_for_sort_on(sort_on, rows)

    # For local (sub-regional) outputs some organisation details are added from
    # reference data later so are temporarily removed from the rows argument
    # Original version is stored when extracting from organisation ref data later.
    # Prevents the process trying to call columns that don't exist in the source data.
    rows_original = rows.copy()
    for variable in rows:
        if variable not in df_filtered.columns:
            rows.remove(variable)

    # Create a combined rows and columns list to represent all the variables
    # that will be grouped on.
    if columns is None:
        all_variables = rows
    else:
        all_variables = rows + [columns]

    # Aggregate the data by the required variables
    df_agg = (df_filtered.groupby(all_variables)[[num_column,
                                                  denom_column]]
              .sum())
    df_agg.reset_index(inplace=True)

    # Add any required row or column subgroups to data
    if row_subgroup is not None:
        df_agg = helpers.add_subgroup_rows(df_agg, rows, row_subgroup)

    if column_subgroup is not None:
        df_agg = helpers.add_subgroup_columns(df_agg, column_subgroup)

    # Apply the count multiplier if applicable
    if count_multiplier is not None:
        for column in [num_column, denom_column]:
            df_agg[column] = df_agg[column] * count_multiplier

    # Call the list of valid output types from parameters
    valid_output_types = param.OUTPUT_TYPE
    # Check for invalid output_type argument against the input value
    helpers.validate_value_with_list("output_type", output_type,
                                     valid_output_types)

    # Where output is coverage, calculate coverage and set as measure
    if output_type == "Coverage":
        df_agg = helpers.add_percent_or_rate(df_agg,
                                             "Coverage",
                                             num_column,
                                             denom_column,
                                             multiplier=100)
        measure = "Coverage"

    # Otherwise set measure for vaccinated and population columns
    elif output_type == "Vaccinated":
        measure = num_column
    elif output_type == "Population":
        measure = denom_column

    # Convert nulls (coverage values with 0 data) to a dummy value
    # for pivoting (prevents loss of nulls)
    if measure == "Coverage":
        dummy_value = -1
        df_agg[measure] = df_agg[measure].fillna(dummy_value)

    # Pivots the dataframe into a crosstab
    df_pivot = pd.pivot_table(df_agg,
                              values=measure,
                              index=rows,
                              columns=columns).reset_index()

    if measure == "Coverage":
        # Restore nulls where previously replaced with dummy value
        df_pivot.replace({-1: np.nan}, inplace=True)

    # Check the rows content for the presence of the 'Org_Code' column
    # If present then join to the valid organisation reference data.
    # This ensures all (and only) current valid organisations are included,
    # even those with no data.
    if "Org_Code" in rows:
        # Restore original rows argument to include columns that only exist
        # in org ref data.
        rows = rows_original
        df_pivot = merge_org_ref_data(df_pivot,
                                      "Org_Code", org_type, rows)

    # This section ensures column_order it is not empty when called in next step.
    # If no columns were defined then set it as the measure count created by
    # the earlier pivot function
    if columns is None:
        column_order = [measure]
    # Else if just no column_order was defined then set it as everything
    # present in the columns field (will be sorted ascending by default).
    elif column_order is None:
        column_order = df_pivot.set_index(rows).columns.tolist()

    # Set final df column content (for now including any column that is
    # only used for sorting). Done inside the loop before column renaming.
    df_order = df_pivot[rows + column_order].copy()

    # Apply selected row ordering option
    if row_order is not None:
        df_order = sort_for_output_defined(df_order, rows, row_order)
    elif sort_on is not None:
        df_order = sort_for_output(df_order, sort_on, cols_to_remove)

    # Remove any variables from rows that were only used for
    # sorting (as have now been dropped from df)
    rows = [item for item in rows if item not in cols_to_remove]

    # Apply optional rounding to columns, which rounds up to the nearest float given
    if rounding is not False:
        for col in column_order:
            df_order[col] = helpers.round_half_up(df_order[col], rounding)

    # Restore the row labels as the index
    df_order.set_index(rows, inplace=True)

    # Rename the user selected columns as defined in column_rename dictionary
    # even if they're in the index
    if column_rename is not None:
        df_order = df_order.rename(columns=column_rename)
        df_order.index = df_order.index.set_names(
            [column_rename.get(name, name) for name in df_order.index.names])

    return df_order


def create_csv_output(df, filter_condition, output_type, breakdowns, sort_on,
                      column_rename, org_type="LA", ts_years=1,
                      num_column="Number_Vaccinated",
                      denom_column="Number_Population"):
    """
    Creates data output for csv. Option to input population or vaccination.
    Inputting population will also add variable name to specify child age of population

    Parameters
    ----------
    df : pandas.DataFrame
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string.
        It may consist of one or more filters of the dataframe variables.
        Used to filter population groups for demographics such as age group.
        Should be formatted as ('Column_Name in ["variable"]')
    output_type : str
        Either "Population" or "Vaccinated"
        Used to specify whether the output will have population or vaccination figures
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
            to form one df
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

    Returns
    -------
    df_csv : pandas.DataFrame
        Total population or total vaccinated per vaccine per org type, for output type
        specified, in format required for csv input

    """

    # Apply filters
    df_filtered = filter_dataframe(df, org_type, filter_condition, ts_years)

    # Aggregate the data by the required variables
    df_filtered = (df_filtered.groupby(breakdowns)[[
        num_column, denom_column]].sum())
    df_filtered.reset_index(inplace=True)

    # Complete output specific adjustments to produce pop or vacc figures per org_type
    if output_type == "Population":
        # Select columns needed
        df_csv = df_filtered[breakdowns + [denom_column]].copy()

        # Add population labels based on vaccines specified in parameters.py
        for pop_label, vac_type in param.POPULATION_VACCINES.items():
            df_csv.loc[df_csv["Vac_Type"] == vac_type, "Vac_Type"] = pop_label

        # Filter for population rows
        df_csv = df_csv[df_csv["Vac_Type"].str.endswith("Eligible_Pop")]

    elif output_type == "Vaccinated":
        # Select columns needed
        df_csv = df_filtered[breakdowns + [num_column]].copy()

    # Apply sort on if applicable
    if sort_on is not None:
        df_csv = sort_for_output(df_csv, sort_on, [])

    # Set index
    df_csv = df_csv.set_index(breakdowns)

    # Apply any column renaming
    if column_rename is not None:
        df_csv = df_csv.rename(columns=column_rename)
        df_csv.index = df_csv.index.set_names(
            [column_rename.get(name, name) for name in df_csv.index.names])

    return df_csv


def create_output_dashboard_data(df, output_type, org_type, breakdowns, sort_on,
                                 column_rename, filter_condition, population_vaccines,
                                 ts_years=1,
                                 num_column="Number_Vaccinated",
                                 denom_column="Number_Population"):
    """
    Creates data output in format required for use by the Power BI dashboard,
    with population and coverage in one value column, summed and grouped based
    on the rows and org_type provided

    Parameters
    ----------
    df : pandas.DataFrame
    output_type : str
        Used to determine the org level of the output and set org codes and names
        not found in the asset e.g. for UK level data
        Valid values are defined in the function
    org_type : str
        Determines which of the pre-defined org types will be reported on.
    breakdowns : list[str]
        Variable name(s) to group the data by (e.g. regions)
    sort_on: list[str]
        List of columns names to sort on (ascending).
    column_rename : dict
        Optional dictionary for renaming of columns from the data source version
        to output requirement.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some tables. It may consist of one or more filters of the
        dataframe variables.
    population_vaccines : dict
        Set which vaccine populations to use when defining eligible population
        for each child age
        e.g. {"12m_Eligible_Pop": "DTaP_IPV_Hib_HepB_12m"}
    ts_years: int
        Number of years to be used in the time series.
        Default is 1.
    num_column: str
        Name of the column that holds the measure (coverage) numerator data
    denom_column: str
        Name of the column that holds the measure (coverage) denominator data

    Returns
    -------
    df_dash : pandas.DataFrame
        Population and coverage data, for output type specified,
        in format required for dashboard input

    Raises
    ------
    ValueError
        If an invalid output_type is provided (valid values are defined in function)
    """
    # Check valid output type has been supplied
    valid_output_types = ["UK", "National", "Other nations", "Region", "LA"]
    helpers.validate_value_with_list("create_output_dashboard output_type",
                                     output_type, valid_output_types)

    # Apply standard and optional filters to dataframe
    df_filtered = filter_dataframe(df, org_type, filter_condition, ts_years)

    # Update org code and name for UK and national data before grouping
    if output_type == "UK":
        df_filtered["Org_Code"] = "K02000001"
        df_filtered["Org_Name"] = "United Kingdom"
    if output_type == "National":
        df_filtered["Org_Code"] = "E92000001"
        df_filtered["Org_Name"] = "England"

    # Add org level column based on input
    if output_type in ["National", "Other nations"]:
        df_filtered["Org_Level"] = "Country"
    else:
        df_filtered["Org_Level"] = output_type

    # Aggregate the data by the required variables
    df_agg = (df_filtered.groupby(breakdowns)[[num_column, denom_column]]
              .sum())

    df_agg.reset_index(inplace=True)

    # Calculate coverage
    df_agg = helpers.add_percent_or_rate(df_agg,
                                         "Coverage",
                                         num_column,
                                         denom_column,
                                         multiplier=100)

    # Unpivot data so one column of values (population and coverage)
    df_dash = pd.melt(df_agg,
                      id_vars=breakdowns,
                      value_vars=["Number_Population", "Coverage"],
                      value_name="Value"
                      )

    if "Vac_Type" in df_dash.columns or "Vac_Type" in df_dash.index.names:
        # Add eligible population labels for main vaccinations set in parameters.py
        for pop_label, vac_type in population_vaccines.items():
            df_dash.loc[(df_dash["Vac_Type"] == vac_type) &
                        (df_dash["variable"] == "Number_Population"),
                        "Vac_Type"] = pop_label

        # Filter out any population fields that don't have an eligible pop label
        df_dash = df_dash[(df_dash["variable"] == "Coverage") |
                          (
                              (df_dash["variable"] == "Number_Population") &
                              (df_dash["Vac_Type"].str.endswith("Eligible_Pop"))
        )]

    # Select columns for output
    df_dash = df_dash[breakdowns + ["Value"]]

    # Apply sort on if applicable
    if sort_on is not None:
        df_dash = sort_for_output(df_dash, sort_on, [])

    # Set the index based on breakdowns
    df_dash.set_index(breakdowns, inplace=True)

    # Rename the user selected columns as defined in column_rename dictionary
    # Will update column names even if they're in the index
    if column_rename is not None:
        df_dash = df_dash.rename(columns=column_rename)
        df_dash.index = df_dash.index.set_names(
            [column_rename.get(name, name) for name in df_dash.index.names])

    return df_dash


def output_specific_updates(df, name):
    """
    This checks the output name and applies any transformations/updates that
    are specific to a particular output(s), that are not covered by the general
    functions.

    Parameters
    ----------
    df : pandas.DataFrame
    name: str
        Name of output. This will be the worksheet name for Excel outputs and
        the filename for csv outputs.

    Returns
    -------
    df : pandas.DataFrame
    """
    # If vaccine status column outputted in index, move to end
    # Get list of all columns in index
    index_cols = list(df.index.names)

    if "Vaccine_Status" in index_cols:
        # Create new index without vaccine status
        new_index = index_cols
        new_index.remove("Vaccine_Status")

        # Reset and then apply new index
        df.reset_index(inplace=True)
        df = df.set_index(new_index)

        # Move vaccine status to end
        # (.pop removes the column from df, then returns it to be added to the end)
        df = pd.concat([df, df.pop("Vaccine_Status")], axis=1)

    if name == "Table 1":
        # Inserts new columns with a colon (:) for retired vaccines
        df.insert(2, "DTaP/IPV/Hib", ":")
        df.insert(3, "MenC", ":")
        df.insert(5, "PCV", ":")

    if name == "Table 2":
        # Inserts new columns with a colon (:) for retired vaccines
        df.insert(2, "DTaP/IPV/Hib", ":")
        df.insert(3, "MenC", ":")

    if name == "Table 3":
        # Adds new column at end with a colon (:) for retired Hib vaccine
        df["Hib"] = ":"

    if name in ["Table 11b", "Table 11c"]:
        # Apply suppression
        df = apply_hepb_suppression(df, "Population", "Vaccinated", "Coverage")

        # Update HepB data values to not available symbol (specified in parameters.py)
        # where vaccine status is 'Full data not available'
        df.loc[df["Vaccine_Status"] == "Full data not available",
               ["Population", "Vaccinated", "Coverage"]] = param.NOT_AVAILABLE

        # Where no HepB data submitted, replace values with 'not available' symbol,
        # and add status of 'Full data not available'
        df.loc[df["Vaccine_Status"].isnull(),
               df.columns] = param.NOT_AVAILABLE

        df.loc[df["Vaccine_Status"] == param.NOT_AVAILABLE,
               "Vaccine_Status"] = "Full data not available"

    if name in ["DTaP_12m_TSeries", "DTaP_24m_TSeries"]:
        # Inserts new column with WHO coverage target
        df.insert(0, "WHO Target", 95)

    if name in ["DTaP_5yr_TSeries",
                "DTaP_IPV_5yr_TSeries",
                "MMR_24m_TSeries",
                "MMR1_5yr_TSeries",
                "MMR2_5yr_TSeries",
                "PCV_12m_24m_TSeries",
                "Hib_MenC_24m_TSeries",
                "Hib_MenC_5y_TSeries",
                "Rota_12m_TSeries"
                ]:
        # Inserts new column with WHO coverage target
        df.insert(1, "WHO Target", 95)

    if name == "childhood_vaccination_map_data":
        # Insert a new column called source
        df.insert(0, "Source", "Perc_Vaccinated")

    if name in ["childhood-vaccination-la-num-denom"]:
        # Replace grouped LAs larger LA name with combined name
        df = df.rename(index={"Leicestershire": "Leicestershire and Rutland",
                              "Hackney": "Hackney and City of London",
                              "Cornwall": "Cornwall and Isles of Scilly"})

        # Sort combined output
        df.sort_values(by=["Parent_Org_Code", "Org_Name", "Child_Age", "Indicator"],
                       inplace=True)

    if name in ["childhood-vaccination-table-11b-11c"]:
        # Set the names of the 12 and 24m measure columns to which suppression
        # will be applied.
        cols_12m = ["HepB_12m_Population",
                    "HepB_12m_Vaccinated",
                    "HepB_12m_Coverage"]

        cols_24m = ["HepB_24m_Population",
                    "HepB_24m_Vaccinated",
                    "HepB_24m_Coverage"]

        # Create a 12m hepb only dataframe and apply suppression
        df_12m = df.drop(cols_24m, axis=1)
        df_12m = apply_hepb_suppression(df_12m, *cols_12m)

        # Create a 24m hepb only dataframe and apply suppression
        df_24m = df.drop(cols_12m, axis=1)
        df_24m = apply_hepb_suppression(df_24m, *cols_24m)

        # Rejoin the 12 month and 24 month data
        df = pd.concat([df_12m, df_24m], axis=1)

    if name == "DashboardData":
        # Sort data for current year before appending to existing data
        df.sort_values(by=["VacCode", "OrgType", "OrgCode"],
                       inplace=True)

    if name == "childhood-vaccination-dashboard-data":
        # Sort combined data for all years
        df.sort_values(by=["Year", "VacCode", "OrgType", "OrgCode"],
                       inplace=True)

    if name == "InternalDashboardData":
        # Sort combined data for all years
        df.sort_values(by=["FinancialYear", "Vac_Type", "Org_Level",
                           "Org_Code"], inplace=True)

    return df
