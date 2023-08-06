import pyquil
from pyquil import Program
from pyquil.api import QuantumComputer, EncryptedProgram
import numpy as np
from pyquil.api._qam import QAMExecutionResult
from strangeworks.errors.error import StrangeworksError
import strangeworks
from strangeworks.rigetti.program import CompiledProgram, encrypted_program_to_json
from strangeworks.rigetti.compiler import StrangeworksCompiler


class QuantumComputer(QuantumComputer):
    def __init__(self, ogc: QuantumComputer, as_qvm: bool):
        self.as_qvm = "True" if as_qvm else "False"
        super().__init__(
            name=ogc.name,
            qam=ogc.qam,
            compiler=StrangeworksCompiler(target=ogc.name, as_qvm=self.as_qvm),
        )

    def compile(self, program: Program) -> CompiledProgram:
        nq_program = self.compiler.quil_to_native_quil(program)
        return self.compiler.native_quil_to_executable(nq_program)

    def run(self, program, shots: int = 1) -> QAMExecutionResult:
        payload = {"as_qvm": self.as_qvm}
        if isinstance(program, CompiledProgram):
            payload = self.__serialize_compiled_program(program)
            shots = program.num_shots
        elif isinstance(program, EncryptedProgram):
            payload = self.__serialize_encrypted_program(program)
        elif isinstance(program, Program):
            payload = self.__serialize_program(program)
            shots = program.num_shots
        else:
            raise StrangeworksError.invalid_argument(
                "must pass either a Program or CompiledProgram to execute"
            )

        job = strangeworks.client.circuit_runner.run(
            payload=payload, shots=shots, backend=f"rigetti.{self.name}"
        )

        return self.__read_response(program=program, response=job.results())

    def __serialize_compiled_program(self, qe: CompiledProgram) -> dict:
        return {
            "as_qvm": self.as_qvm,
            "circuit": qe.out(),
            "circuit_type": "strangeworks.rigetti.CompiledProgram",
            "version": pyquil.pyquil_version,
        }

    def __serialize_encrypted_program(self, qe: EncryptedProgram) -> dict:
        return {
            "as_qvm": self.as_qvm,
            "circuit": encrypted_program_to_json(qe),
            "circuit_type": "pyquil.EncryptedProgram",
            "version": pyquil.pyquil_version,
        }

    def __serialize_program(self, p: Program) -> dict:
        return {
            "as_qvm": self.as_qvm,
            "circuit": p.out(calibrations=False),
            "circuit_type": "pyquil.Program",
            "version": pyquil.pyquil_version,
        }

    def __read_response(self, program: Program, response: dict) -> QAMExecutionResult:
        if "data" not in response:
            raise StrangeworksError.bad_response("no data returned from server")
        readout_data = {}
        res = response["data"]
        for i in res:
            readout_data[i] = np.asarray(res[i])
        return QAMExecutionResult(executable=program, readout_data=readout_data)
