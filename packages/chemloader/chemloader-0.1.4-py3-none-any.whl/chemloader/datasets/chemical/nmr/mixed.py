from chemloader import MolDataLoader, DataDownloader, MolToStoragePipeline
from chemloader.config import MISSMATCH_PREFIX
from tqdm import tqdm
from rdkit import Chem
import re
from rdkit import RDLogger

import warnings
import json


def identity(x):
    return x


def parse_assignments(assignments):
    _assignments = {}
    for am in assignments.split("\n"):
        am = am.strip("\\")
        s_id, ppm, *atom_ids = am.split(", ")
        if s_id in _assignments:
            raise ValueError(f"Duplicate assignment {s_id}")
        _assignments[s_id] = [[int(aid) for aid in atom_ids], float(ppm)]

    return _assignments


def parse_larmors(line):
    lines = line.split("\n")
    lines = [_l.strip("\\").strip() for _l in lines]

    assignments = {}
    for _l in lines:
        if _l.startswith("Spectrum_Location="):
            continue
        if _l.startswith("Larmor="):
            continue

        ppm, label = _l.split(", ")
        ppm = float(ppm)
        label = label.replace("L=", "").strip()
        if label in assignments:
            if assignments[label] != ppm:
                raise ValueError(f"Duplicate label {label}")
        assignments[label] = ppm

    return assignments


parser_functions = {
    "NMREDATA_VERSION": identity,
    "NMREDATA_SOLVENT": identity,
    "NMREDATA_LEVEL": identity,
    "AUTHOR_SUBMITTER": identity,
    "NMREDATA_ID": identity,
    "NMREDATA_SMILES": identity,
    "NMREDATA_INCHI": identity,
    "AUTHOR_SUPPLIER": identity,
    "CHEMNAME": identity,
    "NMREDATA_2D_13C_NJ_15N": identity,
    "NMREDATA_2D_1H_NJ_15N": identity,
    "NMREDATA_ASSIGNMENT": parse_assignments,
    "AUTHOR_LITERATURE": identity,
    "NMREDATA_1D_1H_D_1H": identity,
    "NMREDATA_1D_1H": parse_larmors,
    "NMREDATA_1D_13C": parse_larmors,
    "NMREDATA_1D_19F": parse_larmors,
    "NMREDATA_1D_31P": parse_larmors,
    "NMREDATA_1D_15N": parse_larmors,
    "NMREDATA_1D_17O": parse_larmors,
    "NMREDATA_1D_11B": parse_larmors,
    "NMREDATA_1D_29Si": parse_larmors,
    "NMREDATA_1D_33S": parse_larmors,
    "NMREDATA_1D_195Pt": parse_larmors,
    "NMREDATA_2D_1H_NJ_1H": identity,
    "NMREDATA_2D_1H_NJ_13C": identity,
    "NMREDATA_TEMPERATURE": identity,
    "NMREDATA_1D_73Ge": parse_larmors,
}


def _remove_trailing(x):
    return str(x).strip("\\") if str(x).endswith("\\") else x


def parse_props(mol):
    raw_props = mol.GetPropsAsDict()

    for k, v in raw_props.items():
        raw_props[k] = _remove_trailing(v)

    for k, v in raw_props.items():
        if k in parser_functions:
            raw_props[k] = parser_functions[k](v)
            continue
        else:
            if "#" in k:
                base = k.split("#")[0]
                if base in parser_functions:
                    raw_props[k] = parser_functions[base](v)
                    continue
        warnings.warn(f"Unknown property {k}")

    return raw_props


class WrongElementError(ValueError):
    pass


def assignElementShifts(mol, props, p, element):
    spec_assignments = props[p]
    all_assignments = props["NMREDATA_ASSIGNMENT"]
    for s_id, ppm in spec_assignments.items():
        if s_id not in all_assignments:
            raise ValueError(f"Missing assignment {s_id}")
        if not all_assignments[s_id][1] == ppm:
            raise ValueError(f"Assignment mismatch {s_id}")

        atom_idxs = all_assignments[s_id][0]
        for idx in atom_idxs:
            atom = mol.GetAtomWithIdx(idx - 1)
            if atom.GetSymbol() != element:
                raise WrongElementError(f"Atom {idx} is not {element}")

            if atom.HasProp(MISSMATCH_PREFIX + "shift"):
                prev_ppm = json.loads(atom.GetProp(MISSMATCH_PREFIX + "shift"))
                prev_ppm.append(ppm)
                atom.SetProp(MISSMATCH_PREFIX + "shift", json.dumps(prev_ppm))
            elif atom.HasProp("shift"):
                prev_ppm = atom.GetDoubleProp("shift")
                if prev_ppm == ppm:
                    continue
                atom.SetProp(MISSMATCH_PREFIX + "shift", json.dumps([prev_ppm, ppm]))
                atom.ClearProp("shift")
            else:
                atom.SetDoubleProp("shift", ppm)


class NmrShiftDb2Loader(MolToStoragePipeline):
    def setup(self, dataloader, previous_step=None, force=False):
        self.fallback = "index"
        self.presetup(dataloader)
        RDLogger.DisableLog("rdApp.warning")
        try:
            with open(previous_step.raw_file, "rb") as f:
                for idx, mol in tqdm(
                    enumerate(
                        Chem.ForwardSDMolSupplier(f, sanitize=False, removeHs=False)
                    ),
                    total=dataloader.expected_data_size,
                ):
                    c13 = mol.HasProp("NMREDATA_1D_13C")
                    h1 = mol.HasProp("NMREDATA_1D_1H")
                    f19 = mol.HasProp("NMREDATA_1D_19F")
                    p31 = mol.HasProp("NMREDATA_1D_31P")
                    n15 = mol.HasProp("NMREDATA_1D_15N")
                    o17 = mol.HasProp("NMREDATA_1D_17O")
                    b11 = mol.HasProp("NMREDATA_1D_11B")
                    si29 = mol.HasProp("NMREDATA_1D_29Si")
                    s33 = mol.HasProp("NMREDATA_1D_33S")
                    pt195 = mol.HasProp("NMREDATA_1D_195Pt")
                    c13_2d = mol.HasProp("NMREDATA_2D_1H_NJ_13C")
                    h1_2d = mol.HasProp("NMREDATA_2D_1H_NJ_1H")
                    if not (
                        c13
                        or h1
                        or f19
                        or p31
                        or o17
                        or n15
                        or b11
                        or si29
                        or s33
                        or pt195
                    ):
                        if c13_2d or h1_2d:
                            continue  # skip 2d data
                        raise ValueError(f"No 1D-NMR data only {mol.GetPropNames()}")

                    if mol.GetProp("NMREDATA_ASSIGNMENT").strip() == "":
                        continue
                    props = parse_props(mol)

                    for p in props:
                        if p.startswith("NMREDATA_1D_"):
                            isotope = p.replace("NMREDATA_1D_", "").split("#")[
                                0
                            ]  # e.g. 13C
                            elementsymbol = re.sub(r"[0-9]+", "", isotope)  # e.g. C
                            if len(elementsymbol) == 0 or len(elementsymbol) > 2:
                                continue
                            try:
                                assignElementShifts(mol, props, p, elementsymbol)
                            except WrongElementError:
                                continue
                            except Exception:
                                print(props)
                                print(p)
                                raise

                    self.setupstep(dataloader, mol, index=idx)

        finally:
            RDLogger.EnableLog("rdApp.warning")
            self.postsetup()


class NmrShiftDb2(MolDataLoader):
    expected_data_size = 63867
    expected_mol = 63789

    setup_pipleline = [
        DataDownloader(
            src="https://sourceforge.net/projects/nmrshiftdb2/files/data/nmrshiftdb2.nmredata.sd/download",
            raw_file_name="nmrshiftdb2.nmredata.sd",
        ),
        NmrShiftDb2Loader(),
    ]
