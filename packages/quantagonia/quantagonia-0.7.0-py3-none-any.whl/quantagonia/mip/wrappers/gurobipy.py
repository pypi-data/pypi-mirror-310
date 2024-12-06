from __future__ import annotations

from itertools import product
from collections.abc import Iterable
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyscipopt import Expr as Expression

from quantagonia.mip.model import Model as BaseModel
from quantagonia.mip.variable import Variable
from quantagonia.errors.errors import ModelError
from quantagonia.mip.wrappers.tupledict import tupledict
from quantagonia.mip.wrappers.wrapper_enums import GRB, hybridsolver_status_to_grb, hybridsolver_sense_to_grb


class Model(BaseModel):
    """Wrapper for gurobipy.Model."""

    def __init__(self, name: str = "Model") -> None:
        super().__init__(name)
        self._type = "GurobipyModel"

    @property
    def ObjVal(self) -> float:  # noqa: N802
        """The objective value of the model's best solution.

        Returns:
            float: The objective value of the best solution found.
        """
        return self.objective_value

    @property
    def ModelSense(self) -> GRB:  # noqa: N802
        """The optimization sense of the model.

        Returns:
            GRB: The current optimization sense of the model.

        Raises:
            ModelError: If the current sense is unsupported.
        """
        return hybridsolver_sense_to_grb[self.sense]

    @ModelSense.setter
    def ModelSense(self, sense: GRB) -> None:  # noqa: N802
        """Sets the optimization sense of the model.

        Args:
            sense (HybridSolverOptSenses): The optimization sense to be set.

        Raises:
            ModelError: If the provided sense is unsupported.
        """
        self.set_sense(sense)

    @property
    def ObjConst(self) -> float:  # noqa: N802
        """The offset of the objective function.

        Returns:
            float: The constant offset value of the objective function.
        """
        return self.objective_offset

    @property
    def numVars(self) -> int:  # noqa: N802
        """The number of variables in the model.

        Returns:
            int: The number of variables in the model.
        """
        return self.n_variables

    @property
    def numvars(self) -> int:
        """The number of variables in the model.

        Returns:
            int: The number of variables in the model.
        """
        return self.n_variables

    @property
    def status(self) -> GRB:
        """The solution status of the model.

        Returns:
            GRB: The current solution status of the model.
        """
        return hybridsolver_status_to_grb[self.solution_status]

    def getAttr(self, attr: str, var_list: tupledict | Variable) -> dict | float | str:  # noqa: N802
        """
        Retrieves the specified attribute for a tupledict of variables or a single variable.

        Args:
            attr (str): The name of the attribute to retrieve (e.g., "X" for solution values).
            var_list (tupledict | Variable): A tupledict of variables or a single variable.

        Returns:
            dict | Any: If `var_list` is a tupledict, returns a dictionary mapping keys to
                        attribute values. If `var_list` is a single variable, returns the
                        attribute value for that variable.

        Raises:
            ValueError: If `var_list` is neither a tupledict nor a Variable.
            AttributeError: If the attribute is not valid for the variables.
        """
        if isinstance(var_list, tupledict):
            return {key: getattr(var, attr) for key, var in var_list.items()}
        if isinstance(var_list, Variable):
            return getattr(var_list, attr)
        msg = "Expected a tupledict or a single Variable."
        raise ModelError(msg)

    def addVar(  # noqa: N802
        self,
        lb: float = 0,
        ub: float = float("Inf"),
        obj: float = 0,
        vtype: GRB = GRB.CONTINUOUS,
        name: str = "",
    ) -> Variable:
        """Adds a new variable to the model.

        Args:
            lb (float): The lower bound of the variable. Defaults to 0.
            ub (float): The upper bound of the variable. Defaults to positive infinity.
            obj (float): The coefficient of the variable in the objective function. Defaults to 0.
            name (str): The name of the variable. Defaults to an empty string.
            vtype (GRB): The type of the variable. Defaults to GRB.CONTINUOUS.

        Returns:
            Variable: The Variable instance that was added to the MIP model.

        Raises:
            ModelError: If the variable type is unsupported or if the variable addition fails.
        """
        return self.add_variable(lb, ub, name, obj, vtype)

    def addVars(  # noqa: N802
        self,
        *indices: str | int | range | list[int],
        lb: float = 0.0,
        ub: float = float("inf"),
        obj: float = 0.0,
        vtype: GRB = GRB.CONTINUOUS,
        name: str = "",
    ) -> tupledict:
        """
        Adds multiple variables to the model in a multi-dimensional array format.

        Args:
            *indices: Dimensions for the variable array, or a single list of index tuples.
            lb (float or list): Lower bound for variables, or list of bounds for each variable.
            ub (float or list): Upper bound for variables, or list of bounds for each variable.
            obj (float or list): Objective coefficient for variables, or list of coefficients for each variable.
            vtype (GRB or list): Variable type, or list of types for each variable.
            name (str or list): Base name for each variable, or list of names for each variable.

        Returns:
            tupledict: Dictionary-like structure with keys as index tuples and values as Variable instances.

        Raises:
            ValueError: If indices contain invalid entries or if list lengths of
            lb, ub, obj, vtype, and name don't match.
        """

        # Helper to verify if an item is scalar or iterable (for lists)
        def is_scalar(value: float | str) -> bool:
            return isinstance(value, (int, float, str))

        # Ensure lb, ub, obj are flattened arrays/matrices
        def flatten(param: float | list[float] | np.ndarray) -> list[float]:
            if isinstance(param, (list, np.ndarray)):
                return list(np.array(param).flatten())
            return [param]  # Wrap scalar in a list for consistency

        lb = flatten(lb) if isinstance(lb, (list, np.ndarray)) else lb
        ub = flatten(ub) if isinstance(ub, (list, np.ndarray)) else ub
        obj = flatten(obj) if isinstance(obj, (list, np.ndarray)) else obj

        # Handle custom list of tuples as indices
        if len(indices) == 1 and isinstance(indices[0], list) and all(isinstance(i, tuple) for i in indices[0]):
            # Check that each tuple contains only scalar values, raise error if not
            for idx_tuple in indices[0]:
                if not all(is_scalar(element) for element in idx_tuple):
                    msg = "Each index tuple must contain only scalar values (int, float, str). "
                    "Nested tuples are not allowed."
                    raise ModelError(msg)
            index_combinations = indices[0]
        else:
            # Convert integer indices into ranges and validate lists of scalars
            dimensions = [range(i) if isinstance(i, int) else i for i in indices]
            for idx in dimensions:
                if isinstance(idx, Iterable) and not all(is_scalar(i) for i in idx):
                    msg = "Each entry in *indices must be a scalar, a range, or a list of scalars (int, float, str)."
                    raise ModelError(msg)
            index_combinations = list(product(*dimensions))

        num_vars = len(index_combinations)

        # Ensure that list arguments (if provided) match the number of variables
        lb = lb if isinstance(lb, list) else [lb] * num_vars
        ub = ub if isinstance(ub, list) else [ub] * num_vars
        obj = obj if isinstance(obj, list) else [obj] * num_vars
        vtype = vtype if isinstance(vtype, list) else [vtype] * num_vars
        name = name if isinstance(name, list) else [name] * num_vars

        # Check for matching lengths if lists are provided
        for param, param_name in zip([lb, ub, obj, vtype, name], ["lb", "ub", "obj", "vtype", "name"]):
            if len(param) != num_vars:
                msg = f"Length of '{param_name}' list must match the number of variables ({num_vars})."
                raise ModelError(msg)

        # Create variables based on index combinations and parameters
        variable_dict = tupledict()
        for idx_tuple, lb_val, ub_val, obj_val, vtype_val, name_val in zip(
            index_combinations, lb, ub, obj, vtype, name
        ):
            # If only one index, unpack tuple to get a single key
            key = idx_tuple[0] if len(idx_tuple) == 1 else idx_tuple

            # Generate a unique name for each variable if a name base is provided
            var_name = f"{name_val}[{','.join(map(str, idx_tuple))}]" if name_val else ""

            # Add the variable to the model and store it in the CustomDict
            variable = self.add_variable(lb=lb_val, ub=ub_val, name=var_name, coeff=obj_val, var_type=vtype_val)
            variable_dict[key] = variable

        return variable_dict

    def getVars(self) -> list[Variable]:  # noqa: N802
        """Returns a list of all variables in the model.

        Returns:
            list[Variable]: A list of all variables in the model.
        """
        return self.get_variables()

    def addConstr(self, expr: Expression, name: str = "") -> None:  # noqa: N802
        """Adds a constraint to the model.

        Args:
            expr (Expression): The expression representing the constraint.
            name (str): (optional) The name of the constraint.

        Raises:
            ModelError: If the constraint addition fails.
        """
        self.add_constraint(expr, name)

    def addConstrs(self, generator: Iterable[Expression], name: str = "") -> None:  # noqa: N802
        """
        Adds multiple constraints to the model using a generator.

        Args:
            generator (Generator[Expression, None, None]): A generator yielding
                constraint expressions.
            name (str): (optional) A prefix for the constraint names.
        """
        if not generator:
            msg = "No constraints provided."
            raise ModelError(msg)

        for i, expr in enumerate(generator, start=1):  # Start index from 1
            constraint_name = f"{name}_{i}" if name else ""
            try:
                self.add_constraint(expr, constraint_name)
            except ModelError as e:
                error_message = f"Failed to add constraint '{constraint_name}'."
                raise ModelError(error_message) from e

    def setObjective(self, expr: Expression, sense: GRB = GRB.MINIMIZE) -> None:  # noqa: N802
        """Sets the objective function for the model.

        Args:
            expr (Expression): The expression representing the objective function.
            sense (GRB): The optimization sense (minimize or maximize).
                Defaults to GRB.MINIMIZE.

        Raises:
            ModelError: If the sense is unsupported or if setting the objective fails.
        """
        self.set_objective(sense, expr)

    def optimize(self) -> GRB:
        """Sends the model to the HybridSolver and solves it on the cloud.

        Returns:
            GRB: The solution status after optimization.

        Raises:
            ValueError: If the solution status cannot be cast to HybridSolverStatus.
        """
        return hybridsolver_status_to_grb[self._optimize()]
