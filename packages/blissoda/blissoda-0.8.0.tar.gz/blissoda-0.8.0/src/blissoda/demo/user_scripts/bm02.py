from blissoda.demo.bm02 import bm02_xrpd_processor

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None


def bm02_demo_1d(expo=0.2, npoints=10):
    bm02_xrpd_processor.enable(setup_globals.difflab6)
    try:
        if "nbpt_azim" in bm02_xrpd_processor.integration_options["difflab6"]:
            bm02_xrpd_processor.integration_options["difflab6"].pop("nbpt_azim")
        setup_globals.loopscan(npoints, expo, setup_globals.difflab6)
    finally:
        bm02_xrpd_processor.disable()


def bm02_demo_2d(expo=0.2, npoints=10):
    bm02_xrpd_processor.enable(setup_globals.difflab6)
    try:
        bm02_xrpd_processor.integration_options["difflab6"]["nbpt_azim"] = 100
        setup_globals.loopscan(npoints, expo, setup_globals.difflab6)
    finally:
        bm02_xrpd_processor.disable()
