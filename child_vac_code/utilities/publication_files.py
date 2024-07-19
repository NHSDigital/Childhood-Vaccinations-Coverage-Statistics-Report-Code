import xlwings as xw
import xlsxwriter
import win32com.client as win32
import child_vac_code.parameters as param
import datetime
import child_vac_code.utilities.helpers as helpers
import logging


def define_labels(tag):
    """
    Creates label strings based on tag and year inputs. Used to populated labels
    in external files where the cells contain the tags defined in this function.

    Parameters
    ----------
    tag : str
        tag that is used to lookup the required label
    Returns
    -------
    label: str
    """
    # Set the current year
    year_current = str(datetime.date.today().year)

    # Import the year start value from the parameters
    fyear_start = param.FYEAR_START
    fyear = helpers.fyearstart_to_fyear(fyear_start)

    # Create all the required year ranges
    year_range_11 = helpers.get_year_range_fy(fyear, 11)
    start_fyear_11 = year_range_11[0]

    # Set default label for if Excel tag does not match any of the tags below
    label = "invalid_tag"

    # Define the titles/headers based on the tag required
    if tag == "subtitle_year":
        label = "England, " + fyear
    if tag == "subtitle_timeseries_11":
        label = "England, " + start_fyear_11 + " to " + fyear

    # Define the copyright labels based on the tag required
    if tag == "copyright_ons":
        label = f"""Copyright © {year_current}, re-used with the permission of The Office
        for National Statistics."""
    if tag == "copyright_nhse":
        label = f"Copyright © {year_current}, NHS England"

    return label


def apply_labels(sheet, cells):
    """
    Uses xlwings to apply labels to the specified Excel worksheet based on tags
    established in the define_labels function.

    Parameters
    ----------
    sheet : Sheet
        xlwings worksheet object
    cells : Range
        xlwings cell range object
    Returns
    -------
        None
    """

    # For each cell in the check range:
    for cell in cells:
        check = str(sheet.range(cell).value)
        if check == "":
            pass
        # Add the labels to each sheet based on the tags in the template file
        if check.startswith("tag_"):
            tag = check[4:]
            sheet.range(cell).value = define_labels(tag)


def remove_markers(sheet, cells,
                   markers=["mark_last_row", "mark_last_col"]):
    """
    Uses xlwings to remove markers from the specified Excel worksheet

    Parameters
    ----------
    sheet : Sheet
        xlwings worksheet object
    cells : Range
        xlwings cell range object
    markers : list[str]
        list of strings to be removed from the worksheet
    Returns
    -------
        None
    """

    # For each cell in the check range:
    for cell in cells:
        check = str(sheet.range(cell).value)
        # Remove the time series markers used to identify data ranges
        if check in markers:
            sheet.range(cell).value = ""


def save_tables(source_file):
    """
    Save updated table template to the final data tables folder

    Parameters
    ----------
    source_file : path
        filepath of the Excel file that contains the tables to be saved.
    Returns
    -------
        None
    """

    # Set the publication year
    year = str(datetime.date.today().year)

    # Select the template file to save
    xw.App()
    wb = xw.books.open(source_file)

    # Select the save name and last column of the table range depending on
    # which source file is being saved.
    if source_file == param.TABLE_TEMPLATE:
        save_name = "childhood-vaccinations-eng-" + year + "-tab.xlsx"
    else:
        raise ValueError(f"""The file name {source_file} was not recognised
                         when attempting to write the publication tables""")

    logging.info(f"Saving final publication tables to {save_name}")

    # Save the tables to the publication folder, named as per the report year
    savepath = param.TAB_DIR / save_name
    wb.save(savepath)

    # Remove any worksheets that are not published based on the parameter input list
    delete_sheets = param.TABLES_REMOVE
    sheets_in_file = [sht.name for sht in wb.sheets]
    for sheet in delete_sheets:
        if sheet in sheets_in_file:
            sheet_to_delete = wb.sheets[sheet]
            sheet_to_delete.delete()

    # Apply other required updates to each worksheet
    for sheet in wb.sheets:
        sheet.select()
        # Define the cell range to be checked for each of the worksheets
        # The extent of column range is set to P
        # The maximum rows set to check is 200
        endrow = sheet.range('A200').end('up').last_cell.row+1
        check_range = "A1:C" + str(endrow)
        cells = sheet.range(check_range)

        # Apply labels to the worksheet
        apply_labels(sheet, cells)
        # Remove any time series markers from the worksheet
        remove_markers(sheet, cells)

    # Return to the title sheet, and re-save
    sht = wb.sheets["Contents"]
    sht.select()
    wb.save()
    xw.apps.active.api.Quit()


def save_chart_files(source_file):
    """
    Save each tab in the chart data template as an individual Excel file ready
    for loading to CMS.

    Parameters
    ----------
    source_file : path
        filepath of the Excel file that contains the chart data.
    Returns
    -------
        None
    """

    # Select the chart template file
    xw.App()
    wb = xw.books.open(source_file)

    # Set the output location for saving the final files
    chart_dir = param.CHART_DIR

    # Select the prefix for the filename
    save_prefix = "child_vacc_"

    # For each sheet in the file, remove any markers and save the as an
    # individual Excel file in the specified output folder.
    for sheet in wb.sheets:
        # Check the number of rows and columns covered by the data, extended to
        # ensure any markers are included (max of range set to P30)
        sheet = wb.sheets[sheet]
        endrow = sheet.range('A30').end('up').last_cell.row+1
        endcol = sheet.range('P1').end('left').last_cell.column+1
        endcol = xlsxwriter.utility.xl_col_to_name(endcol)
        # Define the cell range to be checked for each of the worksheets
        check_range = "A1:" + str(endcol) + str(endrow)
        cells = sheet.range(check_range)
        # Remove any time series markers from the worksheet
        remove_markers(sheet, cells)

        # Select the file save name based on the prefix and worksheet name
        save_name = save_prefix + sheet.name + ".xlsx"

        logging.info(f"Saving final publication chart to {save_name}")

        # Create an empty workbook
        new_wb = xw.Book()
        # Copy across the sheet containing the data and remove the default empty sheet
        sheet.copy(after=new_wb.sheets[0])
        new_wb.sheets["Sheet1"].delete()

        # Save the file to the publication folder, and close the file
        save_path = chart_dir / save_name
        new_wb.save(save_path)
        new_wb.close()

    # Close the chart template without saving (to retain markers)
    wb.close()
    xw.apps.active.api.Quit()
