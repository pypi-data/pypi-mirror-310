from collections.abc import Iterable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import ArgValue
from classiq.interface.model.quantum_statement import QuantumOperation

from classiq.model_expansions.capturing.mangling_utils import (
    demangle_handle,
    mangle_captured_var_name,
)
from classiq.model_expansions.closure import FunctionClosure, GenerativeFunctionClosure
from classiq.model_expansions.function_builder import OperationBuilder
from classiq.model_expansions.scope import QuantumSymbol, Scope


@dataclass(frozen=True)
class PropagatedVariable:
    symbol: QuantumSymbol
    direction: PortDeclarationDirection
    defining_function: str
    handle: HandleBinding

    @property
    def name(self) -> str:
        name = self.symbol.handle.name
        assert name == self.handle.name
        return self.symbol.handle.name


class PropagatedVarStack:
    def __init__(self, scope: Scope, builder: OperationBuilder) -> None:
        # We use dictionary instead of set to maintain the order of insertion
        self._stack: list[dict[PropagatedVariable, None]] = [dict()]
        self._current_scope = scope
        self._builder = builder
        self._to_mangle: dict[PropagatedVariable, str] = dict()

    def set_scope(self, scope: Scope) -> None:
        self._current_scope = scope

    @contextmanager
    def capture_variables(self, op: QuantumOperation) -> Iterator[None]:
        self._stack.append(dict())
        yield
        self._post_handle_propagated_vars(op)

    def _post_handle_propagated_vars(self, qop: QuantumOperation) -> None:
        self._halt_propagation_for_vars_in_scope()
        currently_captured_vars = self._get_captured_vars(qop)
        self._stack[-1].update(currently_captured_vars)
        self._update_port_declarations_for_captured_vars()

    def _halt_propagation_for_vars_in_scope(self) -> None:
        currently_propagated = self._stack.pop()
        self._stack[-1].update(
            {var: None for var in currently_propagated if self._should_propagate(var)}
        )

    def _should_propagate(self, var: PropagatedVariable) -> bool:
        # The second case is in case the captured variable was defined in another function,
        # but the current scope has a variable with the same name
        return (
            var.name not in self._current_scope.data
            or isinstance(self._builder.current_operation, FunctionClosure)
            and var.defining_function != self._builder.current_function.name
        )

    def _get_captured_vars(
        self, qop: QuantumOperation
    ) -> dict[PropagatedVariable, None]:
        input_captured = self._get_captured_vars_with_direction(
            qop.inputs,
            (
                PortDeclarationDirection.Input
                if not self._builder.is_compute_context()
                else PortDeclarationDirection.Inout
            ),
        )
        output_captured = self._get_captured_vars_with_direction(
            qop.outputs,
            (
                PortDeclarationDirection.Output
                if not self._builder.is_compute_context()
                else PortDeclarationDirection.Inout
            ),
        )
        inout_captured = self._get_captured_vars_with_direction(
            qop.inouts, PortDeclarationDirection.Inout
        )
        return inout_captured | input_captured | output_captured

    def _get_captured_vars_with_direction(
        self,
        variables: Iterable[HandleBinding],
        direction: PortDeclarationDirection,
    ) -> dict[PropagatedVariable, None]:
        return {
            self._get_captured_var_with_direction(var, direction): None
            for var in variables
            if self._is_captured(var.name)
        }

    def _get_captured_var_with_direction(
        self, var_handle: HandleBinding, direction: PortDeclarationDirection
    ) -> PropagatedVariable:
        defining_function = self._current_scope[var_handle.name].defining_function
        if defining_function is None:
            raise ClassiqInternalExpansionError
        return PropagatedVariable(
            symbol=self._current_scope[var_handle.name].as_type(QuantumSymbol),
            direction=direction,
            defining_function=defining_function.name,
            handle=var_handle,
        )

    def _is_captured(self, var_name: str) -> bool:
        return (
            self._current_scope.parent is not None
            and var_name in self._current_scope.parent
            and var_name not in self._current_scope.data
        )

    def _update_port_declarations_for_captured_vars(self) -> None:
        self._builder.add_captured_vars(
            PortDeclaration(
                name=self._to_mangle.get(var, var.name),
                direction=var.direction,
                quantum_type=var.symbol.quantum_type,
            )
            for var in self._stack[-1]
        )

    def get_propagated_variables(self, flatten: bool) -> list[HandleBinding]:
        return list(
            dict.fromkeys(
                [self._get_propagated_handle(var, flatten) for var in self._stack[-1]]
            )
        )

    def _get_propagated_handle(
        self, var: PropagatedVariable, flatten: bool
    ) -> HandleBinding:
        if (
            var.defining_function == self._builder.current_function.name
            or not isinstance(
                self._builder.current_function, GenerativeFunctionClosure
            )  # FIXME doesn't work for all cases (CAD-22663)
            and self._no_name_conflict(var)
        ):
            handle_name = var.name
            if var in self._to_mangle:
                self._to_mangle.pop(var)
        else:
            handle_name = mangle_captured_var_name(var.name, var.defining_function)
            self._to_mangle[var] = handle_name
        if flatten:
            return HandleBinding(name=handle_name)
        return var.handle.rename(handle_name)

    def _no_name_conflict(self, var: PropagatedVariable) -> bool:
        return var.name not in self._builder.current_function.colliding_variables


def validate_args_are_not_propagated(
    args: Sequence[ArgValue], captured_vars: Sequence[HandleBinding]
) -> None:
    if not captured_vars:
        return
    captured_handles = {demangle_handle(handle) for handle in captured_vars}
    arg_handles = {
        demangle_handle(arg) for arg in args if isinstance(arg, HandleBinding)
    }
    if any(
        arg_handle.overlaps(captured_handle)
        for arg_handle in arg_handles
        for captured_handle in captured_handles
    ):
        captured_handles_str = {str(handle) for handle in captured_handles}
        arg_handles_str = {str(handle) for handle in arg_handles}
        vars_msg = f"Explicitly passed variables: {arg_handles_str}, captured variables: {captured_handles_str}"
        raise ClassiqExpansionError(
            f"Cannot capture variables that are explicitly passed as arguments. "
            f"{vars_msg}"
        )
