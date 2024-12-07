from pathlib import Path
from typing import List

from sum_dirac_dfcoef.args import args
from sum_dirac_dfcoef.data import DataMO
from sum_dirac_dfcoef.header_info import HeaderInfo
from sum_dirac_dfcoef.utils import debug_print


class OutputFileWriter:
    """This class has methods to write data to the output file."""

    def __init__(self) -> None:
        super().__init__()
        self.output_path = self.get_output_path()

    def write_no_header_info(self) -> None:
        # Print NO_HEADERINFO twice because the first and second lines are used for the header
        # If user uses --no-scf option, we cannot get the eigenvalues and the number of electrons from the output file.
        # Therefore, print NO_HEADERINFO twice to avoid using the output file for dcaspt2_input_generator program.
        with open(self.output_path, "a", encoding="utf-8") as f:
            msg = "NO_HEADERINFO: This output cannot be used for the dcaspt2_input_generator program.\n"
            f.write(msg)
            f.write(msg)

    def write_headerinfo(self, header_info: HeaderInfo) -> None:
        with open(self.output_path, "a", encoding="utf-8") as f:
            scheme = "default" if header_info.scheme.value == 0 else str(header_info.scheme.value)
            line = f"electron_num {header_info.electrons} point_group {header_info.point_group} moltra_scheme {scheme}\n"
            for symmetry_type, d in header_info.moltra_info.range_dict.items():
                line += f"{symmetry_type} {d} "
            line += "\n"
            for symmetry_type, d in header_info.eigenvalues.shell_num.items():
                line += f"{symmetry_type} "
                for eigenvalue_type, num in d.items():
                    # only write closed, open, virtual (positive energy eigenvalues)
                    if eigenvalue_type in ("closed", "open", "virtual"):
                        line += f"{eigenvalue_type} {num} "
            line += "\n"
            f.write(line)

    def write_mo_data(self, mo_data: List[DataMO]) -> None:
        with open(self.output_path, "a", encoding="utf-8") as f:
            f.write("\n")
            for mo in mo_data:
                digit_int = len(str(int(mo.mo_energy)))  # number of digits of integer part
                # File write but if args.compress is True \n is not added
                mo_info_energy = f"{mo.mo_info} {mo.mo_energy:{digit_int}.{args.decimal}f}" + ("\n" if not args.compress else "")
                f.write(mo_info_energy)

                for key, coef in mo.coef_dict.items():
                    percentage = coef / mo.norm_const_sum * 100
                    atom_num_label = f"({key.atom_idx})" if key.need_identifier and not args.ignore_atom_num else ""
                    sym_label = key.symmetry_label if not args.ignore_sym else ""
                    ml_label = key.magnetic_label if not args.ignore_ml else ""
                    atomic_symmetry_label = f"{sym_label}{key.atom_label}{key.azimuthal_label}{ml_label}{atom_num_label}"
                    output_str: str
                    if args.compress:
                        output_str = f" {atomic_symmetry_label} {percentage:.{args.decimal}f}"
                    else:
                        output_str = f"{atomic_symmetry_label:<12} {percentage:{args.decimal+4}.{args.decimal}f} %\n"
                    f.write(output_str)
                f.write("\n")  # add empty line
                debug_print(f"sum of coefficient {mo.norm_const_sum:.{args.decimal}f}")

    def create_blank_file(self) -> None:
        # Open the file in write mode
        # Even if the file already exists, it will be overwritten with a blank file
        file = open(self.output_path, "w", encoding="utf-8")
        file.close()

    def get_output_path(self) -> Path:
        import sys

        if args.output is None:
            output_name = "sum_dirac_dfcoef.out"
            output_path = Path.absolute(Path.cwd() / output_name)
        else:
            output_path = Path(args.output).expanduser().resolve()
            if output_path.is_dir():
                sys.exit(
                    "ERROR: The path you specified as the sum_dirac_dfcoef output is a directory. Not a file.\
Please check your -o or --output option is correct."
                )

        return output_path


output_file_writer = OutputFileWriter()
