import pydantic

from classiq.interface.generator.parameters import ParameterFloatType
from classiq.interface.generator.standard_gates.standard_gates import StandardGate


class RXGate(StandardGate):
    """
    Rotation by theta about the X axis
    """

    theta: ParameterFloatType


class RYGate(StandardGate):
    """
    Rotation by theta about the Y axis
    """

    theta: ParameterFloatType


class RZGate(StandardGate):
    """
    Rotation by phi about the Z axis
    """

    phi: ParameterFloatType


class RGate(StandardGate):
    """
    Rotation by theta about the cos(phi)X + sin(phi)Y axis
    """

    theta: ParameterFloatType
    phi: ParameterFloatType


class PhaseGate(StandardGate):
    """
    Add relative phase of lambda
    """

    theta: ParameterFloatType


class DoubleRotationGate(StandardGate):
    """
    Base class for RXX, RYY, RZZ
    """

    theta: ParameterFloatType
    _num_target_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=2)


class RXXGate(DoubleRotationGate):
    """
    Rotation by theta about the XX axis
    """


class RYYGate(DoubleRotationGate):
    """
    Rotation by theta about the YY axis
    """


class RZZGate(DoubleRotationGate):
    """
    Rotation by theta about the ZZ axis
    """
