from child_vac_code.utilities.processing import create_output_crosstab

"""
This module contains all the user defined inputs for each chart.

See the tables.py file for details of each argument.

"""


def get_charts_cover():
    """
    Establishes the functions (contents) required for each COVER data chart output,
    and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        # Add DTaP df 12m vaccs coverage to England time series
        {"name": "DTaP_12m_TSeries",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A12",
         "empty_cols": ["B"],
         "year_check_cell": "A12",
         "years_as_rows": True,
         "contents": [create_chart_dtap_12m_year_eng]
         },
        # Add DTaP df 12m vaccs coverage for Eng and regions to regional time series
        {"name": "DTaP_12m_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_dtap_12m_year_eng,
                      create_chart_dtap_12m_year_reg]
         },
        # Add DTaP df 24m vaccs coverage to England time series
        {"name": "DTaP_24m_TSeries",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A12",
         "empty_cols": ["B"],
         "year_check_cell": "A12",
         "years_as_rows": True,
         "contents": [create_chart_dtap_24m_year_eng]
         },
        # Add DTaP df 24m vaccs coverage for Eng and regions to regional time series
        {"name": "DTaP_24m_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_dtap_24m_year_eng,
                      create_chart_dtap_24m_year_reg]
         },
        # Add DTaP df 5y vaccs coverage to England time series
        {"name": "DTaP_5yr_TSeries",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A12",
         "empty_cols": None,
         "year_check_cell": "A12",
         "years_as_rows": True,
         "contents": [create_chart_dtap_5y_year_eng]
         },
        # Add DTaP df 5y vaccs coverage for Eng and regions to regional time series
        {"name": "DTaP_5yr_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_dtap_5y_year_eng,
                      create_chart_dtap_5y_year_reg]
         },
        # Add DTaP_IPV df 5y vaccs coverage to England time series
        {"name": "DTaP_IPV_5yr_TSeries",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A12",
         "empty_cols": None,
         "year_check_cell": "A12",
         "years_as_rows": True,
         "contents": [create_chart_dtap_ipv_5y_year_eng]
         },
        # Add DTaP_IPV df 5y vaccs coverage for Eng and regions to regional time series
        {"name": "DTaP_IPV_5yr_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_dtap_ipv_5y_year_eng,
                      create_chart_dtap_ipv_5y_year_reg]
         },
        # Add MMR 24m vaccs coverage to England time series
        {"name": "MMR_24m_TSeries",
         "write_type": "excel_add_year",
         "include_row_labels": True,
         "write_cell": None,
         "empty_cols": None,
         "year_check_cell": "A2",
         "years_as_rows": True,
         "contents": [create_chart_mmr_24m_year_eng]
         },
        # Add MMR 24m vaccs coverage for Eng and regions to regional time series
        {"name": "MMR_24m_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_mmr_24m_year_eng,
                      create_chart_mmr_24m_year_reg]
         },
        # Add MMR 24m LA results for histogram
        {"name": "MMR_24m_LA_Results",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A2",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents": [create_chart_mmr_24m_year_las]
         },
        # Add MMR1 5y vaccs coverage to England time series
        {"name": "MMR1_5yr_TSeries",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A12",
         "empty_cols": None,
         "year_check_cell": "A12",
         "years_as_rows": True,
         "contents": [create_chart_mmr1_5y_year_eng]
         },
        # Add MMR1 5y vaccs coverage for Eng and regions to regional time series
        {"name": "MMR1_5yr_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_mmr1_5y_year_eng,
                      create_chart_mmr1_5y_year_reg]
         },
        # Add MMR2 5y vaccs coverage to England time series
        {"name": "MMR2_5yr_TSeries",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A12",
         "empty_cols": None,
         "year_check_cell": "A12",
         "years_as_rows": True,
         "contents_mmr1": [create_chart_mmr1_5y_year_eng],
         "contents_mmr2": [create_chart_mmr2_5y_year_eng]
         },
        # Add MMR2 5y vaccs coverage for Eng and regions to regional time series
        {"name": "MMR2_5yr_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_mmr2_5y_year_eng,
                      create_chart_mmr2_5y_year_reg]
         },
        # Add Rota 12m vaccs coverage to England time series
        {"name": "Rota_12m_TSeries",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A12",
         "empty_cols": None,
         "year_check_cell": "A12",
         "years_as_rows": True,
         "contents": [create_chart_rota_12m_year_eng]
         },
        # Add Rota 12m vaccs coverage for Eng and regions to regional time series
        {"name": "Rota_12m_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_rota_12m_year_eng,
                      create_chart_rota_12m_year_reg]
         },
        # Add PCV 12m and 24m vaccs coverage to England time series
        {"name": "PCV_12m_24m_TSeries",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A12",
         "empty_cols": None,
         "year_check_cell": "A12",
         "years_as_rows": True,
         "contents_12m": [create_chart_pcv_12m_year_eng],
         "contents_24m": [create_chart_pcv_24m_year_eng]
         },
        # Add PCV 24m vaccs coverage for Eng and regions to regional time series
        {"name": "PCV_24m_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_pcv_24m_year_eng,
                      create_chart_pcv_24m_year_reg]
         },
        # Add Hib MenC 24m vaccs coverage to England time series
        {"name": "Hib_MenC_24m_TSeries",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A12",
         "empty_cols": None,
         "year_check_cell": "A12",
         "years_as_rows": True,
         "contents": [create_chart_hib_menc_24m_year_eng]
         },
        # Add Hib MenC 5y vaccs coverage to England time series
        {"name": "Hib_MenC_5y_TSeries",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A12",
         "empty_cols": None,
         "year_check_cell": "A12",
         "years_as_rows": True,
         "contents": [create_chart_hib_menc_5y_year_eng]
         },
        # Add Hib MenC 24m vaccs coverage for Eng and regions to regional time series
        {"name": "Hib_MenC_24m_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_hib_menc_24m_year_eng,
                      create_chart_hib_menc_24m_year_reg]
         },
        # Add Hib MenC 5y vaccs coverage for Eng and regions to regional time series
        {"name": "Hib_MenC_5y_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_hib_menc_5y_year_eng,
                      create_chart_hib_menc_5y_year_reg]
         },
        # Add MenB 12m vaccs coverage for Eng and regions to regional time series
        {"name": "MenB_12m_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_menb_12m_year_eng,
                      create_chart_menb_12m_year_reg]
         },
        # Add MenB booster 24m vaccs coverage for Eng and regions to regional time series
        {"name": "MenB_Booster_24m_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_menb_boost_24m_year_eng,
                      create_chart_menb_boost_24m_year_reg]
         },


    ]

    return all_outputs


def get_charts_flu():
    """
    Establishes the functions (contents) required for each COVER data chart output,
    and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        # Add 24m 3yr flu vaccs coverage
        {"name": "Flu_2y_3y_Reg",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D2",
         "empty_cols": None,
         "year_check_cell": "D1",
         "years_as_rows": False,
         "contents": [create_chart_flu_24m_3y_year_eng,
                      create_chart_flu_24m_3y_year_reg]
         }
    ]

    return all_outputs


"""
    The following functions contain the user defined inputs that determine the
    dataframe content for each output.

    See the tables.py file for details of each argument.


"""


# df of DTaP 12m vaccs coverage for England
def create_chart_dtap_12m_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_12m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1
    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of DTaP 12m vaccs coverage for regions
def create_chart_dtap_12m_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['DTaP_IPV_Hib_HepB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of DTaP 24m vaccs coverage for England
def create_chart_dtap_24m_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_24m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1
    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of DTaP 24m vaccs coverage for regions
def create_chart_dtap_24m_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['DTaP_IPV_Hib_HepB_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of DTaP 5y vaccs coverage for England
def create_chart_dtap_5y_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_5y"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1
    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of DTaP 5y vaccs coverage for regions
def create_chart_dtap_5y_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['DTaP_IPV_Hib_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of DTaP_IPV 5y vaccs coverage for England
def create_chart_dtap_ipv_5y_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_5y"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1
    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of DTaP_IPV 5y vaccs coverage for regions
def create_chart_dtap_ipv_5y_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['DTaP_IPV_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of MMR 24m vaccs coverage for England
def create_chart_mmr_24m_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "MMR_24m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1
    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of MMR 24m vaccs coverage for regions
def create_chart_mmr_24m_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['MMR_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1
    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of MMR 24m vaccs coverage for LAs
def create_chart_mmr_24m_year_las(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Org_Code", "Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Org_Name",
               "Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    filter_condition = (
        "Vac_Type in ['MMR_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years)


# df of MMR 5y vaccs coverage for England
def create_chart_mmr1_5y_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "MMR1_5y"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1
    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of MMR 5y vaccs coverage for regions
def create_chart_mmr1_5y_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['MMR1_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of MMR2 5y vaccs coverage for England
def create_chart_mmr2_5y_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "MMR2_5y"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1
    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of MMR2 5y vaccs coverage for regions
def create_chart_mmr2_5y_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['MMR2_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of rota 12m vaccs coverage for England
def create_chart_rota_12m_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "Rota_12m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1
    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of rota 12m vaccs coverage for regions
def create_chart_rota_12m_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['Rota_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of PCV 12m vaccs coverage for England
def create_chart_pcv_12m_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "PCV_12m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of PCV 24m vaccs coverage for England
def create_chart_pcv_24m_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "PCV_24m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of PCV 24m vaccs coverage for regions
def create_chart_pcv_24m_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['PCV_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of Hib MenC 24m vaccs coverage for England
def create_chart_hib_menc_24m_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "Hib_MenC_24m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of Hib MenC 24m vaccs coverage for regions
def create_chart_hib_menc_24m_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['Hib_MenC_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of Hib MenC 5y vaccs coverage for England
def create_chart_hib_menc_5y_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "Hib_MenC_5y"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of Hib MenC 5y vaccs coverage for regions
def create_chart_hib_menc_5y_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['Hib_MenC_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of MenB 12m vaccs coverage for England
def create_chart_menb_12m_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "MenB_12m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of MenB 12m vaccs coverage for regions
def create_chart_menb_12m_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['MenB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of MenB booster 24m vaccs coverage for England
def create_chart_menb_boost_24m_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "MenB_booster_24m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of MenB booster 24m vaccs coverage for regions
def create_chart_menb_boost_24m_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['MenB_booster_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of flu 24m and 3y vaccs coverage for england
def create_chart_flu_24m_3y_year_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Vac_Type"]
    columns = None
    sort_on = None
    row_order = {"Vac_Type": ["Flu_24m_3y"]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['Flu_24m', 'Flu_3y']")
    row_subgroup = {"Vac_Type":
                    {"Flu_24m_3y": ["Flu_24m", "Flu_3y"]}}
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)


# df of flu 24m and 3y vaccs coverage for regions
def create_chart_flu_24m_3y_year_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Name", "Vac_Type"]
    columns = None
    sort_on = None
    row_order = {"Parent_Org_Name": [
        "North East",
        "North West",
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "East of England",
        "London",
        "South East",
        "South West"
    ],
        "Vac_Type": ["Flu_24m_3y"]}
    column_order = None
    column_rename = None
    filter_condition = ("Vac_Type in ['Flu_24m', 'Flu_3y']")
    row_subgroup = {"Vac_Type":
                    {"Flu_24m_3y": ["Flu_24m", "Flu_3y"]}}
    column_subgroup = None
    count_multiplier = None
    ts_years = 1
    rounding = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier,
                                  ts_years, rounding)
