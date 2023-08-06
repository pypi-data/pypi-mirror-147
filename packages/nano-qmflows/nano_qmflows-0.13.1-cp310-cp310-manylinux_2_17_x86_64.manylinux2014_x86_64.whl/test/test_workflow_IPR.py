"""Test the IPR workflow."""
import os
import shutil
import sys
from os.path import join
from pathlib import Path

from nanoqm.workflows.input_validation import process_input
from nanoqm.workflows.workflow_ipr import workflow_ipr

from .utilsTest import PATH_TEST


def test_workflow_IPR(tmp_path: Path) -> None:
    """Test the Inverse Participation Ratio workflow."""
    file_path = PATH_TEST / 'input_test_IPR.yml'
    config = process_input(file_path, 'ipr_calculation')
    # create scratch path
    shutil.copy(config.path_hdf5, tmp_path)
    config.path_hdf5 = join(tmp_path, "Cd33Se33.hdf5")
    config.workdir = tmp_path

    try:
        workflow_ipr(config)
        os.remove("IPR.txt")
    except Exception as ex:
        raise AssertionError(f"Unxpected error for scratch_path {tmp_path!r}") from ex
