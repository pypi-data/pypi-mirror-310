import funcnodes as fn
import rdkit.Chem as Chem
from .mol import NODE_SHELF as mol_shelf
from .svg import mol_to_svg
import os

FUNCNODES_RENDER_OPTIONS: fn.RenderOptions = {
    "typemap": {
        Chem.Mol: "svg",
    },
}

# REACT_PLUGIN = {
#     "js": [
#         os.path.join(
#             os.path.dirname(__file__), "react_plugin", "js", "ChemDoodleWeb.js"
#         ),
#     ],
#     "module": os.path.join(
#         os.path.dirname(__file__), "react_plugin", "js", "main.js"
#     ),  #
#     "css": [
#         os.path.join(
#             os.path.dirname(__file__), "react_plugin", "css", "jquery-ui-1.11.4.css"
#         ),
#     ],
# }


def molsvgencoder(obj, preview=False):
    if isinstance(obj, Chem.Mol):
        print("molsvgencoder", obj, preview)
        if preview:
            return mol_to_svg(obj, size=(200, 200)), True
        else:
            return mol_to_svg(obj, size=(500, 500)), True
    return None, False


# def editable_mol_encoder(obj, preview=False):
#     try:
#         print("AAAA", obj)
#         print(Chem.MolToMolBlock(obj.GetMol()))
#     except Exception as e:
#         pass
#     if isinstance(obj, Chem.rdchem.EditableMol):
#         return Chem.MolToMolBlock(obj.GetMol()), True
#     return None, False


fn.JSONEncoder.add_encoder(molsvgencoder)
# fn.JSONEncoder.add_encoder(editable_mol_encoder)

NODE_SHELF = fn.Shelf(
    nodes=[],
    subshelves=[mol_shelf],
    name="RDKit",
    description="RDKit nodes",
)
