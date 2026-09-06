from vm_translator.code_builder import CodeBuilder
from vm_translator.parser import parser

def test_code_builder():
    tree = parser.parse("push constant 1")
    print(CodeBuilder().transform(tree))
    assert False