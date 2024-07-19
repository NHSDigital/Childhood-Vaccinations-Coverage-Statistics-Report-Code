import pandas as pd
import logging
from child_vac_code.utilities import helpers, load
import child_vac_code.parameters as param
import child_vac_code.utilities.validations.validations_processing as val_proc

logger = logging.getLogger(__name__)


def create_org_ref_data(fyear, combine_small_las=True):
    """
    Imports and makes updates to the organisation reference
    data needed for processing. Map the parent org codes in the corporate
    reference data to parent names. Adds organisation type.

    Parameters
    ----------
    fyear: str
        Financial year of extract (yyyy-yy)
    Returns
    -------
    df: pandas.DataFrame
        Dataframe containing LA organisation reference data with LA parent name
        and organisation type added.
    combine_small_las : bool
        Flags whether to combine small LAs into larger ones in output e.g.
        Rutland combining with Leicestershire
        Default is True (LAs are combined)

    """
    logging.info("Creating the organisation reference data")

    # Import from the corporate reference data
    df_org_ref = load.import_org_ref_data(fyear)

    # Extract the org code and org name from the reference data as a new dataframe
    df_orgs = df_org_ref[["Org_Code", "Org_Name"]].copy()
    # Rename org code column to parent org code
    df_orgs = df_orgs.rename(columns={"Org_Code": "Parent_Org_Code",
                                      "Org_Name": "Parent_Org_Name"})

    # Add parent names to parent codes in the original dataframe
    df_org_ref = pd.merge(df_org_ref, df_orgs, how="left", on="Parent_Org_Code")

    # Add organisation type and level
    df_org_ref = helpers.add_organisation_type(df_org_ref, "Org_Code")

    # For LA of residence tables, if combine_small_las is True,
    # drop the small LA's that are combined with larger neighbours for reporting.
    # Creates a list from the LA update dictionary in parameters that contains
    # details of the small LAs being combined and drops these from the dataframe
    if combine_small_las:
        df_la_update = pd.DataFrame(data=param.LA_UPDATE)
        small_las = df_la_update["From_code"].tolist()
        df_org_ref = df_org_ref[~df_org_ref["Org_Code"].isin(small_las)]

    # Default index values are reset here to support saving to feather
    return df_org_ref.reset_index(drop=True)


def update_small_las(df, column_code, column_name,
                     lookup=param.LA_UPDATE):
    """
    Updates small LA details to neighbouring LA details for non-
    disclosive purposes, using a dictionary of old to new org codes and names
    from the parameters file.
    As they sit in the same region, the parent details do not require updating.

    Parameters
    ----------
    df : pandas.DataFrame that includes an org code as a variable
    column_code : str
        Column name that holds the LA codes to be updated.
        Can be set to none if only the name requires updating.
    column_name : str
        Column name that holds the LA names to be updated.
        Can be set to none if only the code required updating.
    lookup: dict(str, list)
        Dictionary containing the original org codes and names.
        and corresponding replacement values.

    Returns
    -------
    df : pandas.DataFrame
        with the codes and names updated as per the values in the
        input dictionary.
    """
    logging.info("Updating small LA information")

    # Create a dataframe from the reference data input
    df_la_update = pd.DataFrame(data=lookup)

    # Create separate dictionaries for the org code and org name lookups
    df_code_update = dict(zip(df_la_update["From_code"],
                              df_la_update["To_code"]))
    df_name_update = dict(zip(df_la_update["From_name"],
                              df_la_update["To_name"]))

    # use the dictionaries to update the codes and names in the input dataframe
    if column_code is not None:
        df.replace({column_code: df_code_update}, inplace=True)
    if column_name is not None:
        df.replace({column_name: df_name_update}, inplace=True)

    return df


def map_org_code_to_name(df, df_org_ref, col_ref):
    """
    Function to map user specified org codes to its name in the
    corporate reference dataframe.

    Parameters
    ----------
    df: pandas.DataFrame
    df_org_ref: pandas.DataFrame
        corporate reference dataframe with the organisation codes and names
        (expects Org_Code and Org_Name in columns).
    col_ref: list(str)
        list of org code columns we want to find the organisation name for.
        Expects format to be 'orgtype'_code. e.g. LA_code, LA_parent_code

    Returns
    -------
    df : pandas.DataFrame
    """
    logging.info("Mapping organisations codes to names")

    # Filtering ref data for code and name cols
    df_org_ref = df_org_ref[["Org_Code", "Org_Name"]]

    # For each column in the list specified in the parameters.py file
    for i in col_ref:
        # Rename reference columns based on the column to be updated
        df_i = df_org_ref.rename(columns={"Org_Code": i})
        i_name = i.replace("Code", "")
        df_i = df_i.rename(columns={"Org_Name": i_name+"Name"})

        # Merge dataframe with ref data on the ref column name
        df = pd.merge(df, df_i, how="left", on=i)

    return df


def update_child_vac_data(df, df_org_ref, df_status_updates, combine_small_las=True):
    """
    Performs pre-processing on childhood vaccinations source data

    Parameters
    ----------
    df : pandas.DataFrame
        containing the childhood vaccinations source data
    df_org_ref: pandas.DataFrame
        corporate reference dataframe with the organisation codes and names
        (expects Org_Code and Org_Name in columns).
    df_status_updates : pandas.DataFrame
        data for org codes and vaccination types that need their vaccine
        status updating
    combine_small_las : bool
        Flags whether to combine small LAs into larger ones in output e.g.
        Rutland combining with Leicestershire
        Default is True (LAs are combined)

    Returns
    -------
    df : pandas.DataFrame
    """

    # Add a financial year column for reporting based on the existing financial
    # year start column
    df['FinancialYear'] = df['FinancialYearStart'].apply(helpers.fyearstart_to_fyear)

    if combine_small_las:
        # Combines small LAs with larger LAs according to combination in
        # the parameters.py file
        df = update_small_las(df,
                              "Org_Code",
                              "Org_Name")

    # Add parent names to org codes using org reference data
    df = map_org_code_to_name(df,
                              df_org_ref,
                              ["Parent_Org_Code"])

    # Add vaccine status column
    df = add_vaccine_status(df, df_status_updates)

    return df


def update_flu_vac_data(df, df_org_ref, fyear):
    """
    Performs pre-processing on childhood flu vaccinations source data

    Parameters
    ----------
    df : pandas.DataFrame containing the childhood flu vaccinations source
    data

    df_org_ref: pandas.DataFrame
        corporate reference dataframe with the organisation codes and names
        (expects Org_Code and Org_Name in columns).

    fyear : str
        Expected financial year of extract (yyyy-yy) generated based on the
        financial year start specified in parameters file

    Returns
    -------
    df : pandas.DataFrame
    """

    # Compare imported Year column with financial year generated by the process
    val_proc.flu_invalid_source_year(df, fyear)

    # Rename columns to match other data
    df = df.rename(columns={"Year": "FinancialYear", "Local Authority code": "Org_Code"})

    # Apply any LA code substitutions specified in parameters.py
    for oldcode, newcode in param.UPDATE_LA_CODE_FLU.items():
        df.loc[df["Org_Code"] == oldcode, "Org_Code"] = newcode

    # Join org_ref info to flu dataframe
    # Select columns from df_org_ref
    df_org_cols = df_org_ref[["Org_Code",
                              "Org_Name",
                              "Org_Type",
                              "Parent_Org_Code",
                              "Parent_Org_Name"]]
    df = pd.merge(df, df_org_cols, how="left", on="Org_Code")

    # Checks the merged flu data for nulls
    val_proc.check_flu_organisations(df)

    # Add data type
    df["Data_Type"] = "Actual"

    # Separate 2 year and 3 year flu vaccinations and rename vaccs/pop columns

    # Set common grouping columns
    grouping_cols = ["FinancialYear",
                     "Org_Code",
                     "Org_Name",
                     "Org_Type",
                     "Parent_Org_Code",
                     "Parent_Org_Name",
                     "Data_Type"]

    # Extract the 2 year old children dataframe and generalise the names of the
    # count columns
    df_2y = df[grouping_cols + ["All 2 year olds (combined): Patients registered",
                                "All 2 year olds (combined): Number vaccinated"]]
    df_2y = df_2y.rename(columns={
        "All 2 year olds (combined): Patients registered": "Number_Population",
        "All 2 year olds (combined): Number vaccinated": "Number_Vaccinated"})

    # Extract the 3 year old children dataframe and generalise the names of the
    # count columns
    df_3y = df[grouping_cols + ["All 3 year olds (combined): Patients registered",
                                "All 3 year olds (combined): Number vaccinated"]]
    df_3y = df_3y.rename(columns={
        "All 3 year olds (combined): Patients registered": "Number_Population",
        "All 3 year olds (combined): Number vaccinated": "Number_Vaccinated"})

    # Add column for age and vaccination type
    df_2y["Child_Age"] = "24m"
    df_2y["Vac_Type"] = "Flu_24m"
    df_3y["Child_Age"] = "3y"
    df_3y["Vac_Type"] = "Flu_3y"

    # Append 2 year and 3 year flu dataframes
    df = pd.concat([df_2y, df_3y])

    return df


def add_vaccine_status(df, df_status_updates):
    """
    Adds vaccine status column with default values, and then updates them
    as needed based on whether the related org and vac_type is in the
    status updates file

    If the vaccine status updates file contains a reference that is invalid
    (no matching org code/vac type in source data for the year being processed)
    then a warning message is raised, and invalid updates outputted
    to a file in the Validations folder

    Parameters
    ----------
    df : pandas.DataFrame
        Source data for vaccine status to be added to
    df_status_updates : pandas.DataFrame
        Reference data of orgs and vac types that need their status updating

    Returns
    -------
    df : pandas.DataFrame
        Source data with vaccine status added

    """
    logging.info("Adding vaccine status")

    # Check that data in vaccine status updates file is valid
    val_proc.vaccine_status_updates_invalid(df, df_status_updates)

    # Create dictionary of default status and related vaccination types
    status_default = {
        "Full data submitted": ["HepB_Group2_12m", "HepB_Group2_24m"],
    }

    # Add default vaccine status
    for status, vac_types in status_default.items():
        df.loc[(df["Vac_Type"].isin(vac_types)),
               "Vaccine_Status"] = status

    # Join on status updates data
    df = df.merge(df_status_updates,
                  how="left",
                  on=["FinancialYear", "Org_Code", "Vac_Type"],
                  indicator="Merge_Flag")

    # Create dictionary of new status and related vaccination types
    status_updates = {
        "Full data not available": ["HepB_Group2_12m", "HepB_Group2_24m"],
    }

    # Update status for orgs and vac types mentioned in updates file as below
    for status, vac_types in status_updates.items():
        df.loc[(df["Merge_Flag"] == "both") &
               (df["Vac_Type"].isin(vac_types)),
               "Vaccine_Status"] = status

    # Drop merge flag
    df.drop(columns=["Merge_Flag"], inplace=True)

    return df


def update_child_vac_data_raw(df, df_org_ref):
    """
    Performs pre-processing on the childhood vaccinations raw data

    Parameters
    ----------
    df: pandas.DataFrame
        containing the raw childhood vaccinations COVER source data.

    df_org_ref: pandas.DataFrame
        corporate reference dataframe with the organisation codes and names
        (expects Org_Code and Org_Name in columns).

    Returns
    -------
    df: pandas.DataFrame
        containing the raw COVER source data with pre-processing applied
    """

    # Add financial year
    df["FinancialYear"] = df["FinancialYearStart"].apply(helpers.fyearstart_to_fyear)

    # Join corporate ref data org details onto raw data
    df_orgs = df_org_ref[["Org_Code", "Org_Name", "Parent_Org_Code",
                          "Parent_Org_Name"]].copy()
    df = pd.merge(df, df_orgs, how="left", on="Org_Code")

    # For other countries, use submitted name and code
    df.loc[df["Org_Type"] == "NAT", "Org_Name"] = df["Org_Name_Sub"]
    df.loc[df["Org_Type"] == "NAT", "Parent_Org_Code"] = df["Org_Code"]
    df.loc[df["Org_Type"] == "NAT", "Parent_Org_Name"] = df["Org_Name_Sub"]

    return df


def update_child_vac_data_combined(df):
    """
    Performs pre-processing on the combined childhood vaccinations raw and
    historic source data

    Parameters
    ----------
    df: pandas.DataFrame
        containing the combined raw and historic childhood vaccinations COVER
        source data

    Returns
    -------
    df: pandas.DataFrame
        containing the combined COVER source data with pre-processing applied
    """

    # Update historical vac types as needed
    for prev_vac_type, new_vac_type in param.YOY_UPDATE_PREV_VAC_TYPE.items():
        df.loc[df["Vac_Type"] == prev_vac_type, "Vac_Type"] = new_vac_type

    return df
