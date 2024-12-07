#!/usr/bin/env python3
from sum_dirac_dfcoef.args import args
from sum_dirac_dfcoef.file_writer import output_file_writer
from sum_dirac_dfcoef.functions_info import get_functions_info
from sum_dirac_dfcoef.header_info import HeaderInfo
from sum_dirac_dfcoef.privec_reader import PrivecProcessor
from sum_dirac_dfcoef.utils import get_dirac_filepath, should_write_electronic_results_to_file, should_write_positronic_results_to_file


def main() -> None:
    dirac_filepath = get_dirac_filepath()
    dirac_output = open(dirac_filepath, encoding="utf-8")
    dirac_output.seek(0)  # rewind to the beginning of the file
    header_info = HeaderInfo()
    if args.for_generator:
        header_info.read_header_info(dirac_output)
    dirac_output.seek(0)
    functions_info = get_functions_info(dirac_output)
    output_file_writer.create_blank_file()

    dirac_output_lines = dirac_output.readlines()
    # Read coefficients from the output file of DIRAC and store them in data_all_mo.
    privec_processor = PrivecProcessor(dirac_output_lines, functions_info, header_info.eigenvalues)
    privec_processor.read_privec_data_wrapper()

    # Write the header information to the output file.
    if args.for_generator:
        header_info.calculate_moltra_idx_range(privec_processor.data_all_mo)
        output_file_writer.write_headerinfo(header_info)
    else:
        # If the output file is not for dcaspt2_input_generator, don't write header information.
        output_file_writer.write_no_header_info()

    # Sort the MOs by energy.
    if not args.no_sort:
        privec_processor.data_all_mo.sort_mo_energy()

    # Write the MO data to the output file.
    if should_write_electronic_results_to_file():
        output_file_writer.write_mo_data(privec_processor.data_all_mo.electronic)
    if should_write_positronic_results_to_file():
        output_file_writer.write_mo_data(privec_processor.data_all_mo.positronic)
