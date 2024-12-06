from __future__ import annotations
from typing import Dict, Optional


from .flint.plotter import BasePlotter
from .persistent.parameters import ParameterInfo, WithPersistentParameters
from .persistent.parameters import autocomplete_property
from .utils import trigger


class BaseProcessor(
    WithPersistentParameters,
    parameters=[
        ParameterInfo("_enabled"),
        ParameterInfo("_plotting_enabled"),
        ParameterInfo("trigger_at", category="workflows"),
        ParameterInfo("number_of_scans", category="plotting"),
    ],
):
    plotter_class = BasePlotter

    def __init__(self, **defaults) -> None:
        defaults.setdefault("_enabled", False)
        defaults.setdefault("_plotting_enabled", True)
        defaults.setdefault("number_of_scans", 4)
        super().__init__(**defaults)

        if self._enabled:
            self._register_workflow_trigger()
        else:
            self._unregister_workflow_trigger()

        if self._plotting_enabled:
            self._plotter = self.plotter_class(self.number_of_scans)
            self._plotter.replot()
        else:
            self._plotter = None

    @property
    def plotter(self) -> plotter_class | None:
        return self._plotter

    def enable_plotting(self):
        if self._plotter is not None:
            return
        self._plotter = self.plotter_class(self.number_of_scans)
        self._plotter.replot()
        self._plotting_enabled = True

    def disable_plotting(self):
        if self._plotter is None:
            return
        self.stop_plotting_tasks()
        self._plotter = None
        self._plotting_enabled = False

    def clear_plots(self) -> None:
        if self._plotter:
            return self._plotter.clear()
        else:
            print("Plotting is disabled")

    def replot(self) -> None:
        if self._plotter:
            return self._plotter.replot()
        else:
            print("Plotting is disabled")

    def purge_plotting_tasks(self) -> int:
        if self._plotter:
            return self._plotter.purge_tasks()
        else:
            print("Plotting is disabled")
            return 0

    def stop_plotting_tasks(self) -> int:
        if self._plotter:
            return self._plotter.kill_tasks()
        else:
            print("Plotting is disabled")
            return 0

    @autocomplete_property
    def number_of_scans(self) -> int:
        return self._get_parameter("number_of_scans")

    @number_of_scans.setter
    def number_of_scans(self, value: int):
        self._plotter.number_of_scans = value
        self._set_parameter("number_of_scans", self._plotter.number_of_scans)

    @autocomplete_property
    def trigger_at(self) -> Optional[int]:
        return self._get_parameter("trigger_at")

    @trigger_at.setter
    def trigger_at(self, value: int):
        self._set_parameter("trigger_at", value)
        if self._enabled:
            self.disable()
            self.enable()

    def _info_categories(self) -> Dict[str, dict]:
        categories = super()._info_categories()
        categories["status"] = {
            "Enabled": self._enabled,
            "Plots in Flint": self._plotter is not None,
        }
        if self._plotter:
            categories["status"]["Plotting tasks"] = self._plotter.purge_tasks()
        return categories

    def enable(self):
        self._enabled = True
        self._register_workflow_trigger()

    def disable(self):
        self._enabled = False
        self._unregister_workflow_trigger()

    def _register_workflow_trigger(self):
        workflows_category = trigger.register_workflow_category()
        workflows_category.set("processing", self.trigger_workflow_on_new_scan)

    def _unregister_workflow_trigger(self):
        trigger.unregister_workflow_category()

    def trigger_workflow_on_new_scan(self, scan) -> None:
        raise NotImplementedError()
