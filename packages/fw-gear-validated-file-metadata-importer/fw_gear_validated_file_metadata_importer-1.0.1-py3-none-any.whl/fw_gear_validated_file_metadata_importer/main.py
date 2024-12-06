import logging
import sys
import typing as t
from pathlib import Path

import flywheel
from fw_meta import MetaData

from .files import dicom, nifti
from .util import FILETYPES

AnyPath = t.Union[str, Path]

log = logging.getLogger(__name__)


def project_tag_update(project: flywheel.Project = None) -> None:
    """Helper function to update dicom allow/deny tag list"""
    if project:
        log.info("Updating allow/deny tag list from project.info.context.header.dicom.")
        # Updating allow/deny tag list from project.info.context.header.dicom
        dicom.update_array_tag(
            project.info.get("context", {}).get("header", {}).get("dicom", {})
        )


def run(
    file_type: t.Union[str, None],
    file_path: AnyPath,
    project: flywheel.Project = None,
    siemens_csa: bool = False,
    derived: bool = False,
) -> t.Tuple[t.Dict, MetaData, t.Dict]:
    """Processes file at file_path.

    Args:
        file_type (str): String defining file type.
        file_path (AnyPath): A Path-like to file input.
        project (flywheel.Project): The flywheel project the file is originating
            (Default: None).
        siemens_csa (bool): If True parse Siemens CSA DICOM header (Default: False).
        derived (bool): If True, generate derived metadata (Default: False).

    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.
        dict: Dictionary containing the qc metrics.

    """
    project_tag_update(project)
    log.info("Processing %s...", file_path)

    if file_type is None:
        log.info("Could not find file type, trying to determine file type from suffix")
        name = str(file_path)
        for ft, suffixes in FILETYPES.items():
            if any([name.endswith(suffix) for suffix in suffixes]):
                file_type = ft
                break
        if file_type is None:
            log.error("Could not determine file type from suffix.")
            sys.exit(1)

    if file_type == "dicom":
        fe, meta, qc = dicom.process(
            file_path, siemens_csa=siemens_csa, derived=derived
        )
    elif file_type == "nifti":
        fe, meta, qc = nifti.process(file_path)
    else:
        log.error("File type %s is not supported currently.", file_type)
        sys.exit(1)

    return fe, meta, qc
