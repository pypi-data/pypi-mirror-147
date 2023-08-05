import pytest
from pytest_regressions.data_regression import DataRegressionFixture

from gdsfactory.components.mmi2x2 import mmi2x2
from gdsfactory.components.mzi_phase_shifter import mzi_phase_shifter_top_heater_metal

# from gdsfactory.components.spiral_inner_io import spiral_inner_io
from gdsfactory.containers import container_factory
from gdsfactory.difftest import difftest

container_names = set(container_factory.keys()) - set(
    ["add_grating_couplers_wi_e642a51b"]
)
component = mzi_phase_shifter_top_heater_metal(splitter=mmi2x2)


@pytest.mark.parametrize("container_type", container_names)
def test_settings(container_type: str, data_regression: DataRegressionFixture) -> None:
    """Avoid regressions when exporting settings."""
    c = container_factory[container_type](component=component)
    data_regression.check(c.to_dict())


@pytest.mark.parametrize("container_type", container_names)
def test_gds(container_type: str) -> None:
    """Avoid regressions in GDS geometry shapes and layers."""
    c = container_factory[container_type](component=component)
    difftest(c)


# Special test cases for exotic components
# def test_add_gratings_and_loopback(data_regression: DataRegressionFixture) -> None:
#     """This container requires all ports to face the same direction."""
#     c = add_gratings_and_loopback(component=spiral_inner_io())
#     data_regression.check(c.settings)


if __name__ == "__main__":
    for i in container_names:
        print(i)
