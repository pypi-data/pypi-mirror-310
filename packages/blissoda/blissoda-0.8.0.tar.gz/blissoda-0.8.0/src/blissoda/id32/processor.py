import json
import logging
import os
from typing import Dict, Optional

from blissoda.resources import resource_filename

try:
    from bliss import current_session
except ImportError:
    current_session = None

from ewoksjob.client import submit

from ..persistent.parameters import (
    ParameterInfo,
    WithPersistentParameters,
    autocomplete_property,
)
from ..utils import trigger
from ..utils.directories import get_dataset_processed_dir

logger = logging.getLogger(__name__)


# ~ from bliss import setup_globals
# ~ from bliss.config.settings import HashSetting
# ~ class SpecGenParameters:
# ~ def __init__(self):
# ~ andor_setting = {"slope": 0}
# ~ self.andor = HashSetting('andor1_setting', default_values=andor_setting)


class Id32SpecGenProcessor(
    WithPersistentParameters,
    parameters=[
        ParameterInfo("_enabled"),
        ParameterInfo("trigger_at", category="workflows"),
        ParameterInfo("parameters", category="workflows"),
    ],
):
    WORKER = "ewoksworker_lid32rixs1"
    WORKFLOW_FILENAME = "convert_image_to_spectrum.json"
    OUTPUT_FILENAME = "spectrum.txt"

    def __init__(self, detectors=[], **defaults) -> None:
        if current_session is None:
            raise ImportError("bliss")
        defaults.setdefault("_enabled", False)
        defaults.setdefault("trigger_at", "PREPARED")
        defaults.setdefault(
            "parameters",
            {
                detector: {
                    "slope": -0.0688,
                    "energy calibration (meV/px)": 21.5,
                    "points per pixel": 2.7,
                    "low threshold": 0.12,
                    "high threshold": 1,
                    "mask size": 5,
                    "SPC": True,
                    "SPC grid size": 3,
                    "SPC low threshold": 0.2,
                    "SPC high threshold": 1.0,
                    "SPC single event threshold": 0.4,
                    "SPC double event threshold": 1.5,
                }
                for detector in detectors
            },
        )
        self.detectors = detectors

        super().__init__(**defaults)

        if self._enabled:
            self._register_workflow_trigger()
        else:
            self._unregister_workflow_trigger()

    def _register_workflow_trigger(self):
        workflows_category = trigger.register_workflow_category(timing=self.trigger_at)
        workflows_category.set("processing", self._trigger_workflow_on_new_scan)

    def _unregister_workflow_trigger(self):
        trigger.unregister_workflow_category()

    def enable(self):
        self._enabled = True
        self._register_workflow_trigger()

    def disable(self):
        self._enabled = False
        self._unregister_workflow_trigger()

    def setup(self):

        spacer = 8 * " "
        req = "  ".join(
            ["(%d) %s" % (i + 1, det) for i, det in enumerate(self.detectors)]
        )
        ret = input(spacer + "Detector?  " + req + ":  ")

        try:
            det = self.detectors[int(ret[0]) - 1]
        except (ValueError, IndexError):
            print("Detector unknow")
            return

        for par in self.parameters[det].keys():
            old_par = self.parameters[det][par]
            req = "%s (%s):  " % (par, str(old_par))
            ret = input(spacer + req)
            if not ret:
                continue
            try:
                if isinstance(old_par, bool):
                    new_par = bool(ret)
                elif "size" in par:
                    new_par = int(float(ret))
                else:
                    new_par = float(ret)
            except ValueError:
                print("Invalid input")
                continue
            self.parameters[det][par] = new_par

    def _info_categories(self) -> Dict[str, dict]:
        categories = super()._info_categories()
        categories["status"] = {"Enabled": self._enabled}

        return categories

    @autocomplete_property
    def trigger_at(self) -> Optional[int]:
        return self._get_parameter("trigger_at")

    @trigger_at.setter
    def trigger_at(self, value: int):
        self._set_parameter("trigger_at", value)
        if self._enabled:
            self.disable()
            self.enable()

    def _get_workflow(self) -> dict:
        with open(resource_filename("id32", self.WORKFLOW_FILENAME), "r") as wf:
            return json.load(wf)

    def _get_workflow_inputs(self, scan, detector) -> list:
        return [
            {
                "name": "scan_number",
                "value": scan.scan_number,
            },
            {
                "name": "input_path",
                "value": scan.scan_saving.filename,
            },
            {
                "name": "output_path",
                "value": self._get_scan_processed_directory(scan),
            },
            {"name": "detector", "value": detector},
            {"name": "specgen_parameters", "value": dict(self.parameters[detector])},
        ]

    def _get_scan_filename(self, scan) -> str:
        filename = scan.scan_info.get("filename")
        if filename:
            return filename
        return current_session.scan_saving.filename

    def _get_scan_processed_directory(self, scan) -> str:
        return get_dataset_processed_dir(self._get_scan_filename(scan))

    def _get_workflow_destination(self, scan) -> str:
        """Builds the path where the workflow JSON will be saved."""
        filename = self._get_scan_filename(scan)
        scan_nb = scan.scan_info.get("scan_nb")
        root = self._get_scan_processed_directory(scan)
        stem = os.path.splitext(os.path.basename(filename))[0]
        basename = f"{stem}_{scan_nb:04d}.json"
        return os.path.join(root, basename)

    def _trigger_workflow_on_new_scan(self, scan) -> None:
        if not scan.scan_info["save"]:
            return

        for detector in self.detectors:
            if "%s:image" % detector in scan.scan_info["channels"].keys():
                workflow = self._get_workflow()
                inputs = self._get_workflow_inputs(scan, detector)
                kwargs = {"inputs": inputs, "outputs": [{"all": False}]}
                kwargs["convert_destination"] = self._get_workflow_destination(scan)
                submit(args=(workflow,), kwargs=kwargs, queue=self.WORKER)
