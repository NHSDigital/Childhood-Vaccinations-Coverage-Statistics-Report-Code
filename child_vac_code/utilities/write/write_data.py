import pandas as pd
import xlwings as xw
import child_vac_code.parameters as param
from child_vac_code.utilities import helpers, processing
from child_vac_code.utilities.write import write_format
import logging


def merge_existing_dashboard_data(df, output_path, sheetname):
    """
    For the dashboard data, the new output is merged (or replaces if that
    year already exists) with existing time series data. This function reads
    in the existing data and adds the new data.

    Parameters
    ----------
    df : pandas.DataFrame
    output_path : path
        Filepath of the Excel file that contains the existing dashboard data,
        and where the new data will be added.
    sheetname : str
        Name of the Excel worksheet that contains the existing dashboard data.

    Returns
    -------
    None
    """
    logging.info("Merging new with existing dashboard data")

    # Import the existing data from the relevant worksheet in the dashboard file
    df_existing = pd.read_excel(output_path, sheet_name=sheetname)

    # Get current index columns
    current_index = df.index.names

    # Reset index
    df.reset_index(inplace=True)

    # Set fyear based on financial year start in parameters.py
    fyear = helpers.fyearstart_to_fyear(param.FYEAR_START)

    # Remove any existing data for the current reporting year
    df_existing = df_existing[df_existing["Year"] != fyear]

    # Join the new data with the existing data
    df_merged = pd.concat([df_existing, df], ignore_index=True)

    # Set index back to original columns in current data
    df_merged.set_index(current_index, inplace=True)

    return df_merged


def write_to_excel_static(df, output_path, sheetname, write_cell,
                          include_row_labels=False, empty_cols=None):
    """
    Write data to an excel template. Assumes the table length remains constant.

    Parameters
    ----------
    df : pandas.DataFrame
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    write_cell: str
        identifies the cell location in the Excel worksheet where the data
        will be pasted (top left of data)
    include_row_labels: bool
        Determines if the row labels will be written.
    empty_cols: list[str]
        A list of letters representing any empty (section seperator) excel
        columns in the worksheet. Empty columns will be inserted into the
        dataframe in these positions. Default is None.

    Returns
    -------
    None
    """

    logging.info("Writing data to specified output file")

    # If row labels are required then reset the index so that they are included
    # when writing values (assumes index contains row labels)
    if include_row_labels:
        df.reset_index(inplace=True)

    # Add empty columns where present in target Excel worksheet
    if empty_cols is not None:
        df = write_format.insert_empty_columns(df, empty_cols, write_cell)

    # Load the template and select the required table sheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # write to the specified cell
    sht.range(write_cell).value = df.values


def write_to_excel_variable(df, output_path, sheetname, write_cell,
                            include_row_labels=False, empty_cols=None):
    """
    Write data to an excel template. Can accommodate dataframes where the
    number of rows may change e.g. LA data where the number of LAs may change
    each year.

    Parameters
    ----------
    df : pandas.DataFrame
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    write_cell: str
        identifies the cell location in the Excel worksheet where the data
        will be pasted (top left of data)
        This should be the first cell in the master file where the variable
        data currently exists as it also determines which row to delete first
        e.g. for LAs would be the first cell of the first row of LA data
    include_row_labels: bool
        Determines if the row labels will be written.
    empty_cols: list[str]
        A list of letters representing any empty (section separator) excel
        columns in the worksheet. Empty columns will be inserted into the
        dataframe in these positions. Default is None.
    Returns
    -------
    None
    """
    logging.info(f"Writing data to {sheetname}")

    # Load the Excel output file
    wb = xw.Book(output_path)

    # Check that the provided sheetname exists in the workbook
    sheetname_valid = [sht.name for sht in wb.sheets]
    helpers.validate_value_with_list("Excel sheet name",
                                     sheetname,
                                     sheetname_valid)
    # Select the required sheet
    sht = wb.sheets[sheetname]
    sht.select()

    # For the published time series dashboard data, existing data in output file
    # is merged onto current data, to preserve historical values
    db_ts_sheets = ["DashboardData"]

    if sheetname in db_ts_sheets:
        df = merge_existing_dashboard_data(df, output_path, sheetname)

    # If row labels are required then reset the index so that they are included
    # when writing values (assumes index contains row labels)
    if include_row_labels:
        df.reset_index(inplace=True)

    # Add empty columns where present in target Excel worksheet
    if empty_cols is not None:
        df = write_format.insert_empty_columns(df, empty_cols, write_cell)

    # Get Excel row number of write cell
    firstrownum = helpers.excel_cell_to_row_num(write_cell)

    # Get Excel row number of last row of existing data
    lastrownum_current = sht.range(write_cell).end('down').row

    # Clear all existing data rows from write_cell to end of data
    delete_rows = str(firstrownum) + ":" + str(lastrownum_current)
    sht.range(delete_rows).delete()

    # Count number of rows in dataframe
    df_rowcount = len(df)

    # Create range for new set of rows and insert into sheet
    lastrownnum_new = firstrownum + df_rowcount - 1
    df_rowsrange = str(firstrownum) + ":" + str(lastrownnum_new)

    sht.range(df_rowsrange).insert(shift='down')

    # Write dataframe to the Excel sheet starting at the write_cell reference
    sht.range(write_cell).value = df.values


def write_csv(df, output_path, output_name, year, include_index=True):
    """
    Writes a dataframe to a csv

    Parameters
    ----------
    df :pandas.DataFrame
    output_path: Path
        Folder path where output will be written.
    output_name: str
        Name to be asssigned to output file name.
    year: str
        Represents the reporting period covered by the part of the
        process being run. Used in the filename if output isn't saved
        in the templates folder.
    include_index: bool
        Determines if the index (row names) will be written to the csv.

        Default is True

    Returns
    -------
    .csv file

    """
    # For the dashboard csv to be published, merge current year with existing data
    # in dashboard file
    if output_name in ["childhood-vaccination-dashboard-data"]:
        dashboard_file_path = param.DASHBOARD_TEMPLATE
        sheetname = "DashboardData"
        df = merge_existing_dashboard_data(df, dashboard_file_path, sheetname)

    # Set full file path / name
    # If csv is being outputted to the templates folder, then don't add
    # year to name
    if output_path == param.TEMPLATE_DIR:
        file_name = output_name + ".csv"
    else:
        file_name = output_name + "-" + year + ".csv"

    save_path = output_path / file_name

    logging.info(f"Writing data to {file_name}")

    # Save dataframe to csv
    df.to_csv(save_path, index=include_index)


def select_write_type(df, write_type, output_path, output_name,
                      write_cell, year, include_row_labels=False,
                      empty_cols=None):
    """
    Determines which type of write function is needed and performs that
    function.

    Parameters
    ----------
    df :pandas.DataFrame
    write_type: str
        Determines the method of writing the output.
    output_path: Path
        Path where output will be written. Full file path if writing to Excel
        or the folder path if writing to a csv.
    output_name: str
        Name of the worksheet to be written to (for Excel) or to be assigned
        as the name of the output file (for csv's).
    write_cell: str
        identifies the cell location in the Excel worksheet where the data
        will be pasted (top left of data). Not required if the write_type is
        csv.
    year: str
        Reporting period covered by the part of the process being run.
    include_row_labels: bool
        Determines if the row labels will be written.
    empty_cols: list[str]
        A list of letters representing any empty (section separator) excel
        columns in the worksheet. Empty columns will be inserted into the
        dataframe in these positions. Not required if the write_type is
        csv.

    Returns
    -------
    None

    """
    # Check for invalid write_type argument
    valid_values = ["csv", "excel_static", "excel_variable", "excel_add_year"]
    helpers.validate_value_with_list("write_type", write_type, valid_values)

    # If write_type is csv, then write the output to a csv
    if write_type == "csv":
        write_csv(df, output_path, output_name, year)

    # If write_type is excel_variable, then use the variable write to excel method
    elif write_type == "excel_variable":
        write_to_excel_variable(df, output_path, output_name,
                                write_cell, include_row_labels, empty_cols)
    # Otherwise use the static write excel option
    else:
        write_to_excel_static(df, output_path, output_name,
                              write_cell, include_row_labels, empty_cols)


def write_outputs(df, output_args, output_path, year):
    """
    Processes and writes the data for each function to the output location
    as defined by parameters taken from the output_args dictionary.

    Parameters
    ----------
    df :pandas.DataFrame
    output_args: dictionary
        Provides all the required arguments needed to run and write each
        output: name, write_type, write_cell, empty_cols and the function(s)
        that create the data.
    output_path: Path
        Path where output will be written. Full file path if writing to Excel
        or the folder path if writing to a csv.
    year: str
        Represents the reporting period covered by the part of the
        process being run.

    Returns
    -------
    None

    """
    # For each item in the output_args dictionary
    for output in output_args:
        # Extract all the required arguments from the output_args dictionary
        # Some arguments are not needed if the write_type is csv
        name = output["name"]
        write_type = output["write_type"]

        if write_type == "csv":
            write_cell = None
            include_row_labels = None  # Not used for csv writing as outputted by default
            empty_cols = None
            year_check_cell = None
            years_as_rows = None
        elif write_type == "excel_add_year":
            write_cell = None
            include_row_labels = True
            empty_cols = output["empty_cols"]
            year_check_cell = output["year_check_cell"]
            years_as_rows = True
        else:
            write_cell = output["write_cell"]
            include_row_labels = output["include_row_labels"]
            empty_cols = output["empty_cols"]
            year_check_cell = output["year_check_cell"]
            years_as_rows = output["years_as_rows"]

        # Run the function(s) in the dictionary item(s) beginning with 'contents'.
        # Where there are multiple functions in the contents for one output,
        # the returned dataframes are concatenated. For unmatched columns null
        # values will be created.
        # Where there are multiple contents keys, the outputs will be concatenated
        # along columns (same identical length is assumed on contents set up).
        # List to store the different outputs to join
        total_dfs = []
        # Check the output dictionary for keys starting with contents
        keys = list(output.keys())
        content_keys = [key for key in keys if key.startswith("contents")]
        for content_key in content_keys:
            logging.info(f"Running {content_key} for {name}")
            df_content = pd.concat([content(df) for content in output[content_key]])
            total_dfs.append(df_content)

        # Where there was more than one contents key then these are joined
        # along columns (on index).
        df_output = pd.concat(total_dfs, axis=1)

        # Perform any updates to the dataframe for specific outputs
        df_output = processing.output_specific_updates(df_output, name)

        # Set not available for whole row when no data submitted and more
        # than one column in row
        if len(df_output.columns) > 1:
            df_output.loc[df_output[df_output.columns].isnull().all(axis="columns"),
                          df_output.columns] = param.NOT_AVAILABLE

        # Replace remaining nulls with the required not_applicable replacement
        # value.
        df_final = df_output.fillna(param.NOT_APPLICABLE)

        # If a target output contains fixed length time series data (year_check_cell
        # will be populated) then check if the time series in Excel needs preparing
        # (moving along one year). Not applied if write_type is excel_add_year.
        if (year_check_cell is not None) & (write_type != "excel_add_year"):
            write_format.check_latest_year(output_path, name,
                                            year_check_cell, year,
                                            years_as_rows)

        # If the write type is excel_add_year then check if a new row needs
        # adding to the time series, and return the required write cell
        if write_type == "excel_add_year":
            write_cell = write_format.check_add_year(output_path, name,
                                                      year_check_cell, year)

        # Write the output as per the selected write type
        select_write_type(df_final, write_type, output_path,
                          name, write_cell, year, include_row_labels,
                          empty_cols)
