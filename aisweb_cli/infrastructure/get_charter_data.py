import json
import re
from typing import Optional

import requests
from bs4 import BeautifulSoup
from redis import exceptions

from aisweb_cli.domain.result.result import Result
from aisweb_cli.domain.result.result_unreachable_exception import (
  ResultUnreachableException,
)
from aisweb_cli.infrastructure.cache import Cache
from aisweb_cli.infrastructure.fake_cache import FakeCache
from aisweb_cli.use_cases.get_charter_data import GetCharterData


class GetCharterDataImpl(GetCharterData):
  def __init__(self) -> None:
    try:
      self.cache = Cache()
    except exceptions.ConnectionError:
      self.cache = FakeCache()

  def find_by_icao(self, icao, tries=0) -> Optional[Result]:
    if tries == 0:
      cached_data = self.cache.get(icao)

      if cached_data:
        return json.loads(cached_data, object_hook=lambda d: Result(**d))

    response = requests.get(f"https://aisweb.decea.mil.br/?i=aerodromos&codigo={icao}")

    
    if not response.ok:
      self.retry(tries, lambda: self.find_by_icao(icao, tries+1))

    if "O aeródromo não foi encontrado." in response.text:
      return None

    result = self.parse_result(response.text)
    self.cache.set(icao, json.dumps(result.asdict()))
    
    return result

  
  def parse_result(self, data):
    soup = BeautifulSoup(data, features="html.parser")

    sunrise = soup.find("sunrise").get_text()
    sunset = soup.find("sunset").get_text()
    metar = soup.find("h5", string="METAR").find_next_sibling("p").get_text()
    taf = soup.find("h5", string="TAF").find_next_sibling("p").get_text()

    cartas_header = soup.find("h4", string=re.compile("Cartas"))
    quantidade_de_cartas = int(re.search("\d", cartas_header.get_text()).group())
    cartas = cartas_header.find_next_siblings("h4")[:quantidade_de_cartas]
    cartas_text = [carta.get_text() for carta in cartas]

    return Result(sunrise, sunset, metar, taf, cartas_text)


  def retry(self, tries, callback):
    if tries < 3:
        return callback()
    raise ResultUnreachableException()

