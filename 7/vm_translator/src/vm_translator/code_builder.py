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
            D=A
            """.strip()
    elif segment == "temp":
        TMP = 5
        address = TMP + int(index)
        return f"""
            @{address}
            D=A
            """ 

    raise NotImplemented("Segment {segment} no supported")


def _binary_op(op_name, op_command: str) -> str:
    return dedent(f"""
        // {op_name}
        {_pop_to_d()}
        @R13
        M=D
        {_pop_to_d()}
        @R13
        {op_command}
        {_push_d()}
        """)

def _unary_op(op_name, op_command: str) -> str:
    return dedent(f"""
        // {op_name}
        {_pop_to_d()}
        {op_command}
        {_push_d()}
        """)

def _compare_op(op_name, jump_code, label):
    return dedent(f"""
        // {op_name}
        {_pop_to_d()}
        @R13
        M=D
        {_pop_to_d()}
        @R13
        D=D-M
        @{label}
        D;{jump_code}
        D=0
        @{label}_end
        0;JMP
        ({label})
        D=-1
        ({label}_end)
        {_push_d()}
        """)


def dedent(text: str) -> str:
    return "\n".join(line.lstrip() for line in text.split("\n") if line.lstrip())


class CodeBuilder(Transformer):
    def __init__(self, namespace: str):
        self._label_counter = 0
        self._namespace = namespace

    def comment(self, args):
        comment_text, = args
        return comment_text
                                                                                            
    def push(self, args):
        segment, index = args
        return dedent(f"""
            // push {segment} {index}
            {self._segment_to_d(segment, index)}
            {_push_d()}
            """)

    def pop(self, args):
        segment, index = args
        comment = f"// pop {segment} {index}"
        if segment == "temp":
            return dedent(f"""
            {comment}
            {_pop_to_d()}
            @{5 + int(index)}
            M=D
            """)
        elif segment == "pointer":
            reg = POINTER_INDEX_TO_REG[index]
            return dedent(f"""
            {comment}
            {_pop_to_d()}
            @{reg}
            M=D
            """)
        elif segment == "static":
            return dedent(f"""
            {comment}
            {_pop_to_d()}
            @{self._namespace}.{index}
            M=D
            """)
        return dedent(f"""
            {comment}
            {_segment_addr_to_d(segment, index)}
            @R13
            M=D
            {_pop_to_d()}
            @R13
            A=M
            M=D
            """)

    def add(self, args):
        return _binary_op("add", "D=D+M")

    def sub(self, args):
        return _binary_op("sub", "D=D-M")

    def neg(self, args):
        return _unary_op("neg", "D=-D")

    def and_(self, args):
        return _binary_op("and", "D=D&M")

    def or_(self, args):
        return _binary_op("or", "D=D|M")

    def not_(self, args):
        return _unary_op("not", "D=!D")

    def eq(self, args):
        return _compare_op("eq", "JEQ", self._get_next_label("EQ"))

    def gt(self, args):
        return _compare_op("gt", "JGT", self._get_next_label("GT"))

    def lt(self, args):
        return _compare_op("lt", "JLT", self._get_next_label("LT"))

    def program(self, commands):
        return "\n".join(map(str, commands))

    def _segment_to_d(self, segment: str, index: str) -> str:
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
        elif segment == "static":
            return f"""
                @{self._namespace}.{index}
                D=M
                """.strip()
            
        raise NotImplemented("No code for {segment}")

    def _get_next_label(self, label_prefix: str) -> str:
        label = f"{label_prefix}_{self._label_counter}"
        self._label_counter += 1
        return label
