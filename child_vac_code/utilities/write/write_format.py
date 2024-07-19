import xlwings as xw
import xlsxwriter
from child_vac_code.utilities import helpers


def check_latest_year(output_path, sheetname,
                      year_check_cell, year,
                      years_as_rows=True):
    '''
    For tables with fixed length time series data, checks the target file to
    see if the time series needs moving along one year e.g. the latest year
    in an 11 year time series in the target table is 2019-20, but the data
    being processed is for 2020-21.
    If so then run the function that will do this (one of 2 options determined
    by whether the time series is written vertivally (as rows) or
    horizintally (as columns).

    Parameters
    ----------
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    year_check_cell: str
        This identifies the cell location in the Excel worksheet that contains
        the latest year value.
    year: str
        The current reporting year value that will be used to check if the
        Excel time series requires moving along.
    years_as_rows: bool
        Set to True if years in a time series output are arranged in rows (vertical).
        Set to False if years are arranged in columns (horizontal)
        or year_check_cell is None.


    Returns
    -------
    None
    '''
    # Select the active workbook and sheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # Check the year value in the year_check_cell (which should correspond with
    # the latest year that exists in the data table.
    latest_year = sht.range(year_check_cell).value

    # If the latest year in the table does not match the latest reporting year,
    # then the time series range will be moved back one column or row in Excel.
    if year != latest_year:
        if years_as_rows is True:
            adjust_timeseries_rows(output_path, sheetname,
                                   year_check_cell, year)
        else:
            adjust_timeseries_columns(output_path, sheetname,
                                      year_check_cell, year)

    return None


def check_add_year(output_path, sheetname,
                   ts_start_cell, year):
    '''
    For tables with variable length time series data, checks the target file to
    see if a new year row needs adding to the time series, and returns a cell
    value where the new data will be written. Assumes that years are in rows
    (single column).

    Parameters
    ----------
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    ts_start_cell: str
        This identifies the cell location in the Excel worksheet that contains
        the start of the time series.
    year: str
        The current reporting year value that will be used to check if a new
        year row needs adding.

    Returns
    -------
    None
    '''
    # Select the active workbook and sheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # Extract the column letter and equivalant number containing the time series
    # years from the Excel cell reference
    ts_col = ts_start_cell[0]
    ts_col_num = helpers.excel_cell_to_col_num(ts_start_cell)

    # Find the row that holds the last year value for the current time series
    last_row = sht.range(ts_start_cell).end('down').last_cell.row

    # Extract the latest year value from the current time series
    latest_year = sht.range(last_row, ts_col_num).value

    # If the latest year in the table does not match the latest reporting year,
    # then an extra row will be inserted into the table
    if year != latest_year:
        # Return the row below the latest year value and convert to string
        new_row = str(last_row + 1)
        # Insert a new row in that position
        sht.range(new_row + ":" + new_row).insert('down')
        # record new cell value as the write cell
        write_cell = ts_col + str(new_row)
    else:
        # If year already exists then record that cell as the write cell
        write_cell = ts_col + str(last_row)

    return write_cell


def adjust_timeseries_rows(output_path, sheetname, end_year_cell, year,
                           ts_length=11, mark_end_col="mark_last_col"):
    '''
    For tables with fixed length time series data in rows, moves the range of
    cell content up one row (overwriting data in the topmost row).
    The range is determined using the cell location of the end year of the
    currently written time series (end_year_cell), and a 'mark_col_end' marker
    placed in the Excel cell below the last content that is to be moved.
    The year value in the end_year_cell will also be updated with the
    reporting year that aligns with the new data being written.

    Parameters
    ----------
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    end_year_cell: str
        This identifies the cell location in the Excel worksheet that contains
        the last year value.
    year: str
        The current reporting year value that will be applied to the latest
        position for the time series labels.
    ts_length: int
        Length of time series. Default is 11 for this publication.
    tag_end_col: str
        Name of the tag that must be placed in the Excel table below the last
        cell of data in the range to be moved. Used to determine the last column
        in the range.
    Returns
    -------
    None
    '''
    # Select the active workbook and sheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # The time series range start row and range end column of the Excel
    #  range to be moved can be derived based on the year check cell.
    ts_end_row = helpers.excel_cell_to_row_num(end_year_cell)
    ts_start_row = ts_end_row - ts_length + 1
    ts_start_col = helpers.excel_cell_to_col_num(end_year_cell)

    # Using the markers that should be present in the Excel file, determine
    # the range end row
    ts_end_col = ts_start_col
    for col in range(ts_start_col, 20):
        if sht.range(ts_end_row + 1, col).value == mark_end_col:
            ts_end_col = col
            break

    # The start row used for the copy range is moved down one at this step
    # as the first time series row should be excluded from the copy range.
    ts_start_row_adj = ts_start_row + 1

    # Convert column numbers back to column letters for copy and paste step
    ts_start_col = xlsxwriter.utility.xl_col_to_name(ts_start_col - 1)
    ts_end_col = xlsxwriter.utility.xl_col_to_name(ts_end_col - 1)

    # Select the Excel range to copy, and copy it to the clipboard
    copy_range = (str(ts_start_col)
                  + str(ts_start_row_adj)
                  + ":"
                  + str(ts_end_col)
                  + str(ts_end_row))

    sht.range(copy_range).copy()

    # Select Excel the paste location and paste the copied data
    paste_cell = (str(ts_start_col)
                  + str(ts_start_row))

    sht.range(paste_cell).paste()

    # Update the end year label with the current reporting year
    sht.range(end_year_cell).value = year

    return None


def adjust_timeseries_columns(output_path, sheetname, end_year_cell, year,
                              ts_length=3, mark_end_row="mark_last_row"):
    '''
    For tables with fixed length time series data in columns, moves the range of
    cell content one column left (overwriting data in the leftmost column).
    The range is determined using the cell location of the end year of the
    currently written time series (end_year_cell), and a 'mark_last_row' marker
    placed in the Excel cell next to (to the right) of the last content that is
    to be moved. The year value in the end_year_cell will also be updated with the
    reporting year that aligns with the new data being written.

    Parameters
    ----------
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    end_year_cell: str
        This identifies the cell location in the Excel worksheet that contains
        the last year value.
    year: str
        The current reporting year value that will be applied to the latest
        position for the time series labels.
    ts_length: int
        Length of time series. Default is 3 for this publication.
    tag_end_col: str
        Name of the tag that must be placed in the Excel table to the right of
        the last cell of data in the range to be moved. Used to determine the
        last row in the range.
    Returns
    -------
    None
    '''
    # Select the active workbook and sheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # The time series range start row and range end column of the Excel
    # range to be moved can be derived based on the year check cell.
    ts_end_col = helpers.excel_cell_to_col_num(end_year_cell)
    ts_start_col = ts_end_col - ts_length + 1
    ts_start_row = helpers.excel_cell_to_row_num(end_year_cell)

    # Using the markers that should be present in the Excel file, determine
    # the range end row
    ts_end_row = ts_start_row
    for row in range(ts_start_row, 500):
        if sht.range(row, ts_end_col + 1).value == mark_end_row:
            ts_end_row = row
            break

    # The start column used for the copy range is moved along one at this step
    # as the first time series column should be excluded from the copy range.
    ts_start_col_adj = ts_start_col + 1

    # Convert column numbers back to column letters for copy and paste step
    ts_start_col = xlsxwriter.utility.xl_col_to_name(ts_start_col - 1)
    ts_start_col_adj = xlsxwriter.utility.xl_col_to_name(ts_start_col_adj - 1)
    ts_end_col = xlsxwriter.utility.xl_col_to_name(ts_end_col - 1)

    # Select the Excel range to copy, and copy it to the clipboard
    copy_range = (str(ts_start_col_adj)
                  + str(ts_start_row)
                  + ":"
                  + str(ts_end_col)
                  + str(ts_end_row))

    sht.range(copy_range).copy()

    # Select Excel the paste location and paste the copied data
    paste_cell = (str(ts_start_col)
                  + str(ts_start_row))

    sht.range(paste_cell).paste()

    # Update the end year label with the current reporting year
    sht.range(end_year_cell).value = year

    return None


def insert_empty_columns(df, empty_cols, write_cell):
    '''
    Inserts empty columns into the dataframe based on where any empty columns
    are located in Excel.
    When inserting columns the function exludes the index, so the index should
    only include columns that are not to be pasted into Excel.

    Parameters
    ----------
    df : pandas.DataFrame
    empty_cols: list[str]
        A list of letters representing any empty excel columns in the target
        worksheet.
        Default is None
    write_cell: str
        cell where the dataframe content will be writen to, used for reference
        when coverting the column letter to a dataframe column number.

    Returns
    -------
    df : pandas.DataFrame
    '''

    # For each Excel column letter, convert to a relative numeric dataframe position
    # and insert an empty column in the dataframe.
    # The function takes into account the starting column in Excel (base on write_cell)
    # as it's base (0)
    for col in empty_cols:
        col_num = helpers.excel_col_to_df_col(col, write_cell)
        col_name = "Empty_col_" + str(col_num)
        df.insert(col_num, col_name, "")

    return df
