from pathlib import Path

import pytest

from asm.parser import CInstr
from asm.code import dest_to_code, assemble_cinstr, assemble

BASE_DIR = Path(__file__).parent.parent.parent

def test_dest_to_code():
    assert dest_to_code(None) == "000"
    assert dest_to_code("ADM") == "111"
    assert dest_to_code("AM") == "101"
    assert dest_to_code("D") == "010"


def test_assemble_cinstr():
    assert assemble_cinstr(CInstr("M", "1", None)) == "1110111111001000"
    assert assemble_cinstr(CInstr("D", "D+A", None)) == "1110000010010000"

@pytest.mark.parametrize(
    "asm_path", 
    [
        BASE_DIR / "add" / "Add.asm",
        BASE_DIR / "max" / "MaxL.asm",
        BASE_DIR / "rect" / "RectL.asm",
        BASE_DIR / "max" / "Max.asm",
    ]
)
def test_assemble(asm_path):
    asm_text = asm_path.read_text()
    hack = asm_path.with_suffix(".hack").read_text().split("\n")
    assert assemble(asm_text.split("\n")) == hack