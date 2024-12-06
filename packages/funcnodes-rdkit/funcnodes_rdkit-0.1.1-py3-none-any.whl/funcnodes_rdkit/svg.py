from rdkit import Chem
from rdkit.Chem import Draw


def mol_to_svg(mol: Chem.Mol, size=(300, 300)) -> str:
    d2d = Draw.MolDraw2DSVG(*size)
    d2d.DrawMolecule(mol)
    d2d.FinishDrawing()
    text = d2d.GetDrawingText()
    return text
