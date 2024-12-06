from __future__ import annotations
from typing import List
from ewoksjob.client import submit


from .utils import (
    get_filename,
    master_output_filename,
    task_inputs,
    workflow_destination,
)
from ..processor import BaseProcessor
from ..xrpd.plotter import XrpdPlotter
from ..persistent.parameters import ParameterInfo


try:
    from id09.status import get_xray_energy
except ImportError:
    get_xray_energy = None


class TxsProcessor(
    BaseProcessor,
    parameters=[
        ParameterInfo("distance", category="Txs", doc="meter"),
        ParameterInfo("center", category="Txs", doc="pixel (hor, ver)"),
        ParameterInfo("binning", category="Txs", doc="(hor, ver)"),
        ParameterInfo("detector", category="Txs"),
        ParameterInfo("pixel", category="Txs", doc="meter (hor, ver)"),
        ParameterInfo("energy", category="Txs", doc="eV"),
        ParameterInfo("integrate1d_options", category="Txs"),
    ],
):
    plotter_class = XrpdPlotter

    def __init__(self, **defaults) -> None:
        defaults.setdefault("distance", 1)
        defaults.setdefault("center", (960, 960))
        defaults.setdefault("binning", 2)
        defaults.setdefault("detector", "rayonix")
        defaults.setdefault("pixel", None)
        defaults.setdefault("energy", "automatic")
        defaults.setdefault("integrate1d_options", dict())
        super().__init__(**defaults)

    @property
    def plotter(self) -> XrpdPlotter | None:
        return self._plotter

    def trigger_workflow_on_new_scan(self, scan) -> None:
        if not self.scan_requires_processing(scan):
            return None

        workflow = self.get_workflow(scan)
        kwargs = {"inputs": self.get_inputs(scan), "outputs": [{"all": False}]}
        if scan.scan_info.get("save"):
            kwargs["convert_destination"] = workflow_destination(scan)

        future = submit(args=(workflow,), kwargs=kwargs, queue="celery")

        if self._plotter:
            scan_nb = scan.scan_info.get("scan_nb")
            self._plotter.handle_workflow_result(
                future,
                self.detector,
                scan_name=f"{scan.name}: {scan_nb}.1 {scan.name}",
                output_url=(
                    # TODO: Do not hard-code the output url
                    f"{master_output_filename(scan)}::/{scan_nb}.1/integrate/integrated"
                    if scan.scan_info.get("save")
                    else None
                ),
            )

    def _get_txs_task_identifier(self, scan):
        if scan.scan_info.get("save"):
            return "ewokstxs.tasks.txs.TxsTask"
        return "ewokstxs.tasks.txs.TxsTaskWithoutSaving"

    def get_workflow(self, scan):
        return {
            "graph": {"id": "txs"},
            "nodes": [
                {
                    "id": "txs_task",
                    "task_type": "class",
                    "task_identifier": self._get_txs_task_identifier(scan),
                }
            ],
        }

    def scan_requires_processing(self, scan) -> bool:
        return f"{self.detector}:image" in scan.scan_info.get("channels", dict())

    def get_inputs(self, scan) -> List[dict]:
        if self.energy == "automatic":
            if get_xray_energy is None:
                raise ImportError("Could not import id09.status")
            else:
                energy = get_xray_energy()
        else:
            energy = self.energy

        return task_inputs(
            self._get_txs_task_identifier(scan),
            {
                "scan_key": scan._scan_data.key,
                "filename": get_filename(scan),
                "scan": scan.scan_info.get("scan_nb"),
                "energy": energy,
                "distance": self.distance,
                "center": self.center,
                "detector": self.detector,
                "pixel": self.pixel,
                "binning": (self.binning, self.binning),
                "output_filename": master_output_filename(scan),
                "integrate1d_options": self.integrate1d_options.to_dict(),
            },
        )
