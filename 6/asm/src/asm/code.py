from typing import Iterable
from asm.parser import CInstr, AInstr


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
    {comp : "1" + code for comp, code in M_COMP_CODES.items()}

JUMP_TO_CODE = {
    None: "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

PREDEFINED_SYMBOLS = {f"R{i}": i for i in range(15)} | {symb: i for i, symb in enumerate(("SP", "LCL", "ARG", "THIS", "THAT"))} 


def dest_to_code(dest: str | None) -> str:
    if not dest:
        return "000"
    return "".join("1" if reg in dest else "0" for reg in ("A", "D", "M"))


def assemble_cinstr(cinstr: CInstr) -> str:
    dest_code = dest_to_code(cinstr.dest)
    comp_code = COMP_CODES.get(cinstr.comp)
    if not comp_code:
        raise RuntimeError(f"Invalid comp \"{cinstr.comp}\"")
    jump_code = JUMP_TO_CODE[cinstr.jump]
    return f"111{comp_code}{dest_code}{jump_code}"


def assemble(lines: Iterable[str]) -> Iterable[str]:
    label_to_addr : dict[str, int | list[int]] = {}  # label name to address or to list of a-insruction addresses

    next_instr_addr = 0
    code: list[str | None] = []
    for line_num, parse_res in parse(lines):
        if is_instance(parse_res, CInstr):
            code.append(assemble_cinstr(parse_res))
        elif is_instance(parse_res, AInstr):
            if is_instance(parse_res.addr, int):
                code.append(addr_to_code(parse_res.addr))
            else:
                label = parse_res.addr
                addr = label_to_addr.get(label)
                if addr is None:
                    label_to_addr[label] = [next_instr_addr]
                    code.append(None)
                elif is_instance(addr, int):
                    code.append(addr_to_code(addr))
                elif is_instance(addr, list):
                    addr.append(next_instr_addr)
                else:
                    assert False, f"Invalid address value type {type(addr)}"
        if is_instance(parse_res, Label):
            addr = label_to_addr.get(parse_result.label)
            if addr is None:  # first label occurience
                label_to_addr[label] = next_instr_addr
            elif is_instance(addr, str):
                raise RuntimeError(f"Error: label \"{parse_result.label}\" redefined at line {line_num}")
            elif is_instance(addr, list):
                for inst_addr in addr:
                    assert code[inst_addr] is None
                    code[inst_addr] = next_instr_addr
                    label_to_addr
        else:
            next_instr_addr += 1

