from abc import ABC, abstractmethod
from typing import Optional

from aisweb_cli.domain.result.result import Result


class GetCharterData(ABC):
  @abstractmethod
  def find_by_icao(self, icao, tries) -> Optional[Result]:
    raise NotImplementedError()
