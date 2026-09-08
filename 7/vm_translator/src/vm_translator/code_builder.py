from lark import Transformer


def _push_d() -> str:
    return """@SP
A=M 
M=D
@SP
M=M+1
"""


def _pop_d() -> str:
    return """@SP
M=M-1
A=M
D=M
"""


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
    raise NotImplemented("No code for {segment}")


class CodeBuilder                                                                                       (Transformer):
    def push(self, args):
        segment, index = args
        print(segment, index)
        return "push"

    def program(self, commands):
        return "\n".join(map(str, commands))

    