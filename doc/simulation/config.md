# Config module
Simulation configuration
## Classe
```plantuml
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

namespace NNTrade.common {
  enum TimeFrame
}

SimulationConfig *-- MarketConfig
MarketConfig *-- StockConfig
StockConfig *-- TimeFrame
SimulationConfig *-- StrategyConfig

```