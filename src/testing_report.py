from __future__ import annotations
from typing import Dict, List
from .strategy.run_report import RunReport
from .strategy import run_config as rcfg
from .strategy.run_report import RunReportFactory
from tqdm import tqdm
import pandas as pd

class TestingReport:
    """Report of testing stage
    """

    class Factory:
        def __init__(self, runReportFactory: RunReportFactory) -> None:
            self.__run_report_factory = runReportFactory
            pass

        def get(self, runConfigSet: rcfg.RunConfigSet) -> TestingReport:
            trb = TestingReport.Builder()
            for rc in tqdm(runConfigSet.as_records()):
                rr = self.__run_report_factory.get(rc)
                trb.add(rr)
            return trb.build()

    class Builder:
        """Builder of single tester stage report
        """

        def __init__(self):
            self.run_report_list = []
            pass

        def add(self, strategy_run_report: RunReport):
            """Add strategy run report to testing stage report

            Args:
                strategy_run_report (StrategyRunReport): _description_
            """
            self.run_report_list.append(strategy_run_report)
            pass

        def build(self) -> TestingReport:
            """Build testing stage report

            Returns:
                TesterReport: _description_
            """
            return TestingReport(self.run_report_list)

    def __init__(self, run_report_list: List[RunReport]) -> None:
        self.__run_report_list = run_report_list.copy()
        self.__as_df = None
        pass

    @property
    def run_report_list(self) -> List[RunReport]:
        return self.__run_report_list.copy()
    
    @property 
    def as_df(self)->pd.DataFrame:
        if self.__as_df is None:
            self.__as_df = TestingReport.build_df(self)
        return self.__as_df

    def clear_cache(self):
        self.__as_df = None

    @staticmethod
    def build_df(testing_report:TestingReport)->pd.DataFrame:
        level_cut = 3
        df_rec = []
        for rr in testing_report.run_report_list:
            rr_dict = rr.to_dict()
            del rr_dict["abs_cap_log"]
            del rr_dict["deal_list"]
            flat_dict = TestingReport.flatten_dict(rr_dict)
            cutted_flat_dict = TestingReport.cut_level(flat_dict, level_cut)
            df_rec.append(cutted_flat_dict)
        df = pd.DataFrame.from_records(df_rec)
        df.columns = pd.MultiIndex.from_tuples(df.columns)

        # drop const values
        df.drop([(RunReport.RUN_CONFIG_F, rcfg.RunConfig.STRATEGY_ID_F)],axis=1,inplace=True)
        # join ticker cols
        ticker_cols = [(RunReport.RUN_CONFIG_F, rcfg.RunConfig.MARKET_CFG_F, m) for m in  ["stocks_0_ticker",	"stocks_0_timeframe", rcfg.MarketConfig.STEP_TF_F]]
        df[(RunReport.RUN_CONFIG_F, rcfg.RunConfig.MARKET_CFG_F,"full_ticker")] = df[[(RunReport.RUN_CONFIG_F, rcfg.RunConfig.MARKET_CFG_F, m) for m in  ["stocks_0_ticker",	"stocks_0_timeframe",rcfg.MarketConfig.STEP_TF_F]]].apply(lambda row: ':'.join(map(str, row)), axis=1)
        df.drop(ticker_cols, axis=1,inplace=True)
        # set index
        df.set_index([c for c in df.columns if c[0] ==RunReport.RUN_CONFIG_F], inplace=True)
        # drop unused level
        df.index.names = [(n[1],n[2]) for n in  df.index.names] 
        df.columns = df.columns.droplevel(0)
        df = df.reorder_levels([df.index.names[-1],*df.index.names[:-1]])
        return df
    
    @staticmethod
    def flatten_dict(d, parent_key_stack:List=[]):
        items = []
        for k, v in d.items():
            cur_key_stack = parent_key_stack.copy()
            cur_key_stack.append(k)
            if isinstance(v, dict):
                items.extend(TestingReport.flatten_dict(v, cur_key_stack))
            elif isinstance(v,list):
                for idx, v_el in enumerate(v):
                    el_key_stack = cur_key_stack.copy()
                    el_key_stack.append(f"{idx}")
                    items.extend(TestingReport.flatten_dict(v_el, el_key_stack))
            else:
                items.append((tuple(cur_key_stack), v))
        if len(parent_key_stack)==0:
            return dict(items)
        else:
            return items
        
    @staticmethod
    def cut_level(flat_dict:Dict, level_count):
        cutted_flat_dic = {}
        for k,v in flat_dict.items():
            if len(k) <= level_count:
                cutted_flat_dic[k] = v
            else:
                cutted_flat_dic[tuple([*k[:level_count-1],"_".join(k[level_count-1:])])] = v
        return cutted_flat_dic