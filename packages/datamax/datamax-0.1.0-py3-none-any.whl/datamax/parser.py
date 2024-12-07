from pathlib import Path

from parsimonious import Grammar, NodeVisitor

from datamax.types import IngestStep, RunStep, StepType, StepWithSource

cargo_grammar = Grammar(r"""
    expr_group    = expr_stmt*
    expr_stmt     = generic_stmt / emptyline
    generic_stmt  = ingest_stmt / extend_stmt / run_stmt
    ingest_stmt   = ingest ws string ws string ws
    extend_stmt   = extend ws string ws
    run_stmt      = run ws any newline
    string        = ~r"[^\s]*"
    ingest        = "INGEST"
    extend        = "EXTEND"
    as            = "AS"
    run           = "RUN"
    ws            = ~r"[\s]*"
    ws_group      = ws*
    emptyline     = ws+
    newline       = ~r"[\n]"
    any           = ~r".*"
""")


class CargoVisitor(NodeVisitor):
    def visit_expr_stmt(self, node, visited_children):
        return visited_children

    def visit_expr_group(self, node, visited_children):
        filtered_children = [child for child in visited_children if any(child)]
        return [
            great_grandchild
            for child in filtered_children
            for grandchild in child
            for great_grandchild in grandchild
        ]

    def visit_generic_stmt(self, node, visited_children):
        return visited_children

    def visit_ingest_stmt(self, node, visited_children):
        abs_source_path = Path(visited_children[2])
        return IngestStep(
            type=StepType.INGEST,
            source=abs_source_path.resolve(),
            source_extensions=abs_source_path.suffixes,
            destination=visited_children[4],
        )

    def visit_extend_stmt(self, node, visited_children):
        return StepWithSource(type=StepType.EXTEND, source=visited_children[2])

    def visit_run_stmt(self, node, visited_children):
        directive = visited_children[2].text
        args = directive.split(" ")
        return RunStep(type=StepType.RUN, command=args)

    def visit_string(self, node, visited_children):
        return node.text

    def visit_ingest(self, node, visited_children):
        return node.text

    def visit_extend(self, node, visited_children):
        return node.text

    def visit_run(self, node, visited_children):
        return node.text

    def visit_ws(self, node, visited_children):
        return None

    def visit_ws_group(self, node, visited_children):
        return None

    def visit_emptyline(self, node, visited_children):
        return None

    def generic_visit(self, node, visited_children):
        return visited_children or node



class DatamaxProgram:
    def __init__(self, source: str):
        self.source = source

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, "r") as f:
            return cls(f.read())

    @property
    def steps(self):
        tree = cargo_grammar.parse(self.source)
        visitor = CargoVisitor()
        return visitor.visit(tree)
