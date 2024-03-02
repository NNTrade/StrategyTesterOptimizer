from __future__ import annotations
from dataclasses import dataclass
from ...simulation.report import SimulationReport
from typing import Dict,List
from ...simulation.config import SimulationConfig
from ...common import DatePeriod
import pandas as pd

@dataclass(frozen=True)
class OptimizationAnalyzReport:
    @staticmethod
    def simulation_report_to_series(sim_rep:SimulationReport, prefix:str)->pd.Series:
        opt_dic={}
        opt_dic[(prefix,SimulationConfig.PERIOD_F, DatePeriod.FROM_F)] = sim_rep.simulation_config.period.from_date
        opt_dic[(prefix,SimulationConfig.PERIOD_F, DatePeriod.UNTILL_F)] = sim_rep.simulation_config.period.untill_date
        opt_dic = {**opt_dic, **{ (prefix,k1, k2): v2 for k1, v1 in sim_rep.metrics.to_dict().items() for k2, v2 in v1.items() }}
        return pd.Series(opt_dic)

    @staticmethod
    def flow_to_dataframe(flow:List[OptimizationAnalyzReport])->pd.DataFrame:
        anal_rep_df = pd.DataFrame([anal_rep.to_series() for anal_rep in flow])
        anal_rep_df.set_index([(step, SimulationConfig.PERIOD_F, col) for step in [OptimizationAnalyzReport.OPTIMIZATION_F, OptimizationAnalyzReport.FORWARD_F] for col in [DatePeriod.FROM_F,DatePeriod.UNTILL_F]], inplace=True)
        anal_rep_df.columns = anal_rep_df.columns.swaplevel(0, 2).swaplevel(0, 1)
        anal_rep_df.sort_index(axis=1,inplace=True)
        return anal_rep_df

    OPTIMIZATION_F = "optimization"
    FORWARD_F = "forward"

    optimization: SimulationReport
    forward: SimulationReport

    def to_dict(self) -> Dict:
        return {
            OptimizationAnalyzReport.OPTIMIZATION_F: self.optimization.to_dict(),
            OptimizationAnalyzReport.FORWARD_F: self.forward.to_dict()
        }

    def to_series(self)->pd.Series:
        opt_sr = OptimizationAnalyzReport.simulation_report_to_series(self.optimization,OptimizationAnalyzReport.OPTIMIZATION_F)
        fwd_sr = OptimizationAnalyzReport.simulation_report_to_series(self.forward,OptimizationAnalyzReport.FORWARD_F)   
        return pd.concat([opt_sr, fwd_sr])