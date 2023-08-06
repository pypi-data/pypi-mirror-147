from typing import Any, Optional, Union

import pydantic

from classiq.interface.generator.parameters import ParameterFloatType
from classiq.interface.generator.standard_gates.standard_gates import StandardGate

CONTROLLED_GATE_CONTROL_INPUT = "CTRL_IN"
CONTROLLED_GATE_TARGET_INPUT = "TARGET_IN"

CONTROLLED_GATE_CONTROL_OUTPUT = "CTRL_OUT"
CONTROLLED_GATE_TARGET_OUTPUT = "TARGET_OUT"

CtrlState = Optional[Union[pydantic.StrictStr, pydantic.NonNegativeInt]]


class ControlledGate(StandardGate):
    """
    Base model for controlled Gates
    """

    _num_ctrl_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=1)

    _input_names = pydantic.PrivateAttr(
        default=[CONTROLLED_GATE_CONTROL_INPUT, CONTROLLED_GATE_TARGET_INPUT]
    )
    _output_names = pydantic.PrivateAttr(
        default=[CONTROLLED_GATE_CONTROL_OUTPUT, CONTROLLED_GATE_TARGET_OUTPUT]
    )


class ControlledGateWithState(ControlledGate):
    """
    Base model for controlled Gates with control over the controlled_state
    """

    ctrl_state: CtrlState = pydantic.Field(
        description="The control state in decimal or as a bit string (e.g. '1011'). If not specified, the control "
        "state is 2**num_ctrl_qubits - 1.\n"
        "The gate will be performed if the state of the control qubits matches the control state"
    )

    def __init__(self, **data: Any):
        super().__init__(**data)

        self.validate_ctrl_state()

    def validate_ctrl_state(self) -> None:
        num_ctrl_qubits = self._num_ctrl_qubits
        if self.ctrl_state is None:
            self.ctrl_state = pydantic.StrictStr("1" * num_ctrl_qubits)
            return
        ctrl_state_int: pydantic.NonNegativeInt = (
            int(self.ctrl_state, 2)
            if isinstance(self.ctrl_state, str)
            else self.ctrl_state
        )
        if ctrl_state_int < 0 or ctrl_state_int >= 2**num_ctrl_qubits:
            raise ValueError(
                "Control state value should be zero or positive and smaller than 2**num_ctrl_qubits"
            )


class CXGate(ControlledGateWithState):
    """
    The Controlled-X Gate
    """


class CCXGate(ControlledGateWithState):
    """
    The Double Controlled-X Gate
    """

    _num_ctrl_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=2)


class C3XGate(ControlledGateWithState):
    """
    The X Gate controlled on 3 qubits
    """

    _num_ctrl_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=3)


class C4XGate(ControlledGateWithState):
    """
    The X Gate controlled on 4 qubits
    """

    _num_ctrl_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=4)


class CYGate(ControlledGateWithState):
    """
    The Controlled-Y Gate
    """


class CZGate(ControlledGateWithState):
    """
    The Controlled-Z Gate
    """


class CHGate(ControlledGateWithState):
    """
    The Controlled-H Gate
    """


class CSXGate(ControlledGateWithState):
    """
    The Controlled-SX Gate
    """


class CRXGate(ControlledGateWithState):
    """
    The Controlled-RX Gate
    """

    theta: ParameterFloatType


class CRYGate(ControlledGateWithState):
    """
    The Controlled-RY Gate
    """

    theta: ParameterFloatType


class CRZGate(ControlledGateWithState):
    """
    The Controlled-RZ Gate
    """

    theta: ParameterFloatType


class CPhaseGate(ControlledGateWithState):
    """
    The Controlled-Phase Gate
    """

    theta: ParameterFloatType


class MCPhaseGate(ControlledGate):
    """
    The Controlled-Phase Gate
    """

    num_ctrl_qubits: pydantic.PositiveInt

    lam: ParameterFloatType

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._num_ctrl_qubits = self.num_ctrl_qubits
