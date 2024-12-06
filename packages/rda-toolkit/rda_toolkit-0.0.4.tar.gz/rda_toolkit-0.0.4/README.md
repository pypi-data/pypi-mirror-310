# rdatools

Redistricting analysis tools (RDA)

This repository ([rdatools/rdatools](https://github.com/rdatools/rdatools)) contains redistricting analysis code. 
There are two associated repositories of data:

*   [rdatools/vtd_data](https://github.com/rdatools/vtd_data) &ndash; Various precinct-level input data for the analysis tools,
    where precincts are generally census VTDs except in a few states which use census blockgroups.
*   [rdatools/vtd_ensembles](https://github.com/rdatools/vtd_ensembles) &ndash; Various output data from the analysis tools,
    including ensembles of plans and scores for plans in ensembles.

## Categories

The code here is organized by area:

- [Base](./docs/base.md): Shared code
- [DCCVT](./docs/dccvt.md): Balzer's algorithm to find a maximally population compact map
- [Ensemble](./docs/ensemble.md): Ensemble generation &amp; scoring code
- [EI](./docs/ei.md): Ecological inference code
- [Rootmap](./docs/rootmap.md): Root maps code
- [Score](./docs/score.md): Scoring code

## Installation

To get the code locally, clone the repository:

```bash
git clone https://github.com/rdatools/rdatools
cd rdatools
```

To run the scripts, install the dependencies:

```bash
pip install -r requirements.txt
```

To use the shared code in another project, install the package:

```bash
pip install rda-toolkit
```

## Testing

```bash
$ pytest
```