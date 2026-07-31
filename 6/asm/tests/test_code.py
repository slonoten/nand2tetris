from asm.parser import CInstr
from asm.code import dest_to_code, assemble_cinstr


def test_dest_to_code():
    assert dest_to_code(None) == "000"
    assert dest_to_code("ADM") == "111"
    assert dest_to_code("AM") == "101"
    assert dest_to_code("D") == "010"


def test_asssemle_cinstr():
    assert assemble_cinstr(CInstr("M", "1", None)) == "1110111111001000"

