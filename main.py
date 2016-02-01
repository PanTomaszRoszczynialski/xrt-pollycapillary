import matplotlib.pyplot as plt
from elements import capillary as ec
from elements import structures as st
from lenses import polycapillary as lp
from utils import plotter as up
from utils import beam as ub
from examples import basic as eb
from examples import source as es

def create_source():
    """ Generate photons with xrt and save resulting beam """
    # Every source detail is set and tested within it's module
    # so here we can just create the beam at the desired moment
    beamGlobalTotal = es.create_geometric(1e5)
    ub.save_beam_compressed(beamGlobalTotal, 'basic_source.beamc')

def load_source():
    """ Load beam from file saved with the above function """
    loaded_beam = ub.load_beam_compressed('flat_1e5.beamc')

    return loaded_beam

if __name__ == '__main__':
    """ python main.py """
    # Create 10000 photons
    # beam = es.create_geometric(1e4)

    # Lens parameters needed for capillary shape calculations
    y_settings = {'y0': 0.0, 'y1': 40.0,\
                  'y2': 140.0, 'yf': 155.0,\
                  'ym': 88.0}
    D_settings = {'Din': 4.5, 'Dmax': 8.0, 'Dout': 2.4}

    # Prepare lens object ...
    lens = lp.PolyCapillaryLens(y_settings=y_settings,\
                                D_settings=D_settings)
    structure = st.HexStructure(rIn = 1,\
                                nx_capillary = 3,\
                                ny_bundle = 1)
    lens.set_structure(structure)

    # ... and use it to generate capillaries
    caps = lens.get_capillaries()

    # Investigate bugs on just a few
    daps = caps[1:3]

    # Preparation
    test = eb.MultipleCapillariesFittedSource()
    test.set_capillaries(daps)
    test.run_it()
    ceam = test.get_beam()

    # Remove dead photons
    ceam.filter_good()

    # Show results
    # ub.show_beam(ceam)
    bp = up.BeamPlotter(ceam)
    bp.show(140)
    bp.show(141)
    bp.show(155)
