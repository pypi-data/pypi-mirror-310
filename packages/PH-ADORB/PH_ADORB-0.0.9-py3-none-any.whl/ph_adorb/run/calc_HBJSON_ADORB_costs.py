# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""A script to calculate ADORB Costs from a Honeybee-Model-HBJSON-File, and outputs to CSV files.

This script is called from the command line with the following arguments:
    * [1] (str): The path to the HBJSON file to read in.
    * [2] (str): The path to the EnergyPlus SQL file to read in.
    * [3] (str): The path to the output Yearly CSV file.
    * [4] (str): The path to the output Cumulative CSV file.
    * [5] (str): The path to the output folder for the preview tables.
"""

import os
import shutil
import sys
from pathlib import Path
from collections import namedtuple
import logging
from logging import getLogger

from ph_adorb.from_HBJSON import create_variant, read_HBJSON_file
from ph_adorb.variant import calc_variant_yearly_ADORB_costs, calc_variant_cumulative_ADORB_costs


# Function to setup logger to output to a log file
def setup_logger(log_file_path: Path, _level: int = logging.INFO) -> logging.Logger:
    logging.basicConfig(
        filename=log_file_path, filemode="w", level=_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return getLogger(__name__)


class InputFileError(Exception):
    def __init__(self, path) -> None:
        self.msg = f"\nCannot find the specified HBJSON file:'{path}'"
        super().__init__(self.msg)


Filepaths = namedtuple("Filepaths", ["hbjson", "sql", "annual_csv", "cumulative_csv", "tables"])


def _remove_folder_and_contents(_folder: Path) -> None:
    """Remove all files in the specified folder."""
    print(f"\t>> Removing: {_folder}")
    shutil.rmtree(_folder)


def resolve_paths(_args: list[str]) -> Filepaths:
    """Sort out the file input and output paths. Make the output directory if needed.

    Arguments:
    ----------
        * _args (list[str]): sys.args list of input arguments.

    Returns:
    --------
        * Filepaths
    """

    assert len(_args) == 6, "Error: Incorrect number of arguments."

    # -----------------------------------------------------------------------------------
    # -- The HBJSON input file.
    hbjson_source_filepath = Path(_args[1])
    if not hbjson_source_filepath.exists():
        raise InputFileError(hbjson_source_filepath)

    # -----------------------------------------------------------------------------------
    # -- The EnergyPlus SQL input file.
    results_sql_file = Path(_args[2])
    if not results_sql_file.exists():
        raise InputFileError(results_sql_file)

    # -----------------------------------------------------------------------------------
    # -- Annual CSV output file:
    # -- If the folder of the target_csv_filepath does not exist, make it.
    target_annual_csv_filepath = Path(_args[3])
    target_dir = target_annual_csv_filepath.parent
    if not target_dir.exists():
        print(f"\t>> Creating the directory: {target_dir}")
        os.mkdir(target_dir)

    # -- If the target CSV already exists, delete it.
    if target_annual_csv_filepath.exists():
        print(f"\t>> Removing the existing CSV file: {target_annual_csv_filepath}")
        os.remove(target_annual_csv_filepath)

    # -----------------------------------------------------------------------------------
    # -- Cumulative CSV output file:
    target_cumulative_csv_filepath = Path(_args[4])
    target_dir = target_cumulative_csv_filepath.parent
    if not target_dir.exists():
        print(f"\t>> Creating the directory: {target_dir}")
        os.mkdir(target_dir)

    # -- If the target CSV already exists, delete it.
    if target_cumulative_csv_filepath.exists():
        print(f"\t>> Removing the existing CSV file: {target_cumulative_csv_filepath}")
        os.remove(target_cumulative_csv_filepath)

    # -----------------------------------------------------------------------------------
    # -- Preview-Tables output folder:
    target_tables_dir = Path(_args[5])
    if target_tables_dir.exists():
        _remove_folder_and_contents(target_tables_dir)

    print(f"\t>> Creating the directory: {target_tables_dir}")
    os.mkdir(target_tables_dir)

    return Filepaths(
        hbjson_source_filepath,
        results_sql_file,
        target_annual_csv_filepath,
        target_cumulative_csv_filepath,
        target_tables_dir,
    )


if __name__ == "__main__":
    print("- " * 50)
    print(f"\t>> Using Python: {sys.version}")
    print(f"\t>> Running the script: '{__file__.split('/')[-1]}'")
    print(f"\t>> With the arguments:")
    print("\n".join([f"\t\t{i} | {a}" for i, a in enumerate(sys.argv)]))

    # --- Input / Output file Path
    # -------------------------------------------------------------------------
    print("\t>> Resolving file paths...")
    file_paths = resolve_paths(sys.argv)

    # Setup logger to output to the same directory as the 'file_paths.annual_csv' location
    log_file_path = file_paths.annual_csv.parent / "calc_HBJSON_ADORB_costs.log"
    logger = setup_logger(log_file_path, logging.DEBUG)

    logger.info("Script started")

    print(f"\t>> Source HBJSON File: '{file_paths.hbjson}'")
    print(f"\t>> Source SQL File: '{file_paths.sql}'")
    print(f"\t>> Target CSV File (yearly): '{file_paths.annual_csv}'")
    print(f"\t>> Target CSV File (cumulative): '{file_paths.cumulative_csv}'")
    print(f"\t>> Target Tables Output Folder: '{file_paths.tables}'")

    # --- Read in the existing HB-JSON-File
    # -------------------------------------------------------------------------
    print(f"\t>> Loading the Honeybee-Model from the HBJSON file: {file_paths.hbjson}")
    hb_json_dict = read_HBJSON_file.read_hb_json_from_file(file_paths.hbjson)

    # -- Re-Build the Honeybee-Model from the HBJSON-Dict
    # -------------------------------------------------------------------------
    hb_model = read_HBJSON_file.convert_hbjson_dict_to_hb_model(hb_json_dict)
    print(f"\t>> Honeybee-Model '{hb_model.display_name}' successfully re-built from file.")

    # --- Generate the PH-ADORB-Variant from the Honeybee-Model
    revive_variant = create_variant.get_PhAdorbVariant_from_hb_model(hb_model, file_paths.sql)

    # --- Get the ADORB Costs for the PH-ADORB-Variant
    # -------------------------------------------------------------------------
    variant_yearly_ADORB_df = calc_variant_yearly_ADORB_costs(revive_variant, file_paths.tables)
    variant_cumulative_ADORB_df = calc_variant_cumulative_ADORB_costs(variant_yearly_ADORB_df)

    # --- Output the ADORB Costs to a CSV File
    # -------------------------------------------------------------------------
    variant_yearly_ADORB_df.to_csv(file_paths.annual_csv)
    variant_cumulative_ADORB_df.to_csv(file_paths.cumulative_csv)
    print("\t>> Done calculating the ADORB Costs. The CSV files have been saved.")
    print("- " * 50)
    logger.info("Script finished")
