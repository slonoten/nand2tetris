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
        AM=M-1
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
        A=A-1
        M={op_command}
        """)

def _unary_op(op_name, op_command: str) -> str:
    return dedent(f"""
        // {op_name}
        @SP
        A=M-1
        M={op_command}
        """)

def _compare_op(op_name, jump_code, label):
    return dedent(f"""
        // {op_name}
        {_pop_to_d()}
        A=A-1
        D=M-D
        M=-1
        @{label}
        D;{jump_code}
        @SP
        A=M-1
        M=0
        ({label})
        """)
        
def zero_locals(n_vars: int) -> str:
    return f"""
        @SP
        A=M
        {'M=0\nA=A+1\n'*n_vars}
        D=A
        @SP
        M=D
    """


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
        return _binary_op("add", "D+M")

    def sub(self, args):
        return _binary_op("sub", "M-D")

    def neg(self, args):
        return _unary_op("neg", "-M")

    def and_(self, args):
        return _binary_op("and", "D&M")

    def or_(self, args):
        return _binary_op("or", "D|M")

    def not_(self, args):
        return _unary_op("not", "!M")

    def eq(self, args):
        return _compare_op("eq", "JEQ", self._get_next_label("EQ"))

    def gt(self, args):
        return _compare_op("gt", "JGT", self._get_next_label("GT"))

    def lt(self, args):
        return _compare_op("lt", "JLT", self._get_next_label("LT"))

    def program(self, commands):
        return "\n".join(map(str, commands))

    def function(self, args):
        name, n_vars = args
        n_vars = int(n_vars)
        return dedent(f"""
            ({name})
            {zero_locals(n_vars)}
            """)

    def label(self, args):
        name, = args
        return dedent(f"""
            ({name})
            """)

    def goto(self, args):
        label, = args
        return dedent(f"""
            @{label}
            0;JMP
            """)

    def return_(self, args):
        return dedent(f"""
            // return 
            //   *ARG = return value
            {_pop_to_d()}
            @ARG
            A=M
            M=D
            // save ARG to R13 to restore SP later
            D=A
            @R13
            M=D
            //   SP=LCL to restore frame
            @LCL
            D=M
            @SP
            M=D
            //   restore frame from stack
            {_pop_to_d()}
            @THAT
            M=D
            {_pop_to_d()}
            @THIS
            M=D
            {_pop_to_d()}
            @ARG
            M=D
            {_pop_to_d()}
            @LCL
            M=D
            // save return address to R14 
            {_pop_to_d()}
            @R14
            M=D
            // set SP to ARG+1 (ARG saved to R13)
            @R13
            D=M
            @SP
            M=D+1
            // jump to callie next after call instruction
            @R14
            A=M
            0;JMP
            """)

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
