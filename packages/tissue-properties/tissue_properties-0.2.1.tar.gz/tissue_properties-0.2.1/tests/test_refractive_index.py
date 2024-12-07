import pytest

from tissue_properties.optical.refractive_index import navarro
from tissue_properties.optical.refractive_index.navarro.utils import *
from tissue_properties.units import *


def test_navarro_data():
    n_c = navarro.Cornea()
    n_a = navarro.Aqueous()
    n_l = navarro.Lens()
    n_v = navarro.Vitreous()

    # The four functions alpha_1 - alpha_4, have zeros at three special
    # wavelengths, and are 1 at the other. The four special wavelengths are
    #
    # 0.365 um
    # 0.4861 um
    # 0.6563 um
    # 1.014 um
    #
    # alpha_1(0.365 um) = 1
    # alpha_2(0.4861 um) = 1
    # alpha_3(0.6563 um) = 1
    # alpha_4(1.014 um) = 1
    #
    # See Herzberger, "Colour correction in optical systems and a new dispersion formula", 1959 for details
    #
    assert alpha_1(Q_(365, "nm")).magnitude == pytest.approx(1, abs=0.001)
    assert alpha_1(Q_(486.1, "nm")).magnitude == pytest.approx(0, abs=0.001)
    assert alpha_1(Q_(656.3, "nm")).magnitude == pytest.approx(0, abs=0.001)
    assert alpha_1(Q_(1014, "nm")).magnitude == pytest.approx(0, abs=0.001)

    assert alpha_2(Q_(365, "nm")).magnitude == pytest.approx(0, abs=0.001)
    assert alpha_2(Q_(486.1, "nm")).magnitude == pytest.approx(1, abs=0.001)
    assert alpha_2(Q_(656.3, "nm")).magnitude == pytest.approx(0, abs=0.001)
    assert alpha_2(Q_(1014, "nm")).magnitude == pytest.approx(0, abs=0.001)

    assert alpha_3(Q_(365, "nm")).magnitude == pytest.approx(0, abs=0.001)
    assert alpha_3(Q_(486.1, "nm")).magnitude == pytest.approx(0, abs=0.001)
    assert alpha_3(Q_(656.3, "nm")).magnitude == pytest.approx(1, abs=0.001)
    assert alpha_3(Q_(1014, "nm")).magnitude == pytest.approx(0, abs=0.001)

    assert alpha_4(Q_(365, "nm")).magnitude == pytest.approx(0, abs=0.001)
    assert alpha_4(Q_(486.1, "nm")).magnitude == pytest.approx(0, abs=0.001)
    assert alpha_4(Q_(656.3, "nm")).magnitude == pytest.approx(0, abs=0.001)
    assert alpha_4(Q_(1014, "nm")).magnitude == pytest.approx(1, abs=0.001)

    # it is possible that there is a type in Table 1 of Navarro. they report 1.367 for the cornea refractive index.
    # but it is the only one that is off by more than 0.0001 at 589 nm. If we swap the 6 and 7, it matches.
    assert n_c(Q_(589, "nm")).magnitude == pytest.approx(1.376, abs=0.0001)
    assert n_a(Q_(589, "nm")).magnitude == pytest.approx(1.3374, abs=0.0001)
    assert n_l(Q_(589, "nm")).magnitude == pytest.approx(1.42, abs=0.0001)
    assert n_v(Q_(589, "nm")).magnitude == pytest.approx(1.336, abs=0.0001)
