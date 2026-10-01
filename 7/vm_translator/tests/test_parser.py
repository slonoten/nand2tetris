import pytest
from pathlib import Path

from vm_translator.parser import parser


BASE_DIR = Path(__file__).parent.parent.parent.parent


def test_push_constant():
    parser.parse("push constant 10")

def test_comment():
    parser.parse("// comment it!")

def test_function():
    parser.parse("function SimpleFunction.test 2")

def test_comments():
    parser.parse("""// line 1
// line 2""")

@pytest.mark.parametrize(
    "vm_path", 
    [
        BASE_DIR / "7"/ "MemoryAccess" / "BasicTest" / "BasicTest.vm",
        BASE_DIR / "8" / "FunctionCalls" / "SimpleFunction" / "SimpleFunction.vm"  
    ]
)
def test_vm_file(vm_path):
    vm = vm_path.read_text()
    parser.parse(vm)