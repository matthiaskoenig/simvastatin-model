"""Annotations of the simvastatin models: the compartments and species."""

# the compartments are the shared ones of all models
from pkpdsim.annotations import compartments as compartments
from sbmlutils.metadata import BQB

species: dict[str, list[tuple[BQB, str]]] = {
    "simva": [
        (BQB.IS, "ncit/C29454"),
        (BQB.IS, "chebi/CHEBI:9150"),
        (BQB.IS, "omit/0019802"),
    ],
    "simacid": [
        (BQB.IS, "ncit/C96309"),
        (BQB.IS, "pubchem.substance/64718"),
        (BQB.IS, "inchikey/XWLXKKNPFMNSFA-HGQWONQESA-N"),
    ],
    "simmets": [],
    "simva+simacid": [],
    "active simva inhibitors": [],
    "total simva inhibitors": [],
    "total simva": [],
    "ldlc": [
        (BQB.IS, "efo/0004195"),
        (BQB.IS, "chebi/CHEBI:47774"),
    ],
    "vldlc": [
        (BQB.IS, "chebi/CHEBI:47773"),
    ],
    "cholesterol": [
        (BQB.IS, "chebi/CHEBI:16113"),
        (BQB.IS, "ncit/C369"),
    ],
    "acoa": [
        (BQB.IS, "chebi/CHEBI:15351"),
    ],
    "hmgcoa": [
        (BQB.IS, "ncit/C129007"),
        (BQB.IS, "chebi/CHEBI:15467"),
    ],
    "hmgcoasynthase": [],
    "hmgcoareductase": [
        (BQB.IS, "ncit/C54701"),
    ],
    "ldlr": [
        (BQB.IS, "ncit/C17074"),
    ],
    "ldlr_membrane": [],
    "ldlr_ldlc": [],
    "ldlr_degraded": [],
}
