# Set the parameters for the project
import pathlib

# --- Filepaths ---
# Sets the file paths for the project
BASE_DIR = pathlib.Path(r"BaseDirectory")
INPUT_DIR = BASE_DIR / "Inputs"
OUTPUT_DIR = BASE_DIR / "Outputs"
TEMPLATE_DIR = OUTPUT_DIR / "Templates"
PUB_DIR = OUTPUT_DIR / "PublicationFiles"
TAB_DIR = PUB_DIR / "DataTables"
CHART_DIR = PUB_DIR / "Charts"
CSV_DIR = PUB_DIR / "CSVs"
DASH_DIR = PUB_DIR / "Dashboards"
LOG_DIR = OUTPUT_DIR / "Logs"
VALID_DIR = OUTPUT_DIR / "Validations"

# Set the locations/filenames of the template files
OUTLIER_FILEPATH = VALID_DIR / "childhood_vaccination_outliers.xlsx"
MAIN_VALIDATION_FILEPATH = VALID_DIR / "childhood_vaccination_main_validations.xlsx"
DASHBOARD_DATA_INTERNAL_FILEPATH = VALID_DIR / \
    "childhood_vaccination_dashboard_data_internal.xlsx"
TABLE_TEMPLATE = TEMPLATE_DIR / "childhood_vaccination_datatables.xlsx"
CHART_TEMPLATE = TEMPLATE_DIR / "childhood_vaccination_charts.xlsx"
DASHBOARD_TEMPLATE = TEMPLATE_DIR / "childhood_vaccination_dashboard_data.xlsx"

# Set the locations/filenames of the input files
FLU_LA = INPUT_DIR / "childhood_vaccination_flu_la.csv"
VACC_STATUS_UPDATES = INPUT_DIR / "childhood_vaccination_status_updates.csv"


# --- Reporting years ---
# Set start of current/previous financial years as recorded in raw/asset data (DDMMMYYYY)
FYEAR_START = "01APR2022"
FYEAR_START_PREV = "01APR2021"


# --- Time series years ---
# Set the number of years of data required for outputs
# NOTE - include the current year when setting number of years, to ensure data
# for correct years are pulled from asset.
# Recommended to not go any further back than 2016-17 as 2013-14 to 2015-16
# contains a mixture of actual/estimated data in the asset and this process
# only extracts actual data
# - Validations (number >=2) -
TS_YEARS_VAL_MAIN_YOY = 5
TS_YEARS_VAL_OUTLIERS = 2
TS_YEARS_INTERNAL_DASH = 7
# - Publication outputs (number >=1) -
TS_YEARS_PUB = 1


# --- Run flags and publication outputs ---
# Sets which outputs should be run as part of the create_validations.py
# or create_publication.py process
# (True or False)

# - Validations -
RUN_MAIN_VALIDATIONS = False  # Main validation outputs
RUN_OUTLIERS = False  # Outlier outputs
RUN_INTERNAL_DASH = False  # Internal dashboard data output
# - Publication outputs -
RUN_TABLES_COVER = False  # Tables outputs - COVER data
RUN_CHARTS_COVER = False  # Chart output data - COVER data
RUN_CSVS_COVER = False  # CSV outputs - COVER data
RUN_DASHBOARDS_COVER = False  # Dashboard outputs - COVER data
RUN_TABLES_FLU = False  # Tables outputs - flu data
RUN_CHARTS_FLU = False  # Charts output data - flu data

# Set whether the final publication outputs should be written as part of the pipeline
RUN_PUBLICATION_CHARTS_OUTPUTS = False
RUN_PUBLICATION_TABLES_OUTPUTS = False
# Worksheets to be removed from final publication file
TABLES_REMOVE = []


# --- SQL query references ---
# Set the data asset sql database properties
SERVER = "SERVER"
DATABASE = "DATABASE"
# Current year's data before load to final table - used for validations
TABLE_RAW = "TABLE_RAW"
TABLE = "TABLE"

# Set the corporate reference data server/database/table names and other query
# conditions for import of reference data.
CORP_REF_SERVER = "REF_SERVER"
CORP_REF_DATABASE = "REF_DATABASE"
ONS_ORG_TABLE = "REF_TABLE"  # Table containing the ONS organisation listings


# --- Updates ---
# Small LAs to combine with larger LAs for publication outputs
# City of London E09000001 with Hackney E09000012,
# Isles of Scilly E06000053 with Cornwall E06000052,
# Rutland E06000017 with Leicestershire E10000018
LA_UPDATE = {"From_code": ["E09000001", "E06000053", "E06000017"],
             "To_code":   ["E09000012", "E06000052", "E10000018"],
             "From_name": ["City of London", "Isles of Scilly", "Rutland"],
             "To_name":   ["Hackney", "Cornwall", "Leicestershire"]}

# Update any flu data LA codes for publication outputs
# May be required if submitted code is not active in the financial year
# being processed and needs updating to correct code
# e.g. '{"Q61": "Q61-NEWCODE", "Q62": "Q62-NEWCODE"}' etc.
UPDATE_LA_CODE_FLU = {"E08000020": "E08000037",
                      "E06000048": "E06000057",
                      "E10000002": "E06000060"}


# --- Definitions ---
# Set symbols for not applicable (null) and not available values in all outputs
NOT_APPLICABLE = "z"
NOT_AVAILABLE = ":"

# Set the symbol/text to be used for not included values in the tidy csv outputs
CSV_NOT_INC = "not included"

# Define the types of local level organisations that are included in all outputs
# Used to select organisation reference data for sub-regional (local) tables.
# Should contain the name of the org_code column and corresponding org_type.
# The org type must exist in df_org_ref (as extracted by query_orgref.sql)
LOCAL_LEVEL_ORGS = {"LA_code": "LA",
                    "ICB_code": "ICB"}

# List of valid output types as used in create_output_crosstab
OUTPUT_TYPE = ["Vaccinated", "Population", "Coverage"]

# Specify list of selective vaccinations
SELECTIVE_VACCS = ["BCG_12m", "BCG_3m", "HepB_Group2_12m", "HepB_Group2_24m"]

# Set which vaccine populations to use when defining population for that
# child age in published dashboard and non BCG/HepB published csv outputs
POPULATION_VACCINES = {"12m_Eligible_Pop": "DTaP_IPV_Hib_HepB_12m",
                       "24m_Eligible_Pop": "DTaP_IPV_Hib_HepB_24m",
                       "5y_Eligible_Pop": "MMR1_5y"}


# --- Validations ---
# Specify list of vaccinations to exclude from validation outputs for all years
# NOTE - currently BCG_3m is included in validation outputs and internal dashboard data,
# but not public dashboard data
EXCLUDE_VACCS_VAL = ["BCG_12m", "HepB_12m", "HepB_24m", "HepB_Group1_12m",
                     "HepB_Group1_24m", "HepB_Group2_12m", "HepB_Group2_24m",
                     "MenC_12m", "PCV1_12m"]

# Set which vaccine populations to use when defining population for that
# child age in validation/internal dashboard outputs
POPULATION_VACCINES_VAL = {"BCG_3m_Eligible_Pop": "BCG_3m",
                           "12m_Eligible_Pop": "DTaP_IPV_Hib_HepB_12m",
                           "24m_Eligible_Pop": "DTaP_IPV_Hib_HepB_24m",
                           "5y_Eligible_Pop": "MMR1_5y"}

# Set any vac type updates for historical years for the YoY checks
# format = {vac type in previous years: vac type this year}
YOY_UPDATE_PREV_VAC_TYPE = {"DTaP_IPV_Hib_12m": "DTaP_IPV_Hib_HepB_12m",
                            "DTaP_IPV_Hib_24m": "DTaP_IPV_Hib_HepB_24m",
                            "PCV2_12m": "PCV_12m"}

# Set measures to perform YoY checks on
# NOTE - must be valid output types as specified in OUTPUT_TYPE above
YOY_MEASURE_TO_CHECK = ["Population", "Coverage"]

# Set limits to flag breaches outside of for YoY change outputs
# NOTE - process will flag any YoY changes >= limit value
# Format = {measure: [lower limit, upper limit]}
YOY_BREACH_LIMITS = {
    "Population": [-10, 10],
    "Coverage": [-5, 5],
}

# Set primary and secondary course vaccinations to perform numerator check
# on (checks if primary vaccine <= secondary vaccine)
# format = {primary_vac_type: secondary_vac_type}
PRIM_SECOND_NUM_VACCS_TO_CHECK = {"DTaP_IPV_Hib_5y": "DTaP_IPV_5y",
                                  "MMR1_5y": "MMR2_5y"}
