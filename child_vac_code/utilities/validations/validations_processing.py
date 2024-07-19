from child_vac_code.utilities import helpers
import child_vac_code.parameters as param
import logging

"""
This module contains all the user defined inputs for each validation used by
functions in processing.py
"""


def check_flu_organisations(df):
    """
    Checks the flu data for nulls where it has been joined to organisation
    reference data, and returns an error if any are found (indicating invalid
    codes in the flu data). Outputs the data row to an external file for each error.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the data to check

    Raises
    ------
    warning
        Message to warn users of invalid rows, and where the details have been
        exported to.

    Returns
    -------
    None - invalid rows are outputted to .csv file

    """

    logging.info("Checking for missing organisational details in the flu data")

    # Set inputs for check
    val_type = "warning"
    invalid_condition = "Org_Name.isnull()"
    val_groups = None
    filename = "flu_mismatched_org_codes.csv"
    output_path = param.VALID_DIR / filename
    invalid_message = f"""
    There are org codes in the flu data which don't align with the Org Ref data
    and so will not be included in the outputs.

    The list of these organisations has been exported to {filename} in the
    Validations folders
    """

    # Run check - invalid rows are outputted to Validations folder
    helpers.invalid_row_check(df, val_type, invalid_condition, val_groups,
                              output_path, invalid_message)


def flu_invalid_source_year(df, fyear):
    """
    Check for rows in flu source data where the year does not match the
    financial year being processed

    If any are found, the process is aborted and invalid rows outputted
    to .csv file

    Parameters
    ----------
    df : pandas.DataFrame
        Containing source data to be checked
    fyear : str
        Expected financial year of extract (yyyy-yy) generated based on the
        financial year start specified in parameters file

    Raises
    ------
    ValueError
        Error message after process aborts indicating invalid rows, and
        where the details have been exported to.

    Returns
    -------
    None - invalid rows are outputted to .csv file

    """

    logging.info("Checking for invalid source year in the flu data")

    # Set inputs for check
    val_type = "error"
    invalid_condition = "Year != @fyear"
    val_groups = None
    filename = "flu_invalid_source_year.csv"
    output_path = param.VALID_DIR / filename
    invalid_message = f"""
    The flu input file contains data for years that do not match the
    financial year being processed ({fyear}).

    The first invalid row has been outputted to {filename} in the validations
    folder for review. Please ensure all flu file data are for the same period,
    then run the process again.
    """
    output_limit = 1

    # Run check - invalid rows are outputted to Validations folder
    helpers.invalid_row_check(df, val_type, invalid_condition, val_groups,
                              output_path, invalid_message, output_limit, fyear)


def vaccine_status_updates_invalid(df, df_status_updates):
    """
    Check for invalid rows in vaccine status updates file for the
    financial year being processed (where a match in the source data on
    combination of org code and vac type could not be found)

    If any invalid updates found, a warning message is raised and the invalid
    status updates outputted to .csv file

    Parameters
    ----------
    df : pandas.DataFrame
        Containing source data to check against
    df_status_updates : pandas.DataFrame
        Containing vaccine status updates source data to be checked

    Raises
    ------
    warning
        Warning message indicating invalid rows have been found, and
        where the details have been exported to.

    Returns
    -------
    None - invalid rows are outputted to .csv file

    """
    logging.info("Checking for invalid vaccine status updates in ref file")

    # Set fyear value based on financial year start in parameters.py
    fyear = helpers.fyearstart_to_fyear(param.FYEAR_START)

    # Filter status updates for year being processed
    df_status_updates = df_status_updates[df_status_updates["FinancialYear"]
                                          == fyear]

    # Join source data onto status updates data
    df_comb = df_status_updates.merge(df, how="left", on=["FinancialYear",
                                                          "Org_Code",
                                                          "Vac_Type"])

    # Filter for columns needed for check
    df_comb = df_comb[["FinancialYear", "Org_Code", "Vac_Type", "Org_Name"]]

    # Set inputs for check
    df = df_comb
    val_type = "warning"
    invalid_condition = "Org_Name.isnull()"
    val_groups = None
    filename = "vaccine_status_updates_invalid.csv"
    output_path = param.VALID_DIR / filename
    invalid_message = f"""
    The vaccine status updates input file data contains invalid rows for the
    year being processed ({fyear}).

    Details of invalid rows have been outputted to {filename} in the validations
    folder for review.

    Please ensure all vaccine status updates are for org codes and
    vaccination types that are in the source data for the year being processed.
    """
    # Run check - invalid rows are outputted to Validations folder
    helpers.invalid_row_check(df, val_type, invalid_condition, val_groups,
                              output_path, invalid_message)
