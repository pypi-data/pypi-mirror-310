from collections import OrderedDict
from typing import Optional, Set
from typing import OrderedDict as ODict

from pydantic import BaseModel, validator

from sum_dirac_dfcoef.subshell import subshell_order


class FuncIndices:
    """Class for storing the first and last function indices of the specified atom label(AtomInfo).

    Attributes:
        first (int): The first function index of the specified atom label.
        last (int): The last function index of the specified atom label.
    """

    first: int
    last: int

    def __init__(self, first: int = 0, last: int = 0) -> None:
        self.first = first
        self.last = last

    def __repr__(self) -> str:
        return f"FunIndices(first: {self.first}, last: {self.last})"


class AtomInfo:
    """Class for handling the information of the specified atom label.

    This class is used for FunctionInfo class and PrivecProcessor class.

    Attributes:
        idx_within_same_atom (int): Index of the order of atoms in the same AtomLabel
        label (str): The label of the specified atom label.
        mul (int): The multiplicity of the specified atom label.
        functions (ODict[str, int]): The number of functions of the specified atom label.
        func_idx_dirac21 (FuncIndices): The first and last function indices of the specified atom label. (For DIRAC >= 21)
        func_idx_dirac19 (FuncIndices): The first and last function indices of the specified atom label. (For DIRAC < 21)
    """

    idx_within_same_atom: int
    label: str
    mul: int
    functions: ODict[str, int]
    func_idx_dirac21: FuncIndices
    func_idx_dirac19: FuncIndices  # For DIRAC < 21

    def __init__(
        self,
        idx_within_same_atom: int = 0,
        label: str = "",
        multiplicity: int = 0,
        func_idx_dirac21: Optional[FuncIndices] = None,
        func_idx_dirac19: Optional[FuncIndices] = None,
    ) -> None:
        self.idx_within_same_atom = idx_within_same_atom
        self.label = label
        self.mul = multiplicity
        self.functions = OrderedDict()
        self.func_idx_dirac21 = func_idx_dirac21 if func_idx_dirac21 is not None else FuncIndices()
        self.func_idx_dirac19 = func_idx_dirac19 if func_idx_dirac19 is not None else FuncIndices()

    def __repr__(self) -> str:
        return f"AtomInfo(idx_within_same_atom {self.idx_within_same_atom}, label: {self.label}, mul: {self.mul}, \
func_idx_dirac21: {self.func_idx_dirac21}, func_idx_dirac19: {self.func_idx_dirac19}, functions: {self.functions})"

    def add_function(self, gto_type: str, num_functions: int) -> None:
        self.functions[gto_type] = num_functions

    def decrement_function(self, gto_type: str) -> None:
        try:
            self.functions[gto_type] -= 1
            if self.functions[gto_type] < 0:
                msg = f"Too many functions detected. self.functions[{gto_type}] must be >= 0, but got {self.functions[gto_type]}"
                raise ValueError(msg)
        except KeyError as e:
            msg = f"self.functions[{gto_type}] is not found in self.functions: {self.functions.keys()}"
            raise KeyError(msg) from e

    def get_remaining_functions(self) -> "ODict[str, int]":
        return OrderedDict({k: v for k, v in self.functions.items() if v > 0})


class AtomicOrbital(BaseModel, validate_assignment=True):
    """Class for handling the information of the atomic orbital.

    Raises:
        ValueError: Raises an error if the subshell is not in the subshell_order.
        ValueError: Raises an error if the subshell is not one character.

    Attributes:
        atom (str): The label of the atom. (e.g. "C", "H", "He")
        subshell (str): The label of the subshell. (e.g. "s", "p", "d", "f")
        gto_type (str): The label of the GTO type. (e.g. "s", "px", "dxy", "fxxx")
    """

    atom: str = ""
    subshell: str = "s"
    gto_type: str = "s"

    @validator("subshell")
    def validate_subshell(cls, v: str) -> str:  # noqa: N805 (pydantic method)
        if v not in subshell_order.orbital_labels:
            msg = f"subshell must be one of '{subshell_order.orbital_labels}', but got '{v}'"
            raise ValueError(msg)
        if len(v) != 1:
            msg = f"subshell must be one character, but got '{v}'"
            raise ValueError(msg)
        return v

    def reset(self):
        self.atom = ""
        self.subshell = "s"
        self.gto_type = "s"

    def update(self, atom: str, subshell: str, gto_type: str):
        self.atom = atom
        self.subshell = subshell
        self.gto_type = gto_type


class AtomicOrbitals(BaseModel, validate_assignment=True):
    """Class for handling the information of the atomic orbitals.

    Main purpose of this class is to check if the current ao and the previous ao are the same atom.

    Attributes:
        prev_ao (AtomicOrbital): The previous atomic orbital.
        current_ao (AtomicOrbital): The current atomic orbital.
        idx_within_same_atom (int): The index of the order of atoms in the same AtomLabel.
        function_types (Set[str]): The set of function types.

    Methods:
        reset: Reset the AtomicOrbitals instance.
        is_different_atom: Check if the current ao and the previous ao are the same atom.
    """

    prev_ao: AtomicOrbital = AtomicOrbital()
    current_ao: AtomicOrbital = AtomicOrbital()
    idx_within_same_atom: int = 1
    function_types: Set[str] = set()

    def reset(self):
        self.prev_ao.reset()
        self.current_ao.reset()
        self.idx_within_same_atom = 1
        self.function_types.clear()

    def is_different_atom(self, function_label: str) -> bool:
        def is_reverse_subshell() -> bool:
            prev_subshell_idx = subshell_order.orbital_labels.index(self.prev_ao.subshell)
            current_subshell_idx = subshell_order.orbital_labels.index(self.current_ao.subshell)
            if prev_subshell_idx > current_subshell_idx:
                return True
            elif prev_subshell_idx < current_subshell_idx:
                return False
            else:  # Same subshell
                subshell_idx = subshell_order.orbital_labels.index(self.prev_ao.subshell)
                prev_gto_idx = subshell_order.gto_label_order[subshell_idx].index(self.prev_ao.gto_type)
                current_gto_idx = subshell_order.gto_label_order[subshell_idx].index(self.current_ao.gto_type)
                if prev_gto_idx > current_gto_idx:  # reverse subshell. e.g. self.prev_ato.gto_type = "pz", self.current_ao.gto_type = "px"
                    return True
                else:
                    return False

        if self.prev_ao.atom != self.current_ao.atom:
            return True
        elif function_label in self.function_types:
            # They have the same element label but different atoms.
            # Because the function_label of an atom is combined in one line,
            # it is a different atom if the same function_label appears.
            return True
        elif is_reverse_subshell():
            # e.g. "C  p" -> "C  s"
            # Different atom
            return True
        return False  # Same atom


ao = AtomicOrbitals()
