# Abstract Trading Simulation Factory
[class absTradingSimulationFactory](../src/simulation/abs_trading_simulation_factory.py)

![absTradingSimulationFactory sequence](absTradingSimulationFactory.sequence.png)

```plantuml
@startuml
actor User as u
participant absTradingSimulationFactory as TSF
participant absSimulationReportStorage as SRS
u -> TSF: get(run_config: SimulationConfig)
activate TSF
TSF -> SRS: try_get(strategy_id: StrategyId, run_config: RunConfig)\n-> Union[SimulationReport, None]
activate SRS
SRS --> TSF: Union[SimulationReport, None]
deactivate SRS

alt SimulationReport is none
TSF->TSF: _run(run_config: SimulationConfig)->SimulationLog
TSF->TSF: SimulationReport(\nstrategy_id: StrategyId, run_config: SimulationConfig,\nabs_capital_log: Dict[datetime, float], deal_list: List[Deal])
end
TSF --> u: SimulationReport
deactivate TSF
@enduml
```

## Configuration
![Configuration classes](Configuration.png)
```plantuml
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

enum TimeFrame

class StrategyConfig

SimulationConfig *-- MarketConfig
MarketConfig *-- StockConfig
StockConfig *-- TimeFrame
SimulationConfig *-- StrategyConfig
```

### Simulation

- Testing - testing strategies
- Optimization - strategy optimizer
- ReportFactory - Build reports
  - TestingReportFactory - Build reports of testing process
  - OptimizationReportFactory - Build reports of optimization process
- MetricSource - wrapper of strategy result, which return [base metrics](./Metrics.md#base-metrics)