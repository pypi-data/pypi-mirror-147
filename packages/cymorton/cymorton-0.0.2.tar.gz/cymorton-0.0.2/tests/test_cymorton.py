from click.testing import CliRunner

from cymorton.codec import interleave_to_number
from cymorton.codec import convert_xy_level_to_code
from cymorton.codec import convert_lat_lon_level_to_code
from cymorton.cli import main


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, ["9.165507", "105.219986", "12"])
    assert result.output == '24145105\n'
    assert result.exit_code == 0


def test_interleave_to_number():
    assert interleave_to_number(0b1011001) == 0b1000101000001


def test_convert_xy_level_to_code():
    assert convert_xy_level_to_code(5, 2, 3) == 0b1011001


def test_convert_lat_lon_level_to_code():
    assert convert_lat_lon_level_to_code(9.165507, 105.219986, 12) == 24145105
