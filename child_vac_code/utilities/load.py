import logging
import pandas as pd
import child_vac_code.parameters as param
import child_vac_code.utilities.data_connections as dbc
from child_vac_code.utilities import helpers

logger = logging.getLogger(__name__)


def import_asset_data(year_range: list = [param.FYEAR_START]):
    """
    This function will import data filtered by a given year_range
    (based on financial year start dates) from the asset SQL database.
    Uses the df_from_sql function

    Parameters
    ----------
    year_range: list
        The list of years to return
        defaults to returning FYEAR_START from parameters.py

    Returns
    -------
    pandas.DataFrame

    """
    logging.info("Importing childhood vaccinations data from the SQL asset")

    # Load our parameters
    server = param.SERVER
    database = param.DATABASE
    table = param.TABLE

    sql_folder = r"child_vac_code\sql_code"
    query_name = r"\query_asset.sql"

    with open(sql_folder + r"/" + query_name, "r") as sql_file:
        data = sql_file.read()

    data = data.replace("<YearRange>", "','".join(year_range))
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    return df


def import_org_ref_data(financial_year):
    """
    This function will import data from the corporate reference SQL database
    containing organisations that exist in the current reporting year (Upper
    and lower tier LA's, regions, ICBs and ICB regions)
    Uses the df_from_sql function

    Parameters
    ----------
    financial_year: str
        financial year for reporting (YYYY-YY)

    Returns
    -------
    pandas.DataFrame

    """
    logging.info("Importing organisation reference data")

    # Set server/database/table
    server = param.CORP_REF_SERVER
    database = param.CORP_REF_DATABASE
    table = param.ONS_ORG_TABLE

    # Extract required query parameters from financial year
    fy_start, fy_end = helpers.fyear_to_year_start_end(financial_year)

    sql_folder = r"child_vac_code\sql_code"
    query_name = r"\query_org_ref.sql"

    with open(sql_folder + r"/" + query_name, "r") as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file
    # are replaced with our user defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)
    data = data.replace("<FYStart>", str(fy_start))
    data = data.replace("<FYEnd>", str(fy_end))

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    # Remove any duplicate orgs keeping most recent version where duplicated
    df = df.sort_values(by=["Org_Code", "Open_date"], ascending=True)
    df = df.drop_duplicates(subset=["Org_Code"], keep="last")

    return df


def import_flu():
    """
    This function will import childhood flu data at LA level.

    If the source data does not contain an expected column, the process will abort with
    an error message detailing which columns are missing.

    Expected columns are defined below. Unrequired columns are dropped.

    Returns
    -------
    pandas.DataFrame

    """
    logging.info("Loading LA level flu data")

    # Import csv as a df
    file_path = param.FLU_LA
    df = pd.read_csv(file_path)

    # Specify columns needed and check they are in df
    expected_cols = ["Year",
                     "Local Authority code",
                     "All 2 year olds (combined): Patients registered",
                     "All 2 year olds (combined): Number vaccinated",
                     "All 3 year olds (combined): Patients registered",
                     "All 3 year olds (combined): Number vaccinated"
                     ]
    input_data = "input file childhood_vaccination_flu_la.csv"

    # Check that the columns are as expected
    helpers.expected_column_check(df, input_data, expected_cols)

    # Extract necessary cols only from csv
    df = df[expected_cols]

    # Convert counts to numeric
    for col in ["All 2 year olds (combined): Patients registered",
                "All 2 year olds (combined): Number vaccinated",
                "All 3 year olds (combined): Patients registered",
                "All 3 year olds (combined): Number vaccinated"]:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace(',', '')
            df[col] = df[col].astype('int64')

    return df


def import_vaccine_status_updates():
    """
    This function will import details of any organisations that need their
    vaccine status updating, from the referenced .csv file

    If the source data does not contain an expected column, the process will abort with
    an error message detailing which columns are missing.

    Expected columns are defined below.

    Returns
    -------
    pandas.DataFrame

    """
    logging.info("Loading vaccine status updates data")

    # Import csv as a df
    file_path = param.VACC_STATUS_UPDATES
    df = pd.read_csv(file_path)

    # Specify columns needed and check they are in df
    expected_cols = ["FinancialYear",
                     "Org_Code",
                     "Vac_Type",
                     ]

    input_data = "input file childhood_vaccination_status_updates.csv"

    # Check that the columns are as expected
    helpers.expected_column_check(df, input_data, expected_cols)

    return df


def import_raw_cover_data(fyear_start):
    """
    This function will import the data for the current reporting year
    from the COVER raw SQL table for the validations process
    Uses the df_from_sql function

    Returns
    -------
    pandas.DataFrame
        Containing the data imported from the raw SQL table

    """
    logging.info("Importing childhood vaccinations data from the SQL raw table")

    # Load our parameters
    server = param.SERVER
    database = param.DATABASE
    table = param.TABLE_RAW

    sql_folder = r"child_vac_code\sql_code"
    query_name = r"\query_raw.sql"

    with open(sql_folder + r"/" + query_name, "r") as sql_file:
        data = sql_file.read()

    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)
    data = data.replace("<FinancialYearStart>", fyear_start)

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    return df
