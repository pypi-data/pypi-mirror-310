"""
CONFIG INFO FOR frcw.rs (Fastest ReCom Chain in the West)

bin/frcw 
--graph-json <graph_json>           The path of the dual graph (in NetworkX format).
--n-steps <n_steps>                 The number of proposals to generate.
--tol <tol>                         The relative population tolerance.
--pop-col <pop_col>                 The name of the total population column in the graph metadata.
--assignment-col <assignment_col>   The name of the assignment column in the graph metadata.
--balance-ub <balance_ub>           The normalizing constant (reversible ReCom only).
--n-threads <n_threads>             The number of threads to use.
--batch-size <batch_size>           The number of proposals per batch job.
--rng-seed <rng_seed>               The seed of the RNG used to draw proposals.
--variant <variant>                 The ReCom variant to use (A, AW, reversible, etc.).
--writer <writer>                   The writer to use (canonical, jsonl, jsonl-full, tsv, etc.).
--sum_cols <sum_cols>               The columns to sum in the graph metadata.
--region-weights <region_weights>   Region columns with weights for region-aware ReCom.
"""

from typing import Any, List, Dict, NamedTuple, Optional

import os, json

from .metautils import make_ensemble_metadata
from .ensemble_io import Plan, Metadata


class frcwConfig(NamedTuple):
    """Configuration for frcw.rs"""

    graph_json: str
    n_steps: int
    tol: float
    pop_col: str
    assignment_col: str
    # balance_ub: float                 # Not used
    n_threads: int
    batch_size: int
    rng_seed: int
    variant: str
    writer: str
    # sum_cols: List[str]               # Not used
    region_weights: str

    def to_dict(self):
        as_dict: Dict[str, Any] = self._asdict()

        return as_dict


def population_balance_tolerance(plan_type: str) -> float:
    """
    The +/- deviation from target tolerance for population balance by type of plan.
    See "Recombination: A Familyof Markov Chains for Redistricting" (P.14).

    NOTE: This is different from a 'roughly equal' (max - min) / target.
    """

    pop_tol: float = {
        "congress": 0.01,
        "upper": 0.05,
        "lower": 0.05,
    }[plan_type]

    return pop_tol


def region_surcharge(plan_type: str) -> float:
    """The surcharge for region-aware ReCom by type of plan."""

    return 0.25


def configure_frcw(
    state: str,
    plan_type: str,
    n_districts: int,
    size: int,
    graph_json: str,
    *,
    offset: int = 0,
    n_threads: int = 1,  # TODO - Todd
    batch_size: int = 1,  # TODO - Todd
    # To enable testing of these parameters
    pop_tol_test: Optional[float] = None,
    county_weight_test: Optional[float] = None,
) -> frcwConfig:
    """Configure frcw.rs"""

    # Set the tolerance for population balance
    pop_tol: float = (
        pop_tol_test if pop_tol_test else population_balance_tolerance(plan_type)
    )

    # Set the bias against splitting counties
    county_weight: float = (
        county_weight_test if county_weight_test else region_surcharge(plan_type)
    )

    # Generate a seed for the RNG
    seed: int = 1 + offset
    # seed: int = starting_seed(state, n_districts) + offset

    # Convert a Dict[str, float] to a JSON string
    region_weights: Dict[str, float] = {"COUNTY": county_weight}
    json_string: str = json.dumps(region_weights)
    json_string = json_string.replace(",", " ,")
    region_weight_arg: str = "'" + json_string + "'"

    # Map friendly variant names to frcw.rs variant names
    variant_dict = {
        "A": "cut-edges-rmst",
        "B": "district-pairs-rmst",
        "C": "cut-edges-ust",
        "D": "district-pairs-ust",
        "R": "reversible",
        "AW": "cut-edges-region-aware",
        "BW": "district-pairs-region-aware",
    }  # Cloned from RecomRunnerConfig in mggg/gerrytools

    config = frcwConfig(
        graph_json=graph_json,
        n_steps=size,
        tol=pop_tol,
        pop_col="TOTAL_POP",
        assignment_col="INITIAL",
        n_threads=n_threads,
        batch_size=batch_size,
        rng_seed=seed,
        variant=variant_dict["AW"],
        writer="canonical",
        region_weights=region_weight_arg,
    )

    return config


def frcw_metadata(
    state: str, n_districts: int, size: int, args_dict, config: frcwConfig
) -> Metadata:
    """Create a metadata record for the frcw.rs run."""

    ensemble_metadata: Dict[str, Any] = make_ensemble_metadata(
        xx=state,
        ndistricts=n_districts,
        size=size,
        method="frcw",
    )
    ensemble_metadata.update(args_dict)

    ensemble_metadata.update(config.to_dict())
    metadata_record: Metadata = {
        "_tag_": "metadata",
        "properties": ensemble_metadata,
    }

    return metadata_record


def official_plan_proxy(official_csv: List[Dict[str, Any]]) -> Plan:
    """Create a record for an official plan proxy."""

    official_assignments: Dict[str, int | str] = {
        str(row["GEOID20"]): row["District"] for row in official_csv
    }
    plan_record: Plan = {
        "_tag_": "plan",
        "name": "official-proxy",
        "plan": official_assignments,
    }

    return plan_record


def run_frcw(
    config: frcwConfig, *, frcw_path: str = "bin/frcw", verbose: bool = False
) -> None:
    """Run frcw.rs"""

    command: str = f"""{frcw_path} \
    --graph-json {config.graph_json} \
    --n-steps {config.n_steps} \
    --tol {config.tol} \
    --pop-col {config.pop_col} \
    --assignment-col {config.assignment_col} \
    --n-threads {config.n_threads} \
    --batch-size {config.batch_size} \
    --rng-seed {config.rng_seed} \
    --variant {config.variant} \
    --writer {config.writer} \
    --region-weights {config.region_weights}
    """

    command = " ".join(command.split())

    if verbose:
        print(command)
    os.system(command)


### END ###
