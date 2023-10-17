import json

import click

from aisweb_cli.domain.result.result_unreachable_exception import (
  ResultUnreachableException,
)
from aisweb_cli.infrastructure.get_charter_data import GetCharterDataImpl
from aisweb_cli.use_cases.get_charter_data import GetCharterData

service: GetCharterData = GetCharterDataImpl()


@click.command()
@click.option("-i", "--icao", type=str, help="ICAO Code")
def search_icao(icao):
  try:
    result = service.find_by_icao(icao)

    if result:
      click.echo(json.dumps(result.asdict(), indent=2))
    else:
      click.echo("Aeródromo não encontrado")
  except ResultUnreachableException:
    click.echo("Servidor indisponível")



if __name__ == '__main__':
  search_icao()
