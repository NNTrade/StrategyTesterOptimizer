from dataclasses import dataclass
from ...simulation.report import SimulationReport

@dataclass(frozen=True)
class AnalyzationReport:
    optimization: SimulationReport
    forward: SimulationReport