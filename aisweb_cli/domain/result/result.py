from dataclasses import dataclass, asdict
from datetime import date

@dataclass
class Result:
  sunrise: str
  sunset: str
  metar: str
  taf: str
  charters: list[str]

  def asdict(self):
    return asdict(self)
