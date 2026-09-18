from lark import Transformer


def _push_d() -> str:
    return """
        @SP
        A=M 
        M=D
        @SP
        M=M+1
        """


def _pop_to_d() -> str:
    return """
        @SP
        M=M-1
        A=M
        D=M
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
        return f"""
            @{index}
            D=A
            @{reg}
            A=D+M
            D=M
            """.strip()
    elif segment == "pointer":
        reg = POINTER_INDEX_TO_REG[index]
        return f"""
            @{reg}
            D=M
            """.strip()
    elif segment == "temp":
        TMP = 5
        address = TMP + int(index)
        return f"""
            @{address}
            D=M
            """.strip()    
    elif segment == "constant":
        return f"""
            @{index}
            D=A
            """.strip()
        
    raise NotImplemented("No code for {segment}")


def _segment_addr_to_d(segment: str, index: str) -> str:
    if reg := SEGMENT_TO_REG.get(segment):
        return f"""
            @{index}
            D=A
            @{reg}
            D=D+M
            """.strip()
    elif segment == "pointer":
        reg = POINTER_INDEX_TO_REG[index]
        return f"""
            @{reg}
            D=M
            """.sprip()
    elif segment == "temp":
        TMP = 5
        address = TMP + int(index)
        return f"""
            @{address}
            D=M
            """ 

    raise NotImplemented("Segment {segment} no supported")


def binary_op(op_command: str) -> str:
        return dedent(f"""
            {_pop_to_d()}
            @R13
            M=D
            {_pop_to_d()}
            @R13
            {op_command}
            {_push_d()}
            """)


def dedent(text: str) -> str:
    return "\n".join(line.lstrip() for line in text.split("\n") if line.lstrip())


class CodeBuilder                                                                                       (Transformer):
    def push(self, args):
        segment, index = args
        return dedent(f"""
            // push {segment} {index}
            {_segment_to_d(segment, index)}
            {_push_d()}
            """)

    def pop(self, args):
        segment, index = args
        return dedent(f"""
            {_segment_addr_to_d(segment, index)}
            @R13
            M=D
            {_pop_to_d()}
            @R13
            A=M
            M=D
            """)

    def add(self, args):
        return binary_op("D=D+M")

    def program(self, commands):
        return "\n".join(map(str, commands))
