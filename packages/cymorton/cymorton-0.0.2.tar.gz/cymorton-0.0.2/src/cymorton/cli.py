import click
from cymorton.codec import convert_lat_lon_level_to_code
from cymorton import __version__


@click.command()
@click.version_option(__version__)
@click.argument('lat', type=click.FLOAT)
@click.argument('lon', type=click.FLOAT)
@click.argument('z', type=click.INT)
def main(lat: float, lon: float, z: int):
    """
    Prints the Morton code for LAT and LON at Z level
    """
    click.echo(convert_lat_lon_level_to_code(lat, lon, z))
