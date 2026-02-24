import logging
import unittest

import earthaccess
import pytest

logger = logging.getLogger(__name__)
assertions = unittest.TestCase("__init__")


logger.info(f"earthaccess version: {earthaccess.__version__}")


@pytest.fixture(
    scope="module",
    params=[
        ("MUR25-JPL-L4-GLOB-v04.2", 2),
        ("AVHRR_OI-NCEI-L4-GLOB-v2.1", 1),
        ("TEMPO_NO2_L3", 2),
        ("M2T1NXSLV", 1),
    ],
)
def granules(request):
    short_name, count = request.param
    granules = earthaccess.search_data(
        count=count, temporal=("2025"), short_name=short_name
    )
    return granules


def test_open_virtual_mfdataset(granules):
    # Simply check that the dmrpp can be found, parsed, and loaded. Actual parser result is checked in virtualizarr
    vds = earthaccess.open_virtual_mfdataset(granules, concat_dim="time")
    # We can use fancy indexing
    assert vds.isel(time=0) is not None


def test_open_virtual_mfdataset_with_skipped_variables():
    granules = earthaccess.search_data(
        count=1, temporal=("2025"), short_name="VNP43MA4"
    )
    vds = earthaccess.open_virtual_mfdataset(
        granules,
        group="/HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields",
        concat_dim="XDim",
        skip_variables=["Projection"],
    )

    assert vds.isel(XDim=0) is not None
    assert vds.variables.get("Projection") is None
