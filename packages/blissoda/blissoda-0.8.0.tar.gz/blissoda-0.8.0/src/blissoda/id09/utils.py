from typing import Any, List
import os

from ..utils.directories import get_dataset_processed_dir


def task_inputs(task_identifier: str, inputs: dict[str, Any]) -> List[dict]:
    return [
        dict(task_identifier=task_identifier, name=key, value=value)
        for key, value in inputs.items()
    ]


def get_filename(scan) -> str:
    filename = scan.scan_info.get("filename")
    if filename:
        return filename

    from bliss import current_session

    return current_session.scan_saving.filename


def scan_processed_directory(scan) -> str:
    return get_dataset_processed_dir(get_filename(scan))


def workflow_destination(scan) -> str:
    filename = get_filename(scan)
    scan_nb = scan.scan_info.get("scan_nb")
    root = scan_processed_directory(scan)
    stem = os.path.splitext(os.path.basename(filename))[0]
    basename = f"{stem}_{scan_nb:04d}.json"
    return os.path.join(root, basename)


def master_output_filename(scan) -> str:
    """Filename which can be used to inspect the results after the processing."""
    filename = get_filename(scan)
    root = scan_processed_directory(scan)
    basename = os.path.basename(filename)
    return os.path.join(root, basename)
