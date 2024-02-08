# Classes
## Link
[__init__.py](../../src/simulation/__init__.py)

## Funcitons
- Get Simulation report for config [sequence](./AbstractTradingSimulationFactory.md)

## Class model
![Simulation class model](simulation_class_model)

## PlantUml
```
@startuml
namespace simulation {
  class absTradingSimulationFactory {
    get(run_config: SimulationConfig) -> SimulationReport
    strategy_id:StrategyId
  }
}


namespace simulation.models {
  class SimulationReport {
    strategy_id: StrategyId
    capital_log: Dict[datetime, float]
    deal_list: List[Deal]
    metrics: MetricContainer
    run_config: SimulationConfig
  }

  class Deal
}

namespace simulation.models.metrics {
  class MetricContainer {
    capital: CapitalMetric
    deals: DealMetric
  }
  
  class CapitalMetric
  class DealMetric
}

namespace simulation.config {
  class SimulationConfig {
    market_cfg: MarketConfig
    strategy_cfg: StrategyConfig
  }

  class MarketConfig {
    stocks: Dict[str,StockConfig]
    step_timeframe: TimeFrame
    from_date: date
    untill_date: date
  }

  class StockConfig {
    ticker: str
    timeframe: Union[TimeFrame, None] = None
  }

  class StrategyConfig

  class StrategyId
}

namespace simulation.storage {
  class absSimulationReportStorage {
    try_get(strategy_id:StrategyId, run_config: SimulationConfig) -> Union[SimulationReport, None]:
    try_add(strategy_id:StrategyId, run_config: SimulationConfig, run_report: SimulationReport) -> bool:
  }

  class InMemoryStorage
}


namespace NNTrade.common {
  enum TimeFrame
}

SimulationConfig *-- MarketConfig
MarketConfig *-- StockConfig
StockConfig *-- TimeFrame
SimulationConfig *-- StrategyConfig

absTradingSimulationFactory ..> SimulationConfig
absTradingSimulationFactory ..> SimulationReport
absTradingSimulationFactory ..> absSimulationReportStorage
absTradingSimulationFactory ..> StrategyId

absSimulationReportStorage <|-- InMemoryStorage 

SimulationReport ..> Deal
SimulationReport ..> SimulationConfig
SimulationReport ..> StrategyId
SimulationReport ..> MetricContainer
MetricContainer ..> CapitalMetric
MetricContainer ..> DealMetric
@enduml
```