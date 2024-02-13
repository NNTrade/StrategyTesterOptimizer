# Common package
Common models

## Classes
```plantuml
namespace common{
    class CandleConfig{
        ticker:str
        timeframe:TimeFrame
    }

    class CandleDataSetConfig{
        stocks:Dict[str,CandleConfig]
        step_timeframe:TimeFrame
    }

    class DatePeriod {
        from_date:date
        untill_date:date
        period_in_days:int
        period_in_years:float
        split(chunks_count: int):List[DatePeriod]
    }
}

namespace NNTrade.common{
    enum TimeFrame
}
namespace datetime{
    class date
}

CandleConfig ..> TimeFrame
CandleDataSetConfig ..> TimeFrame
CandleDataSetConfig ..> CandleConfig
DatePeriod ..> date
```