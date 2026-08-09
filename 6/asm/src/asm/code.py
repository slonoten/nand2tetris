from typing import Iterable
from asm.parser import CInstr, AInstr, parse, Label


A_COMP_CODES = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "A": "110000",
    "!D": "001101",
    "!A": "110001",
    "-D": "001111",
    "-A": "110011",
    "D+1": "011111",
    "A+1": "110111",
    "D-1": "001110",
    "A-1": "110010",
    "D+A": "000010",
    "D-A": "010011",
    "A-D": "000111",
    "D&A": "000000",
    "D|A": "010101"
}

M_COMP_CODES = {
    "M": "110000",
    "!M": "110001",
    "-M": "110111",
    "M+1": "110111",
    "M-1": "110010",
    "D+M": "000010",
    "D-M": "010011",
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


def addr_to_code(addr: int) -> str:
    return f"{addr:016b}"


def assemble(lines: Iterable[str]) -> Iterable[str]:
    symbol_to_addr : dict[str, int | list[int]] = PREDEFINED_SYMBOLS  # label name to address or to list of a-insruction addresses
    variables: list[str] = []

    next_instr_addr = 0
    code: list[str | None] = []
    for line_num, parse_res in parse(lines):
        print(line_num, next_instr_addr)
        if isinstance(parse_res, CInstr):
            code.append(assemble_cinstr(parse_res))
        elif isinstance(parse_res, AInstr):
            if isinstance(parse_res.addr, int):
                code.append(addr_to_code(parse_res.addr))
            else:
                label = parse_res.addr
                addr = symbol_to_addr.get(label)
                if addr is None:
                    symbol_to_addr[label] = [next_instr_addr]
                    code.append(None)
                    variables.append(label)
                elif isinstance(addr, int):
                    code.append(addr_to_code(addr))
                elif isinstance(addr, list):
                    addr.append(next_instr_addr)
                    code.append(None)
                else:
                    assert False, f"Invalid address value type {type(addr)}"
        if isinstance(parse_res, Label):
            addr = symbol_to_addr.get(parse_res.label)
            print(">", parse_res.label, addr)
            if addr is None:  # first label occurience
                symbol_to_addr[parse_res.label] = next_instr_addr
            elif isinstance(addr, str):
                raise RuntimeError(f"Error: label \"{parse_result.label}\" redefined at line {line_num}")
            elif isinstance(addr, list):
                for inst_addr in addr:
                    assert code[inst_addr] is None
                    code[inst_addr] = addr_to_code(next_instr_addr)
                symbol_to_addr[parse_res.label] = next_instr_addr
                if parse_res.label in variables:
                    variables.remove(parse_res.label)
        else:
            next_instr_addr += 1

    for var_addr, variable in enumerate(variables, 16):
        if not isinstance(symbol_to_addr[variable], list):
            continue
        for inst_addr in symbol_to_addr[variable]:
            assert code[inst_addr] is None
            code[inst_addr] = addr_to_code(var_addr)

    return code

