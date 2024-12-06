import funcnodes as fn
import rdkit.Chem as Chem


@fn.NodeDecorator(
    id="rdkit.mol2smiles",
    outputs=[{"name": "smiles"}],
)
def mol2smiles(mol: Chem.Mol) -> str:
    return Chem.MolToSmiles(mol)


@fn.NodeDecorator(
    id="rdkit.smiles2mol",
    outputs=[{"name": "mol"}],
    default_render_options={
        "data": {
            "src": "mol",
        }
    },
)
def smiles2mol(smiles: str) -> Chem.Mol:
    return Chem.MolFromSmiles(smiles)


@fn.NodeDecorator(
    id="rdkit.mol2inchi",
    outputs=[{"name": "inchi"}],
)
def mol2inchi(mol: Chem.Mol) -> str:
    return Chem.MolToInchi(mol)


@fn.NodeDecorator(
    id="rdkit.inchi2mol",
    outputs=[{"name": "mol"}],
    default_render_options={
        "data": {
            "src": "mol",
        }
    },
)
def inchi2mol(inchi: str) -> Chem.Mol:
    return Chem.MolFromInchi(inchi)


@fn.NodeDecorator(
    id="rdkit.mol2inchikey",
    outputs=[{"name": "inchikey"}],
)
def mol2inchikey(mol: Chem.Mol) -> str:
    return Chem.MolToInchiKey(mol)


@fn.NodeDecorator(
    id="rdkit.mol2molblock",
    outputs=[{"name": "molblock"}],
)
def mol2molblock(mol: Chem.Mol) -> str:
    return Chem.MolToMolBlock(mol)


@fn.NodeDecorator(
    id="rdkit.molblock2mol",
    outputs=[{"name": "mol"}],
    default_render_options={
        "data": {
            "src": "mol",
        }
    },
)
def molblock2mol(molblock: str) -> Chem.Mol:
    return Chem.MolFromMolBlock(molblock)


@fn.NodeDecorator(
    id="rdkit.mol2smarts",
    outputs=[{"name": "smarts"}],
)
def mol2smarts(mol: Chem.Mol) -> str:
    return Chem.MolToSmarts(mol)


@fn.NodeDecorator(
    id="rdkit.smarts2mol",
    outputs=[{"name": "mol"}],
    default_render_options={
        "data": {
            "src": "mol",
        }
    },
)
def smarts2mol(smarts: str) -> Chem.Mol:
    return Chem.MolFromSmarts(smarts)


@fn.NodeDecorator(
    id="rdkit.mol2svg",
    outputs=[{"name": "svg"}],
)
def mol2svg(mol: Chem.Mol) -> str:
    return Chem.MolToSVG(mol)


# @fn.NodeDecorator(
#     id="rdkit.moleditor",
#     outputs=[{"name": "mol"}],
#     default_render_options={
#         "data": {
#             "src": "inmol",
#         }
#     },
# )
# def moleditor(
#     inmol: Chem.EditableMol = Chem.EditableMol(Chem.MolFromSmiles("C"))
# ) -> Chem.Mol:
#     return inmol.GetMol()


NODE_SHELF = fn.Shelf(
    nodes=[
        # moleditor,
        mol2smiles,
        smiles2mol,
        mol2inchi,
        inchi2mol,
        mol2inchikey,
        mol2molblock,
        molblock2mol,
        mol2smarts,
        smarts2mol,
    ],
    subshelves=[],
    name="Mol",
    description="Molecular operations",
)
