import re
from typing import Iterable

from dataclasses import dataclass


LINE_PATTERN = r"\((?P<label_def>\w+)\)|(?://(?P<comment>.*))|(?:(?P<dest>[ADM]{1,3})=)?(?P<comp>[ADM\+\-01]{1,3})(?:;(?P<jump>J\w{1,2}))?|@(?:(?P<addr>\d{1,5})|(?P<label>[A-Za-z]\w*))$"

LINE_REGEXP = re.compile(LINE_PATTERN)


@dataclass
class CInstr:
    dest: str | None
    comp: str
    jump: str | None


@dataclass
class AInstr:
    addr: int | str


@dataclass
class Label:
    label: str


def parse_line(line: str) -> CInstr | AInstr | Label | None:
    line = line.strip()
    if not line:
        return None
    match = LINE_REGEXP.match(line)
    if not match:
        raise RuntimeError(f"Can't parse line \"{line}\"")
    if match.group("comment"):
        return None
    if label := match.group("label_def"):
        return Label(label)
    if addr := match.group("addr"):
        val = int(addr)
        if 0 > val >= 2 ** 15:
            raise ValueError(f"Value is out of range")
        return AInstr(val)
    if label := match.group("label"):
        return AInstr(label)
    comp = match.group("comp")
    assert comp, "Mandatory group not matched"
    return CInstr(match.group("dest"), comp, match.group("jump"))


def parse(lines: Iterable[str]) -> Iterable[tuple[int, CInstr|AInstr|Label]]:
    for i, line in enumerate(lines):
        try:
            if parse_res := parse_line(line):
                yield i, parse_res
        except Exception as exc:
            raise RuntimeError(f"Error parsing line {i}") from exc

