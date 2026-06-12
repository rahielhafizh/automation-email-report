from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReportTimestamp:
    day: int
    month_name: str 
    month_upper: str  
    year: int
    time_str: str 

    @classmethod
    def now(cls) -> ReportTimestamp:
        dt = datetime.now()
        month = dt.strftime("%B")
        return cls(
            day=dt.day,
            month_name=month,
            month_upper=month.upper(),
            year=dt.year,
            time_str=dt.strftime("%H:%M"),
        )

    @property
    def date_upper(self) -> str:
        return f"{self.day} {self.month_upper} {self.year}"

    @property
    def date_title(self) -> str:
        return f"{self.day} {self.month_name} {self.year}"
