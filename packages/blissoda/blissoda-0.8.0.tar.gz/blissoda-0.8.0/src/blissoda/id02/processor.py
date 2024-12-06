import os
import logging
from typing import Optional, Any


try:
    from bliss import current_session
except ImportError:
    current_session = None


from ewoksjob.client import submit, get_future

from ..persistent.parameters import (
    autocomplete_property,
    ParameterInfo,
    WithPersistentParameters,
)
from .plotter import Id02Plotter
from ..utils.directories import get_dataset_processed_dir
from ..utils import trigger


logger = logging.getLogger(__name__)


class Id02BaseProcessor(
    WithPersistentParameters,
    parameters=[
        ParameterInfo("_enabled"),
        ParameterInfo("worker", category="workflows"),
        ParameterInfo("trigger_at", category="workflows"),
        ParameterInfo("number_of_scans", category="plotting"),
    ],
):
    DEFAULT_WORKER = None

    def __init__(self, **defaults) -> None:
        if current_session is None:
            raise ImportError("bliss")
        defaults.setdefault("worker", self.DEFAULT_WORKER)
        defaults.setdefault("number_of_scans", 4)
        defaults.setdefault("trigger_at", "PREPARED")
        defaults.setdefault("enabled", False)
        super().__init__(**defaults)

        self._preset = self._set_up_preset()

        self._plotter = Id02Plotter(number_of_scans=self.number_of_scans)
        self._plotter.replot()
        if self._enabled:
            self._register_workflow_trigger()
        else:
            self._unregister_workflow_trigger()

    def _set_up_preset(self):
        raise NotImplementedError()

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

    @autocomplete_property
    def trigger_at(self) -> Optional[int]:
        return self._get_parameter("trigger_at")

    @trigger_at.setter
    def trigger_at(self, value: int):
        self._set_parameter("trigger_at", value)
        if self._enabled:
            self.disable()
            self.enable()

    def scan_requires_processing(self, scan) -> bool:
        return scan.scan_info["save"]

    def get_workflow(self, scan) -> dict:
        dets = [d.name for d in self._preset.getDetectors(scan)]
        return self._preset.buildWorkflow(dets)

    def get_inputs(self, scan) -> list:
        dets = [d.name for d in self._preset.getDetectors(scan)]
        return self._preset.getInputs(scan, dets)

    def get_filename(self, scan) -> str:
        filename = scan.scan_info.get("filename")
        if filename:
            return filename
        return current_session.scan_saving.filename

    def scan_processed_directory(self, scan) -> str:
        return get_dataset_processed_dir(self.get_filename(scan))

    def workflow_destination(self, scan) -> str:
        filename = self.get_filename(scan)
        scan_nb = scan.scan_info.get("scan_nb")
        root = self.scan_processed_directory(scan)
        stem = os.path.splitext(os.path.basename(filename))[0]
        basename = f"{stem}_{scan_nb:04d}.json"
        return os.path.join(root, basename)

    def _trigger_workflow_on_new_scan(self, scan) -> Optional[Any]:
        if not self.scan_requires_processing(scan):
            return None

        workflow = self.get_workflow(scan)
        kwargs = {"inputs": self.get_inputs(scan), "outputs": [{"all": False}]}
        if scan.scan_info.get("save"):
            kwargs["convert_destination"] = self.workflow_destination(scan)

        future = submit(args=(workflow,), kwargs=kwargs, queue=self.worker)

        # TODO: Handle plotting with Flint
        future = get_future(future.task_id)

        return future
