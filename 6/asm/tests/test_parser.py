from asm.parser import parse_line, Label, AInstr, CInstr


def test_parse_label():
    assert parse_line("(LABEL)") == Label("LABEL")


def test_ainstr_dec():
    assert parse_line("@32767") == AInstr(32767)


def test_ainstr_label():
    assert parse_line("@symbol")  == AInstr("symbol")


def test_cinstr_jmp():
    assert parse_line("0;JMP") == CInstr(None, "0", "JMP")


def test_cinstr_dest():
    assert parse_line("M=D") == CInstr("M", "D", None)


def test_comment():
    assert parse_line("  // D = R0 - R1") is None
