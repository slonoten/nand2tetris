from textwrap import dedent

from lark import Transformer


def _push_d() -> str:
    return dedent("""
        @SP
        A=M 
        M=D
        @SP
        M=M+1
        """).strip()


def _pop_d() -> str:
    return dedent("""
        @SP
        M=M-1
        A=M
        D=M
        """).strip()


def _copy_d_to_addr(base: str, offset: int) -> str:
    return f"""@{offset}
D=A
@{base}
A=D+M
D=M"""


def copy_addr_to_tmp(base: str, offset: int) -> str:
    return """@{offset}
D=A
${base}
D=D+M
@TMP
M=D
"""


def copy_D_to_tmp_indirect() -> str:
    return """@TMP
A=M
M=D
"""


def segment_to_d(segment: str) -> str:
    if segment == "local":
        return """
    """
SEGMENT_TO_REG = {
    "local" : "LCL",
    "argument" : "ARG",
    "this" : "THIS",
    "that" : "THAT"
}

POINTER_INDEX_TO_REG = {
    "0" : "THIS",
    "1" : "THAT"
}


def _segment_to_d(segment: str, index: str) -> str:
    
    if reg := SEGMENT_TO_REG.get(segment):
        return dedent(f"""
            @{index}
            D=A
            @{reg}
            A=D+M
            D=M
            """).strip()
    elif segment == "constant":
        return dedent(f"""
            @{index}
            D=A
            """).strip()
    elif segment == "pointer":
        reg = POINTER_INDEX_TO_REG[index]
        return dedent(f"""
        @{reg}
        D=M
        """).sprip()
    elif segment == "temp":
        TMP = 5
        address = TMP + int(index)
        return dedent(f"""
        @{address}
        D=M
        """).strip() 
        
    raise NotImplemented("No code for {segment}")


class CodeBuilder                                                                                       (Transformer):
    def push(self, args):
        segment, index = args
        return f"""// push {segment} {index}
{_segment_to_d(segment, index)}
{_push_d()}
"""

    def program(self, commands):
        return "\n".join(map(str, commands))

    