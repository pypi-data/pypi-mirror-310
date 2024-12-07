from pathlib import Path, PosixPath

from datamax.parser import CargoVisitor, cargo_grammar
from datamax.types import StepType


def test_parsing():
    with open("examples/basic.cargofile", "r") as f:
        source = f.read()
        visitor = CargoVisitor()
        tree = cargo_grammar.parse(source)
        parsed = visitor.visit(tree)
        assert tree is not None
        assert [item.model_dump() for item in parsed] == [
            {"type": StepType.EXTEND, "source": PosixPath("scratch")},
            {
                "type": StepType.INGEST,
                "source": Path("./data/sample.csv").resolve(),
                "source_extensions": [".csv"],
                "destination": "sample",
            },
        ]
