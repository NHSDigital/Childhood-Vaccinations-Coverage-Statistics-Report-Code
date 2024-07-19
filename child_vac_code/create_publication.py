import time
import timeit
import logging
from child_vac_code.utilities import logger_config
import child_vac_code.parameters as param
from child_vac_code.utilities import load, pre_processing, helpers
from child_vac_code.utilities import tables, charts, csvs, dashboards
import child_vac_code.utilities.publication_files as publication
from child_vac_code.utilities.write import write_data
import xlwings as xw


def main():

    # Created a temp folder for storing cached dataframes
    # (will be removed at end).
    helpers.create_folder("cached_dataframes/")

    # Load frequently used parameters

    # Load reporting financial year start date and financial year
    fyear_start = param.FYEAR_START
    fyear = helpers.fyearstart_to_fyear(fyear_start)

    # Load template/main file location parameters
    tables_template = param.TABLE_TEMPLATE
    charts_template = param.CHART_TEMPLATE
    csv_output_path = param.CSV_DIR
    template_output_path = param.TEMPLATE_DIR
    dashboard_data_template = param.DASHBOARD_TEMPLATE
    # Load run parameters
    run_tables_cover = param.RUN_TABLES_COVER
    run_tables_flu = param.RUN_TABLES_FLU
    run_csvs_cover = param.RUN_CSVS_COVER
    run_charts_cover = param.RUN_CHARTS_COVER
    run_charts_flu = param.RUN_CHARTS_FLU
    run_dashboards_cover = param.RUN_DASHBOARDS_COVER
    run_pub_chart_outputs = param.RUN_PUBLICATION_CHARTS_OUTPUTS
    run_pub_table_outputs = param.RUN_PUBLICATION_TABLES_OUTPUTS

    # Create source data processing run flags and set default to False
    process_cover = False
    process_flu = False

    # Change source data processing run flags to true based on param. elements
    if (run_tables_cover or run_csvs_cover or run_charts_cover or run_dashboards_cover):
        process_cover = True
    if (run_tables_flu or run_charts_flu):
        process_flu = True

    if process_cover or process_flu:
        # Import organisation reference data and apply pre-processing updates
        df_org_ref = pre_processing.create_org_ref_data(fyear)
        # Add to cache for future use
        df_org_ref.to_feather('cached_dataframes/df_org_ref.ft')
        # Import details of any LAs that need their vaccine status updating
        df_status_updates = load.import_vaccine_status_updates()

    # Import and apply pre-processing to child vaccs data based on process
    # run flags
    if process_cover:
        # Import the childhood vaccinations COVER source data
        fyear_start_range = helpers.get_year_range(fyear_start, param.TS_YEARS_PUB)
        df_cover_import = load.import_asset_data(fyear_start_range)
        # Apply pre-processing
        df_cover = pre_processing.update_child_vac_data(df_cover_import, df_org_ref,
                                                        df_status_updates)

    if process_flu:
        # Import the childhood vaccinations flu source data
        df_flu_import = load.import_flu()
        # Apply pre-processing
        df_flu = pre_processing.update_flu_vac_data(df_flu_import, df_org_ref, fyear)

    # Run each part of the pipeline as per the run flags
    if run_tables_cover:
        # Run the COVER tables as defined by the items in get_tables_cover
        all_tables = tables.get_tables_cover()
        write_data.write_outputs(df_cover, all_tables, tables_template, fyear)

    if run_tables_flu:
        # Run the flu tables as defined by the items in get_tables
        all_tables = tables.get_tables_flu()
        write_data.write_outputs(df_flu, all_tables, tables_template, fyear)

    if run_tables_cover or run_tables_flu:
        # Save the Excel master tables with the updated data and close Excel
        wb = xw.Book(tables_template)
        wb.save()
        # xw.apps.active.api.Quit()

    if run_csvs_cover:
        # Run the COVER csv's as defined by the items in get_csvs_cover
        all_csvs = csvs.get_csvs_cover()
        write_data.write_outputs(df_cover, all_csvs, csv_output_path, fyear)

    if run_charts_cover:
        # Run the COVER chart outputs as defined by the items in get_charts_cover
        all_charts = charts.get_charts_cover()
        write_data.write_outputs(df_cover, all_charts, charts_template, fyear)

    if run_charts_flu:
        # Run the flu chart outputs as defined by the items in get_charts_flu
        all_charts = charts.get_charts_flu()
        write_data.write_outputs(df_flu, all_charts, charts_template, fyear)

    if run_charts_cover or run_charts_flu:
        # Save the Excel chart template file with the updated data
        wb = xw.Book(charts_template)
        wb.save()
        xw.apps.active.api.Quit()

    # Save the CMS publication ready chart files if required.
    if run_pub_chart_outputs:
        publication.save_chart_files(charts_template)

    if run_pub_table_outputs:
        publication.save_tables(tables_template)

    if run_dashboards_cover:
        # Run all dashboard outputs relating to COVER data
        # Run .csv outputs used for PowerBI map file as defined by items
        # in get_dashboards_map_input
        all_dbs = dashboards.get_dashboards_map_input()
        write_data.write_outputs(df_cover, all_dbs, template_output_path, fyear)

        # Run Excel outputs used for PowerBI dashboard file as defined by items
        # in get_dashboards_input
        all_dbs = dashboards.get_dashboards_input()
        write_data.write_outputs(df_cover, all_dbs, dashboard_data_template, fyear)

        # Save the Excel dashboard template with the updated data
        wb = xw.Book(dashboard_data_template)
        wb.save()
        # Close excel
        xw.apps.active.quit()

        # Create .csv version of dashboard data for publication, as defined by
        # items in get_dashboards_csv_pub
        all_dbs = dashboards.get_dashboards_csv_pub()
        write_data.write_outputs(df_cover, all_dbs, csv_output_path, fyear)

    # Remove the cached dataframe folder and all it's contents
    helpers.remove_folder("cached_dataframes/")


if __name__ == "__main__":
    # Setup logging
    formatted_time = time.strftime("%Y%m%d-%H%M%S")
    logger = logger_config.setup_logger(
        # Setup file & path for log, as_posix returns the path as a string
        file_name=(
            param.OUTPUT_DIR / "Logs" /
            f"childhood_vaccinations_create_pub_{formatted_time}.log"
        ).as_posix())

    start_time = timeit.default_timer()
    main()
    total_time = timeit.default_timer() - start_time
    logging.info(
        f"Running time of create_publication: {int(total_time / 60)} minutes and {round(total_time%60)} seconds.")
    logger_config.clean_up_handlers(logger)
