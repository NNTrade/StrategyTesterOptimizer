# Optimization Strategy
Parameter optimization strategy define logic to searching best strategy configuration

## Classes
```plantuml
namespace optimization{
    namespace optimization_strategy {
        class absStrategy{
            first()->StrategyConfig
            next(last_simulation_report:SimulationReport)->Union[StrategyConfig, None]
            best()->Union[SimulationReport, None]
        }
        class absFactory {
            build(strategy_config_set:StrategyConfigSet)->absStrategy:
        }
        namespace realization.grid_strategy {
           class GridStrategy
           class GridStrategyFactory
        }
    }

    namespace config {
        class absBaseConfigSet
        class absBaseBuilder
        class StrategyConfigSet
        class IsValidChecker {
            is_valid(self, validation_object:T)->bool
        }
        class DefaultChecker 
    }
}
absFactory ..>  absStrategy
absStrategy --|> GridStrategy
absFactory --|> GridStrategyFactory
IsValidChecker --|> DefaultChecker
absBaseConfigSet --|> StrategyConfigSet

```

## Using
```plantuml
actor Actory as a
participant absStrategy as as
participant absFactory as af

a->af:build(strategy_config_set:StrategyConfigSet)
activate af
af-->a: absStrategy
deactivate af

a->as:first()
activate as
as-->a:next_str_config = StrategyConfig
deactivate as

alt while next_str_config is not None
a->a: caluclate SimulationReport from StrategyConfig

a->as:next(last_simulation_report:SimulationReport)
activate as
as-->a: next_str_config = Union[StrategyConfig, None]
deactivate as
end

a->as:best()
activate as
as-->a: result_str_report = Union[SimulationReport, None]
deactivate as
```