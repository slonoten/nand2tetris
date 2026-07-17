import re

from dataclasses import dataclass


A_COMP_CODES = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "A": "110000",
    "!D": "001101",
    "!A": "110001",
    "-D": "001111",
    "-A": "110111",
    "D+1": "011111",
    "A+1": "110111",
    "D-1": "001110",
    "A-1": "110110",
    "D+A": "000110",
    "D-A": "010111",
    "A-D": "000111",
    "D&A": "000000",
    "D|A": "010101"
}

M_COMP_CODES = {
    "M": "110000",
    "!M": "110001",
    "-M": "110111",
    "M+1": "110111",
    "M-1": "110110",
    "D+M": "000110",
    "D-M": "010111",
    "M-D": "000111",
    "D&M": "000000",
    "D|M": "010101"
}

COMP_CODES = {comp : "0" + code for comp, code in A_COMP_CODES.items()} | \
    {comp : "1" + code for comp, code in A_COMP_CODES.items()}


JUMP_TO_CODE = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

def dest_to_code(dest: str) -> str:
    return "".join("1" if reg in dest else "0" for reg in ("A", "D", "M"))


LINE_PATTERN = "\(\)"


@dataclass
class CInstr:
    pass


def parse(lines: list[str]) -> list[str]:
    return []