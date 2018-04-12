import click

from carbonize.calculators import distance_between_airports, aviation_emissions
from carbonize.typing import AirportCode


@click.command()
@click.option('--origin', help='Origin airport code.')
@click.option('--destination', help='Destination airport code.')
def carbonize(origin: AirportCode, destination: AirportCode):
    distance = distance_between_airports(origin, destination)
    click.echo(aviation_emissions(1000))


if __name__ == '__main__':
    carbonize()
