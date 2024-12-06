from __future__ import annotations

from typing import Any, ClassVar
from typing import TYPE_CHECKING
import warnings

from pyscipopt import Expr as Expression
from pyscipopt import Variable as _Variable

from quantagonia.enums import VarType
from quantagonia.mip.wrappers.wrapper_enums import GRB, PythonMipEnum, CplexEnum
from quantagonia.errors.errors import ModelError
from quantagonia.extras import SuppressScipOutput

if TYPE_CHECKING:
    from quantagonia.mip.model import Model


class Variable(_Variable):
    """A class representing a variable in a Mixed Integer Programming (MIP) problem."""

    _removed_attributes: ClassVar[set[str]] = {
        "isInLP",
        "getCol",
        "ptr",
        "isOriginal",
        "getIndex",
        "getLbGlobal",
        "getUbGlobal",
        "getLbLocal",
        "getUbLocal",
        "getLPSol",
        "getAvgSol",
        "varMayRound",
        "degree",
        "getLbOriginal",
        "getUbOriginal",
        "getObj",
        "normalize",
        "data",
    }

    def __init__(
        self,
        variable: _Variable = None,
        model: Model = None,
    ):
        """Initializes a Variable instance."""
        self._variable = variable
        self._model = model
        super().__init__()

        for attr in self._removed_attributes:
            if attr in self.__dict__:
                del self.__dict__[attr]

    def __getattribute__(self, name: str) -> Any:  # noqa: ANN401
        if name in Variable._removed_attributes:
            msg = f"Variable object has no attribute '{name}'"
            raise AttributeError(msg)
        return super().__getattribute__(name)

    def __dir__(self):
        return [attr for attr in super().__dir__() if attr not in Variable._removed_attributes]

    @property
    def name(self) -> str:
        """The name of the variable.

        Returns:
            str: The name of the variable.

        Raises:
            ModelError: If the variable is not set or if the variable data are not set.
        """
        if self._variable is None:
            msg = "Variable is not set."
            raise ModelError(msg)
        return self._variable.name

    # Gurobipy interface
    @property
    def VarName(self) -> str:  # noqa: N802
        """The name of the variable.

        Returns:
            str: The name of the variable.
        """
        return self.name

    @property
    def lb(self) -> float:
        """The lower bound of the variable.

        This property allows getting and setting the lower bound of the variable.

        Returns:
            float: The lower bound of the variable.

        Sets:
            float: The new lower bound value for the variable.

        Raises:
            ModelError: If setting the lower bound fails or if the variable data are not set.
        """
        if self._variable is None:
            msg = "Variable is not set."
            raise ModelError(msg)
        return self._variable.getLbOriginal()

    @lb.setter
    def lb(self, value: float) -> None:
        """Set the lower bound of the variable."""
        if self._model.model is None:
            msg = "Model is not set."
            raise ModelError(msg)
        try:
            # Suppress SCIP output
            with SuppressScipOutput():
                self._model.model.chgVarLb(self._variable, value)
        except ValueError as e:
            error_message = f"Failed to set lower bound of variable {self._variable.name}"
            raise ModelError(error_message) from e

    # Gurobipy interface
    @property
    def LB(self) -> float:  # noqa: N802
        """The lower bound of the variable.

        Returns:
            float: The lower bound of the variable.
        """
        return self.lb

    # Gurobipy interface
    @LB.setter
    def LB(self, value: float) -> None:  # noqa: N802
        """Set the lower bound of the variable."""
        self.lb = value

    @property
    def ub(self) -> float:
        """The upper bound of the variable.

        This property allows getting and setting the upper bound of the variable.

        Returns:
            float: The upper bound of the variable.

        Sets:
            float: The new upper bound value for the variable.

        Raises:
            ModelError: If setting the upper bound fails or if the variable data are not set.
        """
        if self._variable is None:
            msg = "Variable is not set."
            raise ModelError(msg)
        return self._variable.getUbOriginal()

    @ub.setter
    def ub(self, value: float) -> None:
        """Set the upper bound of the variable."""
        if self._model is None:
            msg = "Model is not set."
            raise ModelError(msg)
        try:
            # Suppress SCIP output
            with SuppressScipOutput():
                self._model.model.chgVarUb(self._variable, value)
        except ValueError as e:
            error_message = f"Failed to set upper bound of variable {self._variable.name}"
            raise ModelError(error_message) from e

    # Gurobipy interface
    @property
    def UB(self) -> float:  # noqa: N802
        """The upper bound of the variable.

        Returns:
            float: The upper bound of the variable.
        """
        return self.ub

    # Gurobipy interface
    @UB.setter
    def UB(self, value: float) -> None:  # noqa: N802
        """Set the upper bound of the variable."""
        self.ub = value

    @property
    def obj(self) -> float:
        """The coefficient of the variable in the objective function.

        This property allows getting and setting the coefficient of the variable
        in the objective function.

        Returns:
            float: The coefficient of the variable in the objective function.

        Sets:
            float: The new coefficient value for the variable in the objective function.

        Raises:
            ModelError: If setting the objective coefficient fails or if the variable data are not set.
        """
        if self._variable is None:
            msg = "Variable is not set."
            raise ModelError(msg)
        return self._variable.getObj()

    @obj.setter
    def obj(self, value: float) -> None:
        """Set the coefficient of the variable in the objective function."""
        if self._model is None:
            msg = "Model is not set."
            raise ModelError(msg)
        monomial = value * self._variable
        ref_sense = self._model.model.getObjectiveSense()
        try:
            # Suppress SCIP output
            with SuppressScipOutput():
                self._model.model.setObjective(expr=monomial, sense=ref_sense, clear=False)
        except ValueError as e:
            error_message = f"Failed to set objective coefficient of variable {self._variable.name}"
            raise ModelError(error_message) from e

    # Gurobipy interface
    @property
    def Obj(self) -> float:  # noqa: N802
        """The coefficient of the variable in the objective function.

        Returns:
            float: The coefficient of the variable in the objective function.
        """
        return self.obj

    # Gurobipy interface
    @Obj.setter
    def Obj(self, value: float) -> None:  # noqa: N802
        """Set the coefficient of the variable in the objective function."""
        self.obj = value

    @property
    def sol_value(self) -> float:
        """The value of the variable in the current solution.

        Returns:
            float: The value of the variable in the current solution.

        Raises:
            ModelError: If the model is not set.
        """
        if self._model is None:
            msg = "Model is not set."
            raise ModelError(msg)
        return self._model.solution[self.name]

    # Gurobipy interface
    @property
    def X(self) -> float:  # noqa: N802
        """The value of the variable in the current solution.

        Returns:
            float: The value of the variable in the current solution.

        Raises:
            ModelError: If the model is not set.
        """
        return self.sol_value

    # python-mip interface
    @property
    def x(self) -> float:
        """The value of the variable in the current solution.

        Returns:
            float: The value of the variable in the current solution.

        Raises:
            ModelError: If the model is not set.
        """
        return self.sol_value

    @property
    def var_type(self) -> VarType:
        """The type of the variable.

        This property allows getting and setting the type of the variable.

        Returns:
            VarType: The type of the variable (BINARY, INTEGER, or CONTINUOUS).

        Sets:
            VarType: The new type for the variable.

        Raises:
            ModelError: If the variable type is unsupported or if setting the type
            fails or if the variable data are not set.
        """
        if self._variable is None:
            msg = "Variable is not set."
            raise ModelError(msg)
        if self._variable.vtype() == "BINARY":
            if self._model.type == "BaseModel":
                return VarType.BINARY
            if self._model.type == "GurobipyModel":
                return GRB.BINARY
            if self._model.type == "CplexModel":
                return CplexEnum.BINARY
            if self._model.type == "PythonMipModel":
                return PythonMipEnum.BINARY
        if self._variable.vtype() == "INTEGER":
            if self._model.type == "BaseModel":
                return VarType.INTEGER
            if self._model.type == "GurobipyModel":
                return GRB.INTEGER
            if self._model.type == "CplexModel":
                return CplexEnum.INTEGER
            if self._model.type == "PythonMipModel":
                return PythonMipEnum.INTEGER
        if self._variable.vtype() == "CONTINUOUS":
            if self._model.type == "BaseModel":
                return VarType.CONTINUOUS
            if self._model.type == "GurobipyModel":
                return GRB.CONTINUOUS
            if self._model.type == "CplexModel":
                return CplexEnum.CONTINUOUS
            if self._model.type == "PythonMipModel":
                return PythonMipEnum.CONTINUOUS
        error_message = f"Unsupported variable type: {self._variable.vtype()}."
        raise ModelError(error_message)

    @var_type.setter
    def var_type(self, value: VarType | GRB | CplexEnum | PythonMipEnum) -> None:
        """Set the type of the variable."""
        if self._model is None:
            msg = "Model is not set."
            raise ModelError(msg)
        if value in [VarType.BINARY, GRB.BINARY, CplexEnum.BINARY, PythonMipEnum.BINARY]:
            vtype = "B"
        elif value in [VarType.INTEGER, GRB.INTEGER, CplexEnum.INTEGER, PythonMipEnum.INTEGER]:
            vtype = "I"
        elif value in [VarType.CONTINUOUS, GRB.CONTINUOUS, CplexEnum.CONTINUOUS, PythonMipEnum.CONTINUOUS]:
            vtype = "C"
        else:
            error_message = f"Unsupported variable type: {value}."
            raise ModelError(error_message)
        try:
            # Suppress SCIP output
            with SuppressScipOutput():
                self._model.model.chgVarType(self._variable, vtype)
        except ValueError as e:
            error_message = f"Failed to set variable type of variable {self._variable.name}"
            raise ModelError(error_message) from e

    # Gurobipy interface
    @property
    def VType(self) -> GRB:  # noqa: N802
        """The type of the variable.

        Returns:
            GRB: The type of the variable.
        """
        vtype = self.var_type
        if vtype in [VarType.BINARY, GRB.BINARY, CplexEnum.BINARY, PythonMipEnum.BINARY]:
            return GRB.BINARY
        if vtype in [VarType.INTEGER, GRB.INTEGER, CplexEnum.INTEGER, PythonMipEnum.INTEGER]:
            return GRB.INTEGER
        if vtype in [VarType.CONTINUOUS, GRB.CONTINUOUS, CplexEnum.CONTINUOUS, PythonMipEnum.CONTINUOUS]:
            return GRB.CONTINUOUS
        msg = "Unsupported variable type."
        raise ModelError(msg)

    # Gurobipy interface
    @VType.setter
    def VType(self, value: GRB) -> None:  # noqa: N802
        """Set the type of the variable."""
        self.var_type = value

    @property
    def index(self) -> int:
        """The index of the variable.

        Returns:
            int: The index of the variable.

        Raises:
            ModelError: If the variable is not set or if the variable data are not set.
        """
        if self._variable is None:
            msg = "Variable is not set."
            raise ModelError(msg)
        return self._variable.getIndex()

    # Gurobipy interface
    @property
    def Start(self) -> float:  # noqa: N802
        """The starting value of the variable.

        Returns:
            float: The starting value of the variable.
        """
        msg = "The starting value of the variable is not supported."
        warnings.warn(msg, stacklevel=2)
        return 0.0

    # Gurobipy interface
    @Start.setter
    def Start(self, value: float) -> None:  # noqa: N802, ARG002
        """Set the starting value of the variable."""
        msg = "The starting value of the variable is not supported."
        warnings.warn(msg, stacklevel=2)
        pass

    def is_equal(self, other: Variable) -> bool:
        """Check if two variables are equal.

        Args:
            other (Variable): The other variable to compare.

        Returns:
            bool: True if the two variables are equal, False otherwise.
        """
        return self._variable is other._variable  # noqa: SLF001

    def __add__(self, other: Variable) -> Expression:
        """Add two variables or a variable and a constant."""
        if not isinstance(other, Variable):
            return NotImplemented
        return self._variable + other._variable

    def __sub__(self, other: Variable) -> Expression:
        """Subtract two variables or a variable and a constant."""
        if not isinstance(other, Variable):
            return NotImplemented
        return self._variable - other._variable

    def __mul__(self, other: float) -> Expression:
        """Multiply a variable by a constant."""
        if not isinstance(other, (int, float)):
            return NotImplemented
        return other * self._variable

    def __radd__(self, other: Variable) -> Expression:
        """Add a variable and a constant."""
        return self.__add__(other)

    def __rsub__(self, other: Variable) -> Expression:
        """Subtract a variable and a constant."""
        if not isinstance(other, Variable):
            return NotImplemented
        return other._variable - self._variable

    def __rmul__(self, other: float) -> Expression:
        """Multiply a variable by a constant."""
        return self.__mul__(other)
