import time
import timeit
import logging
import xlwings as xw
import pandas as pd

from child_vac_code.utilities import logger_config
import child_vac_code.parameters as param
import child_vac_code.utilities.validations.validations_data as val_data
from child_vac_code.utilities import helpers, load, pre_processing, dashboards
from child_vac_code.utilities.write import write_data


def main():

    # Load frequently used parameters
    # Load reporting financial year start date
    fyear_start = param.FYEAR_START

    # Load run parameters
    run_main_vals = param.RUN_MAIN_VALIDATIONS
    run_outliers = param.RUN_OUTLIERS
    run_internal_dash = param.RUN_INTERNAL_DASH
    # Set filepaths
    main_vals_filepath = param.MAIN_VALIDATION_FILEPATH
    dashboard_data_internal_filepath = param.DASHBOARD_DATA_INTERNAL_FILEPATH

    # Set combine_small_LAs to False so they're not combined in validation outputs
    combine_small_las = False

    # Convert the financial year start to financial year
    fyear = helpers.fyearstart_to_fyear(fyear_start)

    # Import organisation reference data for current year and
    # apply pre-processing updates
    df_org_ref = pre_processing.create_org_ref_data(fyear, combine_small_las)
    # Add to cache for future use (e.g. in processing.select_org_ref_data)
    helpers.create_folder("cached_dataframes/")
    df_org_ref.to_feather('cached_dataframes/df_org_ref.ft')
    # Import details of any LAs that need their vaccine status updating
    df_status_updates = load.import_vaccine_status_updates()

    # Import the raw COVER data for the current year
    df_cover_raw = load.import_raw_cover_data(fyear_start)
    # Apply pre-processing to raw data
    df_cover_raw = pre_processing.update_child_vac_data_raw(df_cover_raw, df_org_ref)

    # Select number of years to import from asset
    # Set default values of 0
    num_years_main_yoy = 0
    num_years_outlier = 0
    num_years_internal_dash = 0
    # Update based on which run flags are set
    if run_main_vals:
        num_years_main_yoy = param.TS_YEARS_VAL_MAIN_YOY
    if run_outliers:
        num_years_outlier = param.TS_YEARS_VAL_OUTLIERS
    if run_internal_dash:
        num_years_internal_dash = param.TS_YEARS_INTERNAL_DASH

    # Get max number of years required
    num_years = max([num_years_main_yoy, num_years_outlier, num_years_internal_dash])

    # Generate year range required and extract data from asset
    fyear_start_range = helpers.get_year_range(fyear_start, num_years)
    df_cover_asset = load.import_asset_data(fyear_start_range)
    # Apply pre-processing to historical asset data
    df_cover_asset = pre_processing.update_child_vac_data(df_cover_asset,
                                                          df_org_ref,
                                                          df_status_updates,
                                                          combine_small_las)

    # Remove any data for current year from historical data imported from asset
    # (in case the raw data being validated is a resubmission)
    df_cover_asset = df_cover_asset[
        df_cover_asset["FinancialYearStart"] != param.FYEAR_START].copy()

    # Combine raw and historical data
    df_combined = pd.concat([df_cover_raw, df_cover_asset])
    # Apply pre-processing updates to combined data
    df_combined = pre_processing.update_child_vac_data_combined(df_combined)

    # Run the validation outputs as per the run flags
    if run_outliers:
        # Run the outliers
        # (function will also output to and save Excel file in Validations folder)
        val_data.create_outliers(df_combined)

    if run_main_vals:
        # Run each main validation check as defined by the items in get_validations_main
        # and output to main validations file
        all_main_vals = val_data.get_validations_main()
        write_data.write_outputs(df_combined,
                                 all_main_vals,
                                 main_vals_filepath,
                                 fyear)

        # Save the main validations file with the updated outputs
        wb = xw.Book(main_vals_filepath)
        wb.save()

    if run_internal_dash:
        # Run Excel outputs used for internal PowerBI dashboard file as defined by items
        # in get_dashboards_internal_input
        all_dbs = dashboards.get_dashboards_internal_input()
        write_data.write_outputs(df_combined, all_dbs,
                                 dashboard_data_internal_filepath, fyear)

        # Save the internal dashboard data file with the updated outputs
        wb = xw.Book(dashboard_data_internal_filepath)
        wb.save()

    # Close Excel after all outputs run
    xw.apps.active.quit()

    # Remove the cached dataframe folder and all it's contents
    helpers.remove_folder("cached_dataframes/")


if __name__ == "__main__":
    # Setup logging
    formatted_time = time.strftime("%Y%m%d-%H%M%S")
    logger = logger_config.setup_logger(
        # Setup file & path for log, as_posix returns the path as a string
        file_name=(
            param.OUTPUT_DIR / "Logs" /
            f"childhood_vaccinations_create_val_{formatted_time}.log"
        ).as_posix())

    start_time = timeit.default_timer()
    main()
    total_time = timeit.default_timer() - start_time
    logging.info(
        f"Running time of create_validations: {int(total_time / 60)} minutes and {round(total_time%60)} seconds.")
    logger_config.clean_up_handlers(logger)
