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
        anal_rep_df = anal_rep_df.swaplevel(0, 2, axis=1).swaplevel(0, 1, axis=1)
        anal_rep_df.sort_index(axis=1,inplace=True)
        return anal_rep_df

    OPTIMIZED_CFG_F = "optimized_cfg"
    OPTIMIZATION_F = "optimization"
    FORWARD_F = "forward"

    optimized_config: SimulationConfig
    optimization: List[SimulationReport]
    forward: SimulationReport

    def to_dict(self) -> Dict:
        return {
            OptimizationAnalyzReport.OPTIMIZED_CFG_F: self.optimized_config.to_dict(),
            OptimizationAnalyzReport.OPTIMIZATION_F: [o.to_dict() for o in self.optimization],
            OptimizationAnalyzReport.FORWARD_F: self.forward.to_dict()
        }

    
    def to_series(self)->pd.Series:
        opt_sr_arr = []
        for idx, opt_rep in enumerate(self.optimization):
            opt_sr = OptimizationAnalyzReport.simulation_report_to_series(opt_rep,f"{OptimizationAnalyzReport.OPTIMIZATION_F}_{idx}")
            opt_sr_arr.append(opt_sr)
        
        opt_sr = self._get_base_sr(OptimizationAnalyzReport.OPTIMIZATION_F,self.optimized_config.period)
    
        fwd_sr = OptimizationAnalyzReport.simulation_report_to_series(self.forward,OptimizationAnalyzReport.FORWARD_F)   
        return pd.concat([*opt_sr_arr, opt_sr, fwd_sr])

    def _get_base_sr(self,prefix:str, period:DatePeriod)->pd.Series:
        opt_dic={}
        opt_dic[(prefix,SimulationConfig.PERIOD_F, DatePeriod.FROM_F)] = period.from_date
        opt_dic[(prefix,SimulationConfig.PERIOD_F, DatePeriod.UNTILL_F)] = period.untill_date
        opt_sr = pd.Series(opt_dic)
        return opt_sr