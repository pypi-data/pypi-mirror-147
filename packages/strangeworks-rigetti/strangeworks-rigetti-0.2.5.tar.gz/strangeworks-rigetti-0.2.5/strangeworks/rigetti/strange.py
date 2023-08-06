import strangeworks
from typing import List, Optional
from .qc import QuantumComputer
from qcs_api_client.client import QCSClientConfiguration
import pyquil


def list_quantum_computers() -> List[str]:
    res = []
    backends = strangeworks.client.circuit_runner.get_backends(pprint=False)
    for b in backends:
        if "rigetti" in b.selector_id():
            res.append(b.selector_id().replace("rigetti.", ""))
    return res


def get_qc(name: str, as_qvm: Optional[bool] = None) -> QuantumComputer:    
    return QuantumComputer(name, as_qvm=as_qvm)
