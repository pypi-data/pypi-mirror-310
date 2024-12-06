import os
import json

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None
try:
    from bliss import current_session
except ImportError:
    current_session = None


from .calib import DEFAULT_CALIB
from ..utils import directories
from ..bm02.xrpd_processor import Bm02XrpdProcessor


class DemoBm02XrpdProcessor(Bm02XrpdProcessor):
    def __init__(self, **defaults) -> None:
        defaults.setdefault("lima_names", ["difflab6"])
        defaults.setdefault(
            "integration_options",
            {
                "difflab6": {
                    "method": "no_csr_cython",
                    "nbpt_rad": 4096,
                    "unit": "q_A^-1",
                }
            },
        )
        super().__init__(**defaults)
        self._ensure_pyfai_config_filename()

    def _ensure_pyfai_config_filename(self):
        root_dir = directories.get_processed_dir(current_session.scan_saving.filename)
        cfgfile = os.path.join(root_dir, "config", "pyfaicalib.json")
        if not os.path.exists(cfgfile):
            poni = DEFAULT_CALIB
            os.makedirs(os.path.dirname(cfgfile), exist_ok=True)
            with open(cfgfile, "w") as f:
                json.dump(poni, f)
        self.config_filename = {"difflab6": cfgfile}


if setup_globals is None:
    bm02_xrpd_processor = None
else:
    bm02_xrpd_processor = DemoBm02XrpdProcessor()
