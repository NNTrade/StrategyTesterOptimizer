from dataclasses import dataclass
from ...simulation.report import SimulationReport

@dataclass(frozen=True)
class AnalizationReport:
    optimization: SimulationReport
    forward: SimulationReport