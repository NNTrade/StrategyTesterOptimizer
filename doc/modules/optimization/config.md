# Config
configuration objects

## Classes
```plantuml
namespace optimization.config {

    class StrategyConfigSet {
        as_records(record_type: record_type = record_type.only_valid)->List[StrategyConfig]:
    }
    class StrategyConfigSet__Builder{
        add_set(parameterName, parameterSet: List[Union[int,float,str]])->StrategyConfigSet.Builder
        set_build_func(build_func: Callable[[Dict[str,Union[int,float,str]]],Union[T,None]]) ->  StrategyConfigSet.Builder
        build()->StrategyConfigSet
    }
    class OptimizationConfigSet{
        market_cfg->MarketConfig
        strategy_cfg_set->StrategyConfigSet
        as_records->List[SimulationConfig]
    }

}

namespace simulation.config {
  class StrategyConfig
  class MarketConfig
  class SimulationConfig
}

StrategyConfigSet ..> StrategyConfig
StrategyConfigSet__Builder ..> StrategyConfigSet
StrategyConfigSet__Builder ..> StrategyConfig
OptimizationConfigSet ..> MarketConfig
OptimizationConfigSet ..> StrategyConfigSet
OptimizationConfigSet ..> SimulationConfig
```

### Links
- [simulation.config](../simulation/config.md)

## Sequence
```plantuml
actor actor as a
control "lambda\nbuild_func" as l
participant StrategyConfigSet.Builder as scsb
participant StrategyConfigSet as scs

a->scsb:construct
activate scsb
scsb-->a: instance\nStrategyConfigSet.Builder
deactivate scsb

a->scsb:add_set(parameterName, parameterSet)
activate scsb
scsb-->a: same instance\nStrategyConfigSet.Builder
deactivate scsb

a->scsb:set_build_func(lambda build_func)\nset lambda func\nto create instance of StrategyConfig
activate scsb
scsb-->a: same instance\nStrategyConfigSet.Builder
deactivate scsb

a->scsb:build()
activate scsb
scsb-->a: instance\nStrategyConfigSet
deactivate scsb

a->scs:as_records()
activate scs
alt for each combination of data set
    scs->l:data_set
    activate l
    l-->scs:str_config = Union[StrategyConfig,None]
    deactivate l

    alt str_config is not None
        scs->scs: add str_config to return list
    end
end
scs-->a:strategy config list
deactivate scs
```
