"""Executor module, implementing facilities for executing quantum programs using Classiq platform."""
import asyncio
from typing import Optional, Union

from classiq.interface.executor import (
    execution_request,
    hamiltonian_minimization_problem,
    result as exc_result,
)
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.executor.quantum_program import QuantumProgram
from classiq.interface.executor.result import (
    ExecutionDetails,
    FinanceSimulationResults,
    GroverSimulationResults,
)
from classiq.interface.executor.vqe_result import VQESolverResult
from classiq.interface.generator import result as generation_result

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.type_validation import validate_type
from classiq.exceptions import ClassiqExecutionError


class Executor:
    """Executor is the entry point for executing quantum programs on multiple quantum hardware vendors."""

    def __init__(
        self, preferences: Optional[ExecutionPreferences] = None, **kwargs
    ) -> None:
        """Init self.

        Args:
            preferences (): Execution preferences, such as number of shots.
        """
        self._preferences = preferences or ExecutionPreferences(**kwargs)

    def execute_quantum_program(
        self, quantum_program: QuantumProgram
    ) -> ExecutionDetails:
        return asyncio.run(self.execute_quantum_program_async(quantum_program))

    async def execute_quantum_program_async(
        self, quantum_program: QuantumProgram
    ) -> ExecutionDetails:
        """Async version of `execute_quantum_program`"""
        request = execution_request.ExecutionRequest(
            execution_payload=execution_request.QuantumProgramExecution(
                **quantum_program.dict()
            ),
            preferences=self._preferences,
        )
        try:
            execution_result = await ApiWrapper.call_execute_task(request=request)
        except Exception as exc:
            raise ClassiqExecutionError(f"Execution failed: {exc!s}") from exc

        if execution_result.status != exc_result.ExecutionStatus.SUCCESS:
            raise ClassiqExecutionError(f"Execution failed: {execution_result.details}")
        return validate_type(
            obj=execution_result.details,
            expected_type=ExecutionDetails,
            operation="Execution",
            exception_type=ClassiqExecutionError,
        )

    def execute_generated_circuit(
        self, generation_result: generation_result.GeneratedCircuit
    ) -> Union[FinanceSimulationResults, GroverSimulationResults]:
        return asyncio.run(self.execute_generated_circuit_async(generation_result))

    async def execute_generated_circuit_async(
        self, generation_result: generation_result.GeneratedCircuit
    ) -> Union[FinanceSimulationResults, GroverSimulationResults]:
        """Async version of `execute_generated_circuit`"""
        if generation_result.metadata is None:
            raise ClassiqExecutionError(
                "The execute_generated_circuit is to execute generated circuits as oracles, but "
                "the generated circuit's metadata is empty. To execute a circuit as-is, please"
                "use execute_quantum_program."
            )
        request = execution_request.ExecutionRequest(
            execution_payload=execution_request.GenerationMetadataExecution(
                **generation_result.metadata.dict()
            ),
            preferences=self._preferences,
        )
        execution_result = await ApiWrapper.call_execute_task(request=request)

        if execution_result.status != exc_result.ExecutionStatus.SUCCESS:
            raise ClassiqExecutionError(f"Execution failed: {execution_result.details}")
        return validate_type(
            obj=execution_result.details,
            expected_type=(FinanceSimulationResults, GroverSimulationResults),
            operation="Execution",
            exception_type=ClassiqExecutionError,
        )

    def execute_hamiltonian_minimization(
        self,
        hamiltonian_minimization_problem: hamiltonian_minimization_problem.HamiltonianMinimizationProblem,
    ) -> VQESolverResult:
        return asyncio.run(
            self.execute_hamiltonian_minimization_async(
                hamiltonian_minimization_problem
            )
        )

    async def execute_hamiltonian_minimization_async(
        self,
        hamiltonian_minimization_problem: hamiltonian_minimization_problem.HamiltonianMinimizationProblem,
    ) -> VQESolverResult:
        """Async version of `execute_hamiltonian_minimization`"""
        request = execution_request.ExecutionRequest(
            execution_payload=execution_request.HamiltonianMinimizationProblemExecution(
                **hamiltonian_minimization_problem.dict()
            ),
            preferences=self._preferences,
        )
        execution_result = await ApiWrapper.call_execute_task(request=request)

        if execution_result.status != exc_result.ExecutionStatus.SUCCESS:
            raise ClassiqExecutionError(f"Execution failed: {execution_result.details}")
        return validate_type(
            obj=execution_result.details,
            expected_type=VQESolverResult,
            operation="Execution",
            exception_type=ClassiqExecutionError,
        )
