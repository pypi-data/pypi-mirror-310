"""
SCORE AN ENSEMBLE OF PLANS
"""

from typing import List, Dict, Set, Any, Callable, TextIO

import warnings
import time
import csv
from collections import OrderedDict


from ..base import (
    # mkPoints,
    # Point,
    # index_points,
    # IndexedPoint,
    # populations,
    # index_geoids,
    # index_assignments,
    Assignment,
    # IndexedWeightedAssignment,
    # calc_energy,
)
from ..score import analyze_plan
from .ensemble_io import read_record, format_scores
from .utils import make_assignments


def score_ensemble(
    ensemble_stream: TextIO,
    scores_stream: TextIO,
    data: Dict[str, Dict[str, int | str]],
    shapes: Dict[str, Any],
    graph: Dict[str, List[str]],
    metadata: Dict[str, Any],
    *,
    which: str = "all",
    more_data: Dict[str, Any] = {},
    more_scores_fn: Callable[..., Dict[str, float | int]],
    verbose: bool = False,
) -> None:
    """Score an ensemble of plans."""

    tic: float = time.perf_counter()
    warnings.warn("Starting scoring plans ...")

    # 11-15-24 -- Commented out unnecessary scoring to improve performance

    # points: List[Point] = mkPoints(data, shapes)

    # indexed_geoids: Dict[str, int] = index_geoids(points)
    # indexed_points: List[IndexedPoint] = index_points(points)

    # ipop_by_geoid: Dict[str, int] = populations(data)
    # epsilon: float = 0.01  # Minimum population per precinct
    # fpop_by_geoid: Dict[str, float] = {
    #     k: float(max(epsilon, v)) for k, v in ipop_by_geoid.items()
    # }

    # Read & score each plan

    for i, line in enumerate(ensemble_stream):
        try:
            # Skip the metadata record
            in_record: Dict[str, Any] = read_record(line)
            if i == 0:
                assert in_record["_tag_"] == "metadata"
                continue

            # Score each plan record
            assert in_record["_tag_"] == "plan"

            plan_name: str = in_record["name"]
            if verbose:
                print(f"Scoring {i}: {plan_name} ...")

            plan: Dict[str, int | str] = in_record["plan"]
            assignments: List[Assignment] = make_assignments(plan)

            # 11-15-24 -- Commented out unnecessary scoring to improve performance

            # indexed_assignments: List[IndexedWeightedAssignment] = index_assignments(
            #     assignments, indexed_geoids, fpop_by_geoid
            # )

            # Make sure districts are indexed [1, 2, 3, ...]
            # district_ids: Set[int | str] = set()
            # for a in assignments:
            #     district_ids.add(a.district)
            # if min(district_ids) != 1:
            #     warnings.warn("Exiting: Districts must be indexed [1, 2, 3, ...]")
            #     sys.exit(1)

            # energy: float = calc_energy(indexed_assignments, indexed_points)

            out_record: OrderedDict[str, Any] = OrderedDict()
            out_record["map"] = plan_name  # The "join" key

            scorecard: Dict[str, Any] = analyze_plan(
                assignments,
                data,
                shapes,
                graph,
                metadata,
                which=which,
            )

            # Remove by-district compactness & splitting from from the scores
            by_district: List[Dict[str, float]] = scorecard.pop("by_district")

            # Add the (flat) scores
            out_record.update(scorecard)

            if which == "all" or which == "extended":
                # Compute additional scores, if specified
                if more_data and more_scores_fn:
                    more_scores: Dict[str, float | int] = more_scores_fn(
                        out_record,
                        by_district,
                        assignments,
                        data,
                        shapes,
                        graph,
                        metadata,
                        more_data,
                    )
                    out_record.update(more_scores)

            # Write the scores to the output stream
            if i == 1:
                cols: List[str] = list(out_record.keys())
                writer: csv.DictWriter = csv.DictWriter(scores_stream, fieldnames=cols)
                writer.writeheader()

            writer.writerow(format_scores(out_record))

            pass

        except Exception as e:
            warnings.warn(f"Exception: {e}")
            pass

    toc: float = time.perf_counter()
    warnings.warn(f"Done. Elapsed time = {toc - tic: 0.1f} seconds.")

    return


### END ###
