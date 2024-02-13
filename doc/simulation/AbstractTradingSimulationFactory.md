# Abstract Trading Simulation Factory
[class absTradingSimulationFactory](../../src/simulation/abs_trading_simulation_factory.py)

## Definition
Offer function to simulate trading

## Methods
### Get Simulation Log
#### Sequential
```plantuml
@startuml
actor User as u
participant absTradingSimulationFactory as TSF
participant absSimulationLogStorage as SRS
u -> TSF: get(run_config: SimulationConfig)
activate TSF
TSF -> SRS: try_get(strategy_id: StrategyId, run_config: RunConfig)\n-> Union[SimulationLog, None]
activate SRS
SRS --> TSF: Union[SimulationLog, None]
deactivate SRS

alt SimulationLog\ is none
TSF->TSF: _run(run_config: SimulationConfig)->SimulationLog
end
TSF --> u: SimulationLog
deactivate TSF
@enduml
```