"""
ENSEMBLE & SCORES METADATA
"""

from typing import Any, Dict

import os, pwd, datetime
from importlib.metadata import version


def shared_metadata(
    xx: str,
    repo: str,
    *,
    cycle: str = "2020",
    plan_type: str = "congress",
) -> Dict[str, Any]:
    """Create the shared metadata for ensembles and scores."""

    shared: Dict[str, Any] = dict()

    shared["username"] = pwd.getpwuid(os.getuid()).pw_name

    timestamp = datetime.datetime.now()
    shared["date_created"] = timestamp.strftime("%x")
    shared["time_created"] = timestamp.strftime("%X")

    shared["repository"] = repo

    shared["state"] = xx
    shared["cycle"] = cycle
    shared["plan_type"] = plan_type
    shared["units"] = "VTD"

    return shared


def make_ensemble_metadata(
    *,
    xx: str,
    ndistricts: int,
    size: int,
    method: str,
    repo: str = "rdatools/rdaensemble",
) -> Dict[str, Any]:
    """Create the metadata for an ensemble."""

    ensemble: Dict[str, Any] = shared_metadata(xx, repo)

    ensemble["ndistricts"] = ndistricts
    ensemble["method"] = method
    ensemble["size"] = size

    return ensemble


### END ###
