from child_vac_code.utilities.processing import (create_output_crosstab,
                                                 create_output_dashboard_data)
import child_vac_code.parameters as param


"""
This module contains all the user defined inputs for the Power BI dashboard or map data.
See the tables.py and processing.py files for details of the arguments used
in the related functions.

"""


def get_dashboards_map_input():
    """
    Establishes the functions (contents) required for each output used
    as input data for the Power BI map file, and the arguments needed for
    the write process

    Will be written as .csv files to Outputs/Templates area

    Parameters:
        None

    """
    all_outputs = [
        # Create the data that is used for the PowerBI maps in the report
        # The vaccines are DTaP12m and MMR24m
        {"name": "childhood_vaccination_map_data",
         "write_type": "csv",
         "contents": [create_dashboard_map_data],
         },
    ]

    return all_outputs


def get_dashboards_input():
    """
    Establishes the functions (contents) required for each output used as
    input data for the Power BI dashboard, and the arguments needed for
    the write process.

    Will be written to Excel file in Outputs/Templates area

    Parameters:
        None

    """
    all_outputs = [

        # Create data used as input for the PowerBI dashboard
        {"name": "DashboardData",
         "write_type": "excel_variable",
         "write_cell": "A2",
         "include_row_labels": True,
         "year_check_cell": None,
         "years_as_rows": None,
         "empty_cols": None,
         "contents": [create_dashboard_data_uk,
                      create_dashboard_data_england,
                      create_dashboard_data_other_nations,
                      create_dashboard_data_regions,
                      create_dashboard_data_las],
         },
    ]

    return all_outputs


def get_dashboards_internal_input():
    """
    Establishes the functions (contents) required for each output used as
    input data for the internal Power BI dashboard, and the arguments needed for
    the write process.

    Will be written to Excel file in Outputs/Validations area

    Parameters:
        None

    """
    all_outputs = [

        # Create data used as input for the internal PowerBI dashboard
        {"name": "InternalDashboardData",
         "write_type": "excel_variable",
         "write_cell": "A2",
         "include_row_labels": True,
         "year_check_cell": None,
         "years_as_rows": None,
         "empty_cols": None,
         "contents": [create_dashboard_data_internal_uk,
                      create_dashboard_data_internal_england,
                      create_dashboard_data_internal_other_nations,
                      create_dashboard_data_internal_regions,
                      create_dashboard_data_internal_las],
         },
    ]

    return all_outputs


def get_dashboards_csv_pub():
    """
    Establishes the functions (contents) required for each dashboard output used to
    create a .csv for publication, and the arguments needed for the write process

    Will be written to Outputs/PublicationFiles/CSVs with the current year
    included in the filename

    Parameters:
        None

    """
    all_outputs = [
        # Create data used for the PowerBI dashboard to be published
        {"name": "childhood-vaccination-dashboard-data",
         "write_type": "csv",
         "contents": [create_dashboard_data_uk,
                      create_dashboard_data_england,
                      create_dashboard_data_other_nations,
                      create_dashboard_data_regions,
                      create_dashboard_data_las],
         },
    ]

    return all_outputs


# To create df of coverage for DTaP12m and MMR24m for the dashboard report map
def create_dashboard_map_data(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear", "Parent_Org_Code", "Org_Code", "Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code", "Org_Code"]
    row_order = None
    column_order = None
    column_rename = {"FinancialYear": "CollectionYearRange"}
    row_subgroup = None
    column_subgroup = None
    filter_condition = ("Vac_Type in ['DTaP_IPV_Hib_HepB_12m', 'MMR_24m']")
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  row_subgroup, column_subgroup,
                                  count_multiplier, ts_years)


# Creates dashboard data at UK level
def create_dashboard_data_uk(df):
    output_type = "UK"
    org_type = None
    breakdowns = ["FinancialYear", "Org_Code", "Org_Name", "Org_Level", "Vac_Type"]
    sort_on = ["Vac_Type", "Org_Code"]
    column_rename = {"FinancialYear": "Year", "Org_Code": "OrgCode",
                     "Org_Name": "OrgName", "Org_Level": "OrgType",
                     "Vac_Type": "VacCode"}
    filter_condition = "Vac_Type not in (@param.SELECTIVE_VACCS)"
    population_vaccines = param.POPULATION_VACCINES

    return create_output_dashboard_data(df, output_type, org_type, breakdowns,
                                        sort_on, column_rename,
                                        filter_condition, population_vaccines)


# Creates dashboard data at national (England) level
def create_dashboard_data_england(df):
    output_type = "National"
    org_type = "LA"
    breakdowns = ["FinancialYear", "Org_Code", "Org_Name", "Org_Level", "Vac_Type"]
    sort_on = ["Vac_Type", "Org_Code"]
    column_rename = {"FinancialYear": "Year", "Org_Code": "OrgCode",
                     "Org_Name": "OrgName", "Org_Level": "OrgType",
                     "Vac_Type": "VacCode"}
    filter_condition = "Vac_Type not in (@param.SELECTIVE_VACCS)"
    population_vaccines = param.POPULATION_VACCINES

    return create_output_dashboard_data(df, output_type, org_type, breakdowns,
                                        sort_on, column_rename,
                                        filter_condition, population_vaccines)


# Creates dashboard data for other nations
def create_dashboard_data_other_nations(df):
    output_type = "Other nations"
    org_type = "NAT"
    breakdowns = ["FinancialYear", "Org_Code", "Org_Name", "Org_Level", "Vac_Type"]
    sort_on = ["Vac_Type", "Org_Code"]
    column_rename = {"FinancialYear": "Year", "Org_Code": "OrgCode",
                     "Org_Name": "OrgName", "Org_Level": "OrgType",
                     "Vac_Type": "VacCode"}
    filter_condition = "Vac_Type not in (@param.SELECTIVE_VACCS)"
    population_vaccines = param.POPULATION_VACCINES

    return create_output_dashboard_data(df, output_type, org_type, breakdowns,
                                        sort_on, column_rename,
                                        filter_condition, population_vaccines)


# Creates dashboard data for regions
def create_dashboard_data_regions(df):
    output_type = "Region"
    org_type = "LA"
    breakdowns = ["FinancialYear", "Parent_Org_Code",
                  "Parent_Org_Name", "Org_Level", "Vac_Type"]
    sort_on = ["Vac_Type", "Parent_Org_Code"]
    column_rename = {"FinancialYear": "Year", "Parent_Org_Code": "OrgCode",
                     "Parent_Org_Name": "OrgName", "Org_Level": "OrgType",
                     "Vac_Type": "VacCode"}
    filter_condition = "Vac_Type not in (@param.SELECTIVE_VACCS)"
    population_vaccines = param.POPULATION_VACCINES

    return create_output_dashboard_data(df, output_type, org_type, breakdowns,
                                        sort_on, column_rename,
                                        filter_condition, population_vaccines)


# Creates dashboard data for local authorities
def create_dashboard_data_las(df):
    output_type = "LA"
    org_type = "LA"
    breakdowns = ["FinancialYear", "Org_Code", "Org_Name", "Org_Level", "Vac_Type"]
    sort_on = ["Vac_Type", "Org_Code"]
    column_rename = {"FinancialYear": "Year", "Org_Code": "OrgCode",
                     "Org_Name": "OrgName", "Org_Level": "OrgType",
                     "Vac_Type": "VacCode"}
    filter_condition = "Vac_Type not in (@param.SELECTIVE_VACCS)"
    population_vaccines = param.POPULATION_VACCINES

    return create_output_dashboard_data(df, output_type, org_type, breakdowns,
                                        sort_on, column_rename,
                                        filter_condition, population_vaccines)


# Creates internal dashboard data at UK level
def create_dashboard_data_internal_uk(df):
    output_type = "UK"
    org_type = None
    breakdowns = ["FinancialYear", "Org_Code", "Org_Name", "Org_Level", "Vac_Type"]
    sort_on = ["Vac_Type", "Org_Code"]
    column_rename = None
    filter_condition = "Vac_Type not in (@param.EXCLUDE_VACCS_VAL)"
    population_vaccines = param.POPULATION_VACCINES_VAL
    ts_years = param.TS_YEARS_INTERNAL_DASH

    return create_output_dashboard_data(df, output_type, org_type, breakdowns,
                                        sort_on, column_rename,
                                        filter_condition, population_vaccines, ts_years)


# Creates internal dashboard data at national (England) level
def create_dashboard_data_internal_england(df):
    output_type = "National"
    org_type = "LA"
    breakdowns = ["FinancialYear", "Org_Code", "Org_Name", "Org_Level", "Vac_Type"]
    sort_on = ["Vac_Type", "Org_Code"]
    column_rename = None
    filter_condition = "Vac_Type not in (@param.EXCLUDE_VACCS_VAL)"
    population_vaccines = param.POPULATION_VACCINES_VAL
    ts_years = param.TS_YEARS_INTERNAL_DASH

    return create_output_dashboard_data(df, output_type, org_type, breakdowns,
                                        sort_on, column_rename,
                                        filter_condition, population_vaccines, ts_years)


# Creates internal dashboard data for other nations
def create_dashboard_data_internal_other_nations(df):
    output_type = "Other nations"
    org_type = "NAT"
    breakdowns = ["FinancialYear", "Org_Code", "Org_Name", "Org_Level", "Vac_Type"]
    sort_on = ["Vac_Type", "Org_Code"]
    column_rename = None
    filter_condition = "Vac_Type not in (@param.EXCLUDE_VACCS_VAL)"
    population_vaccines = param.POPULATION_VACCINES_VAL
    ts_years = param.TS_YEARS_INTERNAL_DASH

    return create_output_dashboard_data(df, output_type, org_type, breakdowns,
                                        sort_on, column_rename,
                                        filter_condition, population_vaccines, ts_years)


# Creates internal dashboard data for regions
def create_dashboard_data_internal_regions(df):
    output_type = "Region"
    org_type = "LA"
    breakdowns = ["FinancialYear", "Parent_Org_Code",
                  "Parent_Org_Name", "Org_Level", "Vac_Type"]
    sort_on = ["Vac_Type", "Parent_Org_Code"]
    column_rename = {"Parent_Org_Code": "OrgCode",
                     "Parent_Org_Name": "OrgName"}
    filter_condition = "Vac_Type not in (@param.EXCLUDE_VACCS_VAL)"
    population_vaccines = param.POPULATION_VACCINES_VAL
    ts_years = param.TS_YEARS_INTERNAL_DASH

    return create_output_dashboard_data(df, output_type, org_type, breakdowns,
                                        sort_on, column_rename,
                                        filter_condition, population_vaccines, ts_years)


# Creates internal dashboard data for local authorities
def create_dashboard_data_internal_las(df):
    output_type = "LA"
    org_type = "LA"
    breakdowns = ["FinancialYear", "Org_Code", "Org_Name", "Org_Level", "Vac_Type"]
    sort_on = ["Vac_Type", "Org_Code"]
    column_rename = None
    filter_condition = "Vac_Type not in (@param.EXCLUDE_VACCS_VAL)"
    population_vaccines = param.POPULATION_VACCINES_VAL
    ts_years = param.TS_YEARS_INTERNAL_DASH

    return create_output_dashboard_data(df, output_type, org_type, breakdowns,
                                        sort_on, column_rename,
                                        filter_condition, population_vaccines, ts_years)
