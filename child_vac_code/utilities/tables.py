from child_vac_code.utilities.processing import create_output_crosstab

"""
This module contains all the user defined inputs for each table.
The write arguments in get_tables are defined as:

name : str
    Excel worksheet where data is to be written.
write_type: str
    Determines the method of writing the output. Valid options for Excel are:
    excel_static: Writes data to Excel where the length of the data is
    static. Use for timeseries data with a limited number of years to show.
    e.g. time series data fixed to 3 years
    (write_cell must be populated).
    excel_variable: Writes data to Excel where the length of the data is
    variable (write_cell must be populated).
    excel_add_year: Adds a new year (row) to a time series before writing.
    If used then write_cell/year_check_cell should be set as the first year
    in the time series, and include_row_labels should be set to True.
    Can only be used where year values are in rows.
write_cell: str
    Identifies the cell location in the Excel worksheet where the data
    will be pasted (top left of data).
    If write_type is excel_add_year then this is not used (set to None).
include_row_labels: bool
    Determines if the row labels will be written.
empty_cols: list[str]
    A list of letters representing any empty (section separator) excel
    columns in the worksheet. Empty columns will be inserted into the
    dataframe in these positions. Default is None.
year_check_cell: str
    Cell location
    If the output is a time series table, this identifies the cell
    location in the Excel worksheet that contains the latest year value for a
    fixed length time series, or
    where write_type is excel_add_year, then the first year value in the time
    series.
    Used to determine if the new year value already exists i.e. is an update
    rather than an additional data year.
years_as_rows: bool
    Set to true if years in a time series table are arranged in rows (vertical).
    Only used if year_check_cell is not None.
    Set to False if years are arranged in columns (horizontal) or year_check_cell is None
contents: list[str]
    The name of the function that creates the output.
    If more than one function is included, the outputs will be appended.
    Note that multiple contents keys can be added to the dictionary with
    different suffixes (e.g. contents_1), as long as the outputs are of the
    same length and order e.g. same organisation type. The outputs of each
    contents_ key will be joined before writing, retaining only the first
    version of duplicate columns.
    Note that where adding multiple contents keys, the include_row_label
    argument must be consistent for all the functions called (will only return
    one version of the labels if set to True)

"""


def get_tables_cover():
    """
    Establishes the functions (contents) required for each COVER data table,
    and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        # Add population and coverage, 12m vaccines, England to table
        {"name": "Table 1",
         "write_type": "excel_add_year",
         "include_row_labels": True,
         "write_cell": None,
         "empty_cols": ["C", "E", "G", "I", "L", "N"],
         "year_check_cell": "A8",
         "years_as_rows": True,
         "contents_pop": [create_table_population_12m_england_thousands],
         "contents_vax": [create_table_coverage_12m_england]
         },
        # Add population and coverage, 24m vaccines, England to table
        {"name": "Table 2",
         "write_type": "excel_add_year",
         "include_row_labels": True,
         "write_cell": None,
         "empty_cols": ["C", "E", "G", "I", "K", "M", "O"],
         "year_check_cell": "A8",
         "years_as_rows": True,
         "contents_pop": [create_table_population_24m_england_thousands],
         "contents_vax": [create_table_coverage_24m_england]
         },
        # Add population and coverage, 5y vaccines, England to table
        {"name": "Table 3",
         "write_type": "excel_add_year",
         "include_row_labels": True,
         "write_cell": None,
         "empty_cols": ["C", "E", "G", "I", "K", "M"],
         "year_check_cell": "A8",
         "years_as_rows": True,
         "contents_pop": [create_table_population_5y_england_thousands],
         "contents_vax": [create_table_coverage_5y_england]
         },
        # Add coverage, DTaP 24m, England to table
        {"name": "Table 4a",
         "write_type": "excel_add_year",
         "include_row_labels": True,
         "write_cell": None,
         "empty_cols": ["B", "D"],
         "year_check_cell": "A8",
         "years_as_rows": True,
         "contents_nat": [create_table_coverage_dtap_24m_england],
         "contents_reg": [create_table_coverage_dtap_24m_regions]
         },
        # Add coverage, MMR 24m, England to table
        {"name": "Table 4b",
         "write_type": "excel_add_year",
         "include_row_labels": True,
         "write_cell": None,
         "empty_cols": ["B", "D"],
         "year_check_cell": "A8",
         "years_as_rows": True,
         "contents_nat": [create_table_coverage_mmr_24m_england],
         "contents_reg": [create_table_coverage_mmr_24m_regions]
         },
        # Add population, 12m vaccines, UK and all countries to table
        {"name": "Table 5a",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "B10",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents": [create_table_population_12m_uk_thousands,
                      create_table_population_12m_england_thousands,
                      create_table_population_12m_other_nations_thousands]
         },
        # Add coverage, 12m vaccines, UK and all countries to table
        {"name": "Table 5a",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D10",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents": [create_table_coverage_12m_uk,
                      create_table_coverage_12m_england,
                      create_table_coverage_12m_other_nations]
         },
        # Add population, 24m vaccines, UK and all countries to table
        {"name": "Table 5b",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "B10",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents": [create_table_population_24m_uk_thousands,
                      create_table_population_24m_england_thousands,
                      create_table_population_24m_other_nations_thousands]
         },
        # Add coverage, 24m vaccines, UK and all countries to table
        {"name": "Table 5b",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D10",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents": [create_table_coverage_24m_uk,
                      create_table_coverage_24m_england,
                      create_table_coverage_24m_other_nations]
         },
        # Add population, 5y vaccines, UK and all countries to table
        {"name": "Table 5c",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "B10",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents": [create_table_population_5y_uk_thousands,
                      create_table_population_5y_england_thousands,
                      create_table_population_5y_other_nations_thousands]
         },
        # Add coverage, 5y vaccines, UK and all countries to table
        {"name": "Table 5c",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D10",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents": [create_table_coverage_5y_uk,
                      create_table_coverage_5y_england,
                      create_table_coverage_5y_other_nations]
         },
        # Add coverage, DTaP 12m, England to table
        {"name": "Table 6",
         "write_type": "excel_add_year",
         "include_row_labels": True,
         "write_cell": None,
         "empty_cols": None,
         "year_check_cell": "A8",
         "years_as_rows": True,
         "contents": [create_table_coverage_dtap_12m_england]
         },
        # Add coverage, MMR 24m, England to table
        {"name": "Table 7",
         "write_type": "excel_add_year",
         "include_row_labels": True,
         "write_cell": None,
         "empty_cols": None,
         "year_check_cell": "A8",
         "years_as_rows": True,
         "contents": [create_table_coverage_mmr_24m_england]
         },
        # Add population and coverage, 12m vaccines, England to table
        {"name": "Table 8a",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D10",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_12m_england_thousands],
         "contents_vax": [create_table_coverage_12m_england]
         },
        # Add population and coverage, 12m vaccines, regions to table
        {"name": "Table 8a",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A11",
         "empty_cols": ["B", "E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_12m_regions_thousands],
         "contents_vax": [create_table_coverage_12m_regions]
         },
        # Add population and coverage, 12m vaccines, LAs to table
        {"name": "Table 8a",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A21",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_12m_las_thousands],
         "contents_vax": [create_table_coverage_12m_las]
         },
        # Add population and vaccinated, 12m vaccines, England to table
        {"name": "Table 8b",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D9",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_12m_england],
         "contents_vax": [create_table_vaccinated_12m_england]
         },
        # Add population and vaccinated, 12m vaccines, regions to table
        {"name": "Table 8b",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A10",
         "empty_cols": ["B", "E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_12m_regions],
         "contents_vax": [create_table_vaccinated_12m_regions]
         },
        # Add population and vaccinated, 12m vaccines, LAs to table
        {"name": "Table 8b",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A20",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_12m_las],
         "contents_vax": [create_table_vaccinated_12m_las]
         },
        # Add population and coverage, 24m vaccines, England to table
        {"name": "Table 9a",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D10",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_24m_england_thousands],
         "contents_vax": [create_table_coverage_24m_england]
         },
        # Add population and coverage, 24m vaccines, regions to table
        {"name": "Table 9a",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A11",
         "empty_cols": ["B", "E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_24m_regions_thousands],
         "contents_vax": [create_table_coverage_24m_regions]
         },
        # Add population and coverage, 24m vaccines, LAs to table
        {"name": "Table 9a",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A21",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_24m_las_thousands],
         "contents_vax": [create_table_coverage_24m_las]
         },
        # Add population and vaccinated, 24m vaccines, England to table
        {"name": "Table 9b",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D9",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_24m_england],
         "contents_vax": [create_table_vaccinated_24m_england]
         },
        # Add population and vaccinated, 24m vaccines, regions to table
        {"name": "Table 9b",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A10",
         "empty_cols": ["B", "E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_24m_regions],
         "contents_vax": [create_table_vaccinated_24m_regions]
         },
        # Add population and vaccinated, 24m vaccines, LAs to table
        {"name": "Table 9b",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A20",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_24m_las],
         "contents_vax": [create_table_vaccinated_24m_las]
         },
        # Add population and coverage, 5y vaccines, England to table
        {"name": "Table 10a",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D10",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_5y_england_thousands],
         "contents_vax": [create_table_coverage_5y_england]
         },
        # Add population and coverage, 5y vaccines, regions to table
        {"name": "Table 10a",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A11",
         "empty_cols": ["B", "E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_5y_regions_thousands],
         "contents_vax": [create_table_coverage_5y_regions]
         },
        # Add population and coverage, 5y vaccines, LAs to table
        {"name": "Table 10a",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A21",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_5y_las_thousands],
         "contents_vax": [create_table_coverage_5y_las]
         },
        # Add population and vaccinated, 5y vaccines, England to table
        {"name": "Table 10b",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D9",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_5y_england],
         "contents_vax": [create_table_vaccinated_5y_england]
         },
        # Add population and vaccinated, 5y vaccines, regions to table
        {"name": "Table 10b",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A10",
         "empty_cols": ["B", "E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_5y_regions],
         "contents_vax": [create_table_vaccinated_5y_regions]
         },
        # Add population and vaccinated, 5y vaccines, LAs to table
        {"name": "Table 10b",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A20",
         "empty_cols": ["E"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_5y_las],
         "contents_vax": [create_table_vaccinated_5y_las]
         },
        # !!! BCG Code below is year specific, only works for 2022-23 onward
        # Add data for 3m BCG vaccine in England to Table
        # Add population, BCG 3m, England to Table
        {"name": "Table 11a",
            "write_type": "excel_static",
            "include_row_labels": False,
            "write_cell": "D9",
            "empty_cols": ["E"],
            "year_check_cell": None,
            "years_as_rows": False,
            "contents_pop": [create_table_population_bcg_3m_eng],
            "contents_vax": [create_table_vaccinated_bcg_3m_eng],
            "contents_cov": [create_table_coverage_bcg_3m_eng]
         },
        # Add data for 3m BCG vaccine in Reg to Table
        # Add vaccinated, BCG 3m, regions to table
        {"name": "Table 11a",
            "write_type": "excel_static",
            "include_row_labels": True,
            "write_cell": "A10",
            "empty_cols": ["B", "E"],
            "year_check_cell": None,
            "years_as_rows": False,
            "contents_pop": [create_table_population_bcg_3m_reg],
            "contents_vax": [create_table_vaccinated_bcg_3m_reg],
            "contents_cov": [create_table_coverage_bcg_3m_reg]
         },
        # Add data for 3m BCG vaccine in LAs to Table
        # Add population, vaccinated and coverage, BCG 3m, LAs to table
        {"name": "Table 11a",
            "write_type": "excel_variable",
            "include_row_labels": True,
            "write_cell": "A20",
            "empty_cols": ["E"],
            "year_check_cell": None,
            "years_as_rows": False,
            "contents_pop": [create_table_population_bcg_3m_las],
            "contents_vax": [create_table_vaccinated_bcg_3m_las],
            "contents_cov": [create_table_coverage_bcg_3m_las]
         },
        # Add population, vaccinated and coverage, HepB 12m, LAs to table
        {"name": "Table 11b",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A9",
         "empty_cols": ["E", "H"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_hepb_12m_las],
         "contents_vax": [create_table_vaccinated_hepb_12m_las],
         "contents_cov": [create_table_coverage_hepb_12m_las],
         },
        # Add population, vaccinated and coverage, HepB 24m, LAs to table
        {"name": "Table 11c",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A9",
         "empty_cols": ["E", "H"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_hepb_24m_las],
         "contents_vax": [create_table_vaccinated_hepb_24m_las],
         "contents_cov": [create_table_coverage_hepb_24m_las]
         },
    ]

    return all_outputs


def get_tables_flu():
    """
    Establishes the functions (contents) required for each flu table,
    and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        # Add population, vaccinated and coverage, flu 24m, England to table
        {"name": "Table 12",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D8",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_flu_24m_england],
         "contents_vax": [create_table_vaccinated_flu_24m_england],
         "contents_cov": [create_table_coverage_flu_24m_england]
         },
        # Add population, vaccinated and coverage, flu 24m, regions to table
        {"name": "Table 12",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A9",
         "empty_cols": ["B"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_flu_24m_regions],
         "contents_vax": [create_table_vaccinated_flu_24m_regions],
         "contents_cov": [create_table_coverage_flu_24m_regions]
         },
        # Add population, vaccinated and coverage, flu 24m, LAs to table
        {"name": "Table 12",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A19",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_flu_24m_las],
         "contents_vax": [create_table_vaccinated_flu_24m_las],
         "contents_cov": [create_table_coverage_flu_24m_las]
         },
        # Add population, vaccinated and coverage, flu 3y, England to table
        {"name": "Table 13",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D8",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_flu_3y_england],
         "contents_vax": [create_table_vaccinated_flu_3y_england],
         "contents_cov": [create_table_coverage_flu_3y_england]
         },
        # Add population, vaccinated and coverage, flu 3y, regions to table
        {"name": "Table 13",
         "write_type": "excel_static",
         "include_row_labels": True,
         "write_cell": "A9",
         "empty_cols": ["B"],
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_flu_3y_regions],
         "contents_vax": [create_table_vaccinated_flu_3y_regions],
         "contents_cov": [create_table_coverage_flu_3y_regions]
         },
        # Add population, vaccinated and coverage, flu 3y, LAs to table
        {"name": "Table 13",
         "write_type": "excel_variable",
         "include_row_labels": True,
         "write_cell": "A19",
         "empty_cols": None,
         "year_check_cell": None,
         "years_as_rows": False,
         "contents_pop": [create_table_population_flu_3y_las],
         "contents_vax": [create_table_vaccinated_flu_3y_las],
         "contents_cov": [create_table_coverage_flu_3y_las]
         }
    ]

    return all_outputs


"""
    The following functions contain the user defined inputs that determine the
    dataframe content for each output. The arguments are defined as:

org_type: str
    Determines which of the pre-defined org types the data will be filtered to.
    Options are "LA" which brings across all LAs in England and can be used for
    LA or England level data and "NAT" which brings across Wales, Scotland & NI.
    If None no org_type filter will be applied (UK level data)
output_type : str
    Determines which of the pre-defined output types will be reported on.
    Options are "Vaccinated", "Population", "Coverage".
rows : list[str]
    Variable name(s) that holds the output row content (multiple variables
    can be selected).
columns : str
    Variable name that holds the output column content (single variable)
    If set to None then only a total count of the row content will be returned.
sort_on : list[str]
    Optional list of columns names to sort on (ascending).
    Can include columns that will not be displayed in the output.
    Note that using this option will mean that totals will be removed
    e.g. for use in org outputs.
    If row_order is not None then this input should be None.
row_order: dict(str, list)
    Optional dictionary with lists of row content that determines the inclusions
    and sorting. Contains the column name(s) and defined order of content
    in which data will be presented in the output. Allows for full control
    of row ordering (can only include row values that exist in the
    collection). Used for precise user-defined row ordering.
    If sort_on is not None then this input should be None.
column_order: list[str]
    list of content from the 'columns' variable that determines what is
    included and the order they will be presented in the output.
    This can include derived variables as long as they have been added to
    field_definitions.py.
    If set to None then all columns will be returned in default order.
column_rename : dict
    Optional dictionary for renaming of columns from the data source version
    to output requirement. Any column set within the 'rows' or
    'column order' parameters can be renamed.
filter_condition : str
    This is a non-standard, optional dataframe filter as a string
    needed for some outputs. It may consist of one or more filters of the
    dataframe variables.
row_subgroup: dict(dict(str, list))
    Optional input where a grouped option is reported, requiring a new
    subgroup based on row content.
    Contains the target column name, and for each target column another
    nested dictionary with the new subgroup code that will be assigned to the
    new grouping(s), and the original subgroup values that will form the
    group e.g. {"AgeBand": {'53<65': ['53-54', '55-59', '60-64']}}
    Not applicable for the create_output_measure function.
column_subgroup: dict(str, list)
    Optional input where a grouped option is reported, requiring a new
    subgroup based on column content.
    Contains the new value(s) that will be assigned to the
    new grouping(s), and the values (from the 'columns' variable) that
    will form the group.
count_multiplier: num
    All counts will be multiplied by this value in the output e.g. for
    thousands set to 0.001. Set to None of no multiplier is needed.
ts_years: int
    Defines the number of time series years required in the output.
    Default is 1.
rounding: integer/bool
    Number of decimal places to round columns in column_order to.
    The default is False (no rounding applied)

Returns:
-------
    Each function returns a dataframe with the output.

"""


# Create df of population data (thousands) for 12m vaccines for England
def create_table_population_12m_england_thousands(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 12m vaccines for England
def create_table_coverage_12m_england(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_12m",
        "PCV_12m",
        "Rota_12m",
        "MenB_12m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 24m vaccines for England
def create_table_population_24m_england_thousands(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ('DTaP_IPV_Hib_HepB_24m')")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 24m vaccines for England
def create_table_coverage_24m_england(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_24m",
        "MMR_24m",
        "Hib_MenC_24m",
        "PCV_24m",
        "MenB_booster_24m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 5y vaccines for England
def create_table_population_5y_england_thousands(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['MMR1_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 5y vaccines for England
def create_table_coverage_5y_england(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_5y",
        "DTaP_IPV_5y",
        "MMR1_5y",
        "MMR2_5y",
        "Hib_MenC_5y"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for DTaP 24m for England
def create_table_coverage_dtap_24m_england(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for MMR 24m for England
def create_table_coverage_mmr_24m_england(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
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
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for DTaP 24m by region
def create_table_coverage_dtap_24m_regions(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Parent_Org_Code"
    sort_on = None
    row_order = None
    column_order = ["E12000001", "E12000002", "E12000003", "E12000004",
                    "E12000005", "E12000006", "E12000007", "E12000008",
                    "E12000009"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for MMR 24m by region
def create_table_coverage_mmr_24m_regions(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Parent_Org_Code"
    sort_on = None
    row_order = None
    column_order = ["E12000001", "E12000002", "E12000003", "E12000004",
                    "E12000005", "E12000006", "E12000007", "E12000008",
                    "E12000009"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['MMR_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 12m vaccines for UK
def create_table_population_12m_uk_thousands(df):
    org_type = None
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 12m vaccines
# for Wales, Scotland, and N Ireland
def create_table_population_12m_other_nations_thousands(df):
    org_type = "NAT"
    output_type = "Population"
    rows = ["Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {
        "Org_Name": [
            "Wales",
            "Scotland",
            "Northern Ireland"
        ]}
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 12m vaccines for UK
def create_table_coverage_12m_uk(df):
    org_type = None
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_12m",
        "PCV_12m",
        "Rota_12m",
        "MenB_12m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 12m vaccines for Wales, Scotland, and N Ireland
def create_table_coverage_12m_other_nations(df):
    org_type = "NAT"
    output_type = "Coverage"
    rows = ["Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {
        "Org_Name": [
            "Wales",
            "Scotland",
            "Northern Ireland"
        ]}
    column_order = [
        "DTaP_IPV_Hib_HepB_12m",
        "PCV_12m",
        "Rota_12m",
        "MenB_12m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 24m vaccines for UK
def create_table_population_24m_uk_thousands(df):
    org_type = None
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 24m vaccines
# for Wales, Scotland, and N Ireland
def create_table_population_24m_other_nations_thousands(df):
    org_type = "NAT"
    output_type = "Population"
    rows = ["Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {
        "Org_Name": [
            "Wales",
            "Scotland",
            "Northern Ireland"
        ]}
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 24m vaccines for UK
def create_table_coverage_24m_uk(df):
    org_type = None
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_24m",
        "MMR_24m",
        "Hib_MenC_24m",
        "PCV_24m",
        "MenB_booster_24m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 24m vaccines for Wales, Scotland, and N Ireland
def create_table_coverage_24m_other_nations(df):
    org_type = "NAT"
    output_type = "Coverage"
    rows = ["Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {
        "Org_Name": [
            "Wales",
            "Scotland",
            "Northern Ireland"
        ]}
    column_order = [
        "DTaP_IPV_Hib_HepB_24m",
        "MMR_24m",
        "Hib_MenC_24m",
        "PCV_24m",
        "MenB_booster_24m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 5y vaccines for UK
def create_table_population_5y_uk_thousands(df):
    org_type = None
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['MMR1_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 5y vaccines
# for Wales, Scotland, and N Ireland
def create_table_population_5y_other_nations_thousands(df):
    org_type = "NAT"
    output_type = "Population"
    rows = ["Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {
        "Org_Name": [
            "Wales",
            "Scotland",
            "Northern Ireland"
        ]}
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['MMR1_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 5y vaccines for UK
def create_table_coverage_5y_uk(df):
    org_type = None
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_5y",
        "DTaP_IPV_5y",
        "MMR1_5y",
        "MMR2_5y",
        "Hib_MenC_5y"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 5y vaccines for Wales, Scotland, and N Ireland
def create_table_coverage_5y_other_nations(df):
    org_type = "NAT"
    output_type = "Coverage"
    rows = ["Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = {
        "Org_Name": [
            "Wales",
            "Scotland",
            "Northern Ireland"
        ]}
    column_order = [
        "DTaP_IPV_Hib_5y",
        "DTaP_IPV_5y",
        "MMR1_5y",
        "MMR2_5y",
        "Hib_MenC_5y"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for DTaP 12m for England
def create_table_coverage_dtap_12m_england(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 12m vaccines by region
def create_table_population_12m_regions_thousands(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 12m vaccines by region
def create_table_coverage_12m_regions(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_12m",
        "PCV_12m",
        "Rota_12m",
        "MenB_12m"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 12m vaccines by LA
def create_table_population_12m_las_thousands(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 12m vaccines by LA
def create_table_coverage_12m_las(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_12m",
        "PCV_12m",
        "Rota_12m",
        "MenB_12m"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for 12m vaccines for England
def create_table_population_12m_england(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for 12m vaccines for England
def create_table_vaccinated_12m_england(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_12m",
        "PCV_12m",
        "Rota_12m",
        "MenB_12m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for 12m vaccines by region
def create_table_population_12m_regions(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 12m vaccines by region
def create_table_vaccinated_12m_regions(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_12m",
        "PCV_12m",
        "Rota_12m",
        "MenB_12m"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for 12m vaccines by LA
def create_table_population_12m_las(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for 12m vaccines by LA
def create_table_vaccinated_12m_las(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_12m",
        "PCV_12m",
        "Rota_12m",
        "MenB_12m"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 24m vaccines by region
def create_table_population_24m_regions_thousands(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 24m vaccines by region
def create_table_coverage_24m_regions(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_24m",
        "MMR_24m",
        "Hib_MenC_24m",
        "PCV_24m",
        "MenB_booster_24m"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 24m vaccines by LA
def create_table_population_24m_las_thousands(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 24m vaccines by LA
def create_table_coverage_24m_las(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_24m",
        "MMR_24m",
        "Hib_MenC_24m",
        "PCV_24m",
        "MenB_booster_24m"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 5y vaccines by region
def create_table_population_5y_regions_thousands(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['MMR1_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 5y vaccines by region
def create_table_coverage_5y_regions(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_5y",
        "DTaP_IPV_5y",
        "MMR1_5y",
        "MMR2_5y",
        "Hib_MenC_5y"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data (thousands) for 5y vaccines by LA
def create_table_population_5y_las_thousands(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['MMR1_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = 0.001
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for 5y vaccines by LA
def create_table_coverage_5y_las(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_5y",
        "DTaP_IPV_5y",
        "MMR1_5y",
        "MMR2_5y",
        "Hib_MenC_5y"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for 5y vaccines for England
def create_table_population_5y_england(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Type"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['MMR1_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for 5y vaccines for England
def create_table_vaccinated_5y_england(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Org_Type"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_5y",
        "DTaP_IPV_5y",
        "MMR1_5y",
        "MMR2_5y",
        "Hib_MenC_5y"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for 5y vaccines by region
def create_table_population_5y_regions(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['MMR1_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for 5y vaccines by region
def create_table_vaccinated_5y_regions(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_5y",
        "DTaP_IPV_5y",
        "MMR1_5y",
        "MMR2_5y",
        "Hib_MenC_5y"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for 5y vaccines by LA
def create_table_population_5y_las(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['MMR1_5y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for 5y vaccines by LA
def create_table_vaccinated_5y_las(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_5y",
        "DTaP_IPV_5y",
        "MMR1_5y",
        "MMR2_5y",
        "Hib_MenC_5y"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for 24m vaccines for England
def create_table_vaccinated_24m_england(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_24m",
        "MMR_24m",
        "Hib_MenC_24m",
        "PCV_24m",
        "MenB_booster_24m"
    ]
    column_rename = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for 24m vaccines by region
def create_table_vaccinated_24m_regions(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_24m",
        "MMR_24m",
        "Hib_MenC_24m",
        "PCV_24m",
        "MenB_booster_24m"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for 24m vaccines by LA
def create_table_vaccinated_24m_las(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = [
        "DTaP_IPV_Hib_HepB_24m",
        "MMR_24m",
        "Hib_MenC_24m",
        "PCV_24m",
        "MenB_booster_24m"
    ]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for 24m vaccines for England
def create_table_population_24m_england(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ('DTaP_IPV_Hib_HepB_24m')")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for 24m vaccines by region
def create_table_population_24m_regions(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for 24m vaccines by LA
def create_table_population_24m_las(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['DTaP_IPV_Hib_HepB_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create df of population for 3 month bcg vaccines in LAs (no multiplier)
def create_table_population_bcg_3m_las(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {'BCG_3m': 'Population'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create df of vaccinated for 3 month bcg vaccines in LAs (no multiplier)
def create_table_vaccinated_bcg_3m_las(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {'BCG_3m': 'Vaccinated'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create df of coverage for 3 month bcg vaccines in LAs
def create_table_coverage_bcg_3m_las(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = ['BCG_3m']
    column_rename = {'BCG_3m': 'Coverage'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create df of population for 3 month bcg vaccines in regions
def create_table_population_bcg_3m_reg(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = {'BCG_3m': 'Population'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create df of vaccinated for 3 month bcg vaccines in regions
def create_table_vaccinated_bcg_3m_reg(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = {'BCG_3m': 'Vaccinated'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create df of coverage for 3 month bcg vaccines in regions
def create_table_coverage_bcg_3m_reg(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = ['BCG_3m']
    column_rename = {'BCG_3m': 'Coverage'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create df of population for 3 month bcg vaccines for England
def create_table_population_bcg_3m_eng(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = {'BCG_3m': 'Population'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create df of vaccinated for 3 month bcg vaccines in England
def create_table_vaccinated_bcg_3m_eng(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = {'BCG_3m': 'Vaccinated'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# To create df of coverage for 3 month bcg vaccines in England
def create_table_coverage_bcg_3m_eng(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = {'BCG_3m': 'Coverage'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['BCG_3m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for HepB 12m by LA
# Vaccine_Status will be moved to end of output in output_specific_updates
def create_table_population_hepb_12m_las(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name", "Vaccine_Status"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {'HepB_Group2_12m': 'Population'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['HepB_Group2_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for HepB 12m by LA
# Vaccine_Status will be moved to end of output in output_specific_updates
def create_table_vaccinated_hepb_12m_las(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name", "Vaccine_Status"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {'HepB_Group2_12m': 'Vaccinated'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['HepB_Group2_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for HepB 12m by LA
# Vaccine_Status will be moved to end of output in output_specific_updates
def create_table_coverage_hepb_12m_las(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name", "Vaccine_Status"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = ['HepB_Group2_12m']
    column_rename = {'HepB_Group2_12m': 'Coverage'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['HepB_Group2_12m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for HepB 24m by LA
# Vaccine_Status will be moved to end of output in output_specific_updates
def create_table_population_hepb_24m_las(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name", "Vaccine_Status"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {'HepB_Group2_24m': 'Population'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['HepB_Group2_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for HepB 24m by LA
# Vaccine_Status will be moved to end of output in output_specific_updates
def create_table_vaccinated_hepb_24m_las(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name", "Vaccine_Status"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = {'HepB_Group2_24m': 'Vaccinated'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['HepB_Group2_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for HepB 24m by LA
# Vaccine_Status will be moved to end of output in output_specific_updates
def create_table_coverage_hepb_24m_las(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name", "Vaccine_Status"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = ['HepB_Group2_24m']
    column_rename = {'HepB_Group2_24m': 'Coverage'}
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['HepB_Group2_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for flu 24m for England
def create_table_population_flu_24m_england(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for flu 24m for England
def create_table_vaccinated_flu_24m_england(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    filter_condition = (
        "Vac_Type in ['Flu_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for flu 24m for England
def create_table_coverage_flu_24m_england(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    filter_condition = (
        "Vac_Type in ['Flu_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for flu 24m by region
def create_table_population_flu_24m_regions(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for flu 24m by region
def create_table_vaccinated_flu_24m_regions(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for flu 24m by region
def create_table_coverage_flu_24m_regions(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    filter_condition = (
        "Vac_Type in ['Flu_24m']")
    row_subgroup = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for flu 24m by LA
def create_table_population_flu_24m_las(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_24m']")
    row_subgroup = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for flu 24m by LA
def create_table_vaccinated_flu_24m_las(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for flu 24m by LA
def create_table_coverage_flu_24m_las(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_24m']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for flu 3y for England
def create_table_population_flu_3y_england(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_3y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for flu 3y for England
def create_table_vaccinated_flu_3y_england(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    filter_condition = (
        "Vac_Type in ['Flu_3y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for flu 3y for England
def create_table_coverage_flu_3y_england(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["FinancialYear"]
    columns = "Vac_Type"
    sort_on = None
    row_order = None
    column_order = None
    column_rename = None
    filter_condition = (
        "Vac_Type in ['Flu_3y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for flu 3y by region
def create_table_population_flu_3y_regions(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_3y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for flu 3y by region
def create_table_vaccinated_flu_3y_regions(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_3y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for flu 3y by region
def create_table_coverage_flu_3y_regions(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Parent_Org_Code", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code"]
    row_order = None
    column_order = None
    column_rename = None
    filter_condition = (
        "Vac_Type in ['Flu_3y']")
    row_subgroup = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of population data for flu 3y by LA
def create_table_population_flu_3y_las(df):
    org_type = "LA"
    output_type = "Population"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_3y']")
    row_subgroup = None
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of vaccinated data for flu 3y by LA
def create_table_vaccinated_flu_3y_las(df):
    org_type = "LA"
    output_type = "Vaccinated"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_3y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)


# Create df of coverage data for flu 3y by LA
def create_table_coverage_flu_3y_las(df):
    org_type = "LA"
    output_type = "Coverage"
    rows = ["Org_Code", "Org_Name", "Parent_Org_Name"]
    columns = "Vac_Type"
    sort_on = ["Parent_Org_Code",
               "Org_Name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    filter_condition = (
        "Vac_Type in ['Flu_3y']")
    row_subgroup = None
    column_subgroup = None
    count_multiplier = None
    ts_years = 1

    return create_output_crosstab(df, org_type, output_type, rows, columns,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition, row_subgroup,
                                  column_subgroup, count_multiplier, ts_years)
