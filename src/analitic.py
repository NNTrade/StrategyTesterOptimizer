import pandas as pd
from typing import Dict
from .testing_report import TestingReport
from .strategy.run_report import metrics as m
from .strategy import run_config as rcfg

class Analitic:
  def __init__(self,testing_rep: TestingReport)-> None:
    self.__testing_rep = testing_rep
    self.__result_df = None
    pass

  @staticmethod
  def get_metric(name:str,df:pd.DataFrame)->Dict:
    str_yield_per_year_std = df[(m.MetricContainer.CAP_F, m.CapitalMetric.STR_YIELD_YEAR_F)].std()
    str_yield_per_year_median = df[(m.MetricContainer.CAP_F, m.CapitalMetric.STR_YIELD_YEAR_F)].median()
    std_median_rel = round(str_yield_per_year_std/str_yield_per_year_median*100,3)
    return {
      "name":name,
      "std(yield/year), %":round(str_yield_per_year_std*100,3),
      "median(yield/year), %":round(str_yield_per_year_median*100,3),
      "std/median of (yield/year), %": std_median_rel
    }
  @staticmethod
  def get_success_yield(name:str,df:pd.DataFrame)->Dict:
    return {
      "name":name,
      "yield > 0, %":round(len(df[df[(m.MetricContainer.CAP_F,m.CapitalMetric.STR_YIELD_F)]>0])/len(df)*100,3),
      "median(success_deal/deal), %": round((df[(m.MetricContainer.DEALS_F, m.DealMetric.SUCCESS_DEAL_COUNT_F)] / df[(m.MetricContainer.DEALS_F, m.DealMetric.DEAL_COUNT_F)]).median()*100,3)
    }
  
  @staticmethod
  def build_analis_df(testing_rep: TestingReport)->pd.DataFrame:
    df = testing_rep.as_df

    return pd.concat([pd.DataFrame([
      Analitic.get_success_yield("all", df),
      Analitic.get_success_yield("ticker", df.groupby(((rcfg.RunConfig.MARKET_CFG_F, "full_ticker"))).median()),
      Analitic.get_success_yield("str", df.groupby([c for c in df.index.names if c[0]==rcfg.RunConfig.STRATEGY_CFG_F]).median()),
    ]).set_index("name"),
    pd.DataFrame([
      Analitic.get_metric("all", df),
      Analitic.get_metric("ticker", df.groupby(((rcfg.RunConfig.MARKET_CFG_F, "full_ticker"))).median()),
      Analitic.get_metric("str",df.groupby([c for c in df.index.names if c[0]==rcfg.RunConfig.STRATEGY_CFG_F]).median()),
    ]).set_index("name")], axis=1)

  @property
  def analis(self)->pd.DataFrame:
    if self.__result_df is None:
      self.__result_df = Analitic.build_analis_df(self.__testing_rep)
    return self.__result_df