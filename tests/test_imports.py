import importlib

MODULES = [
    "hoi4modtools.statemap",
    "hoi4modtools.focusgfx",
    "hoi4modtools.focusshine",
    "hoi4modtools.ideagfx",
    "hoi4modtools.localisation",
    "hoi4modtools.manpower",
    "hoi4modtools.transfertech",
    "hoi4modtools.fileformatter",
    "hoi4modtools.newsheader",
    "hoi4modtools.minister_converter",
    "hoi4modtools.usa_election",
]


def test_modules_importable():
    for module in MODULES:
        importlib.import_module(module)
