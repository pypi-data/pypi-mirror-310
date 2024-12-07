import re
from io import TextIOWrapper

from sum_dirac_dfcoef.utils import (
    delete_dirac_input_comment_out,
    is_dirac_input_line_should_be_skipped,
    is_dirac_input_section,
    is_end_dirac_input_field,
    is_start_dirac_input_field,
    space_separated_parsing,
    space_separated_parsing_upper,
)


def get_electron_num_from_input(dirac_output: TextIOWrapper) -> int:
    """If users calculate SCF with open shell they must explicitly write the OPEN SHELL and CLOSED SHELL keywords
    in the input file. Therefore, we can get the electron number from the input file.

        Args:
            dirac_output (TextIOWrapper): Output file of DIRAC

        Returns:
            int: The number of electrons in the system
    """

    def get_a_natural_number(word: str) -> int:
        # OPEN SHELL and CLOSED SHELL electron number settings
        # must be written as a natural number (negative number is not allowed)
        regex_number = r"[-]?[0-9]+"
        match = re.search(regex_number, word)
        if match is None:
            msg = "Failed to get a number related to the electron number or spinor number from your DIRAC input file.\n\
Please check your DIRAC input file and try again.\n"
            raise ValueError(msg)
        number = int(match.group())
        if number < 0:
            msg = "The number of electrons in OPEN SHELL and CLOSED SHELL must be a natural number.\n\
But we found a negative number in your DIRAC input file.\n\
Please check your DIRAC input file and try again.\n"
            raise ValueError(msg)
        return number

    electron_num: int = 0
    is_closed_shell_section: bool = False
    is_openshell_section: bool = False
    num_of_open_shell: int = 0
    is_reach_input_field: bool = False
    is_scf_found: bool = False
    scf_detail_section: bool = False
    for line in dirac_output:
        no_comment_out_line = delete_dirac_input_comment_out(line)
        words = space_separated_parsing_upper(no_comment_out_line)

        if is_dirac_input_line_should_be_skipped(words):
            continue

        if is_start_dirac_input_field(no_comment_out_line):
            is_reach_input_field = True
            continue

        if is_end_dirac_input_field(no_comment_out_line):
            break  # end of input field

        if is_reach_input_field:
            if ".SCF" in words[0]:
                is_scf_found = True

            if is_dirac_input_section(words[0]):
                if "*SCF" in words[0]:
                    scf_detail_section = True
                else:
                    scf_detail_section = False

            if scf_detail_section:
                if is_openshell_section:
                    # open shell format
                    # https://diracprogram.org/doc/master/manual/wave_function/scf.html#open-shell
                    # .OPEN SHELL
                    # num_of_open_shell
                    # num_of_elec/irrep1_num_spinor irrep2_num_spinor ...
                    # We want to get only num_of_elec
                    if num_of_open_shell == 0:
                        num_of_open_shell = get_a_natural_number(words[0])
                    else:
                        electron_num += get_a_natural_number(words[0])
                        num_of_open_shell -= 1  # Got an electron_num, so decrease the num_of_open_shell
                        if num_of_open_shell == 0:  # Got all open shell electron_num
                            is_openshell_section = False

                if is_closed_shell_section:
                    # closed shell format
                    # https://diracprogram.org/doc/master/manual/wave_function/scf.html#closed-shell
                    # .CLOSED SHELL
                    # irrep1_num_spinor irrep2_num_spinor ...
                    for word in words:
                        electron_num += get_a_natural_number(word)
                    is_closed_shell_section = False

                # .CLOSED SHELL
                if ".CLOSED" == words[0] and "SHELL" in words[1]:
                    is_closed_shell_section = True

                # .OPEN SHELL
                if ".OPEN" == words[0] and "SHELL" in words[1]:
                    is_openshell_section = True
    if not is_scf_found:
        msg = "\nCannot find SCF calculation settings from your DIRAC input file written in your output file.\n\
we cannot get information about the electron number and orbital energy without SCF calculation.\n\
So we cannot continue this program because we need electron number and orbital energies to summarize DIRAC output.\n\
Please check your DIRAC input file and try again.\n\
If you want to use this program by using the output file without SCF calculation, please use --no-scf option.\n\
But you cannot use the output using --no-scf option to dcaspt2_input_generator program.\n"
        raise ValueError(msg)
    return electron_num


def get_electron_num_from_scf_field(dirac_output: TextIOWrapper) -> int:
    # https://gitlab.com/dirac/dirac/-/blob/79e6b9e27cf8018999ddca2aa72247ccfb9d2a2d/src/dirac/dirrdn.F#L2127
    # find "i.e. no. of electrons ="
    is_wave_function_module_reached: bool = False
    for line in dirac_output:
        words = space_separated_parsing(line)
        if "Wave function module" in line:
            is_wave_function_module_reached = True
            continue

        if is_wave_function_module_reached:
            if "i.e. no. of electrons" in line:
                # ["i.e.", "no.", "of", "electrons", "=", number]
                return int(words[5])
    msg = "\nCannot find electron number from your DIRAC output file.\n\
we cannot get information about the electron number and orbital energy without SCF calculation.\n\
So we cannot continue this program because we need electron number and orbital energies to summarize DIRAC output.\n\
Please check your DIRAC input file and try again.\n\
If you want to use this program by using the output file without SCF calculation, please use --no-scf option.\n\
But you cannot use the output using --no-scf option to dcaspt2_input_generator program.\n"
    raise ValueError(msg)
