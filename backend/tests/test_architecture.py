"""Architectural guardrails.

ADR 001 depends on domain logic being callable from both an HTTP route and a Lambda
handler. That only holds if ``services/`` stays free of framework and AWS imports, so
the rule is enforced by a test rather than by memory.
"""

import ast
from pathlib import Path

FORBIDDEN = ("fastapi", "boto3", "sqlalchemy", "starlette")
SERVICES = Path(__file__).parent.parent / "src" / "tournament" / "services"


def _imported_modules(source: Path) -> set[str]:
    tree = ast.parse(source.read_text())
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            modules.add(node.module.split(".")[0])
    return modules


def test_services_layer_has_no_framework_or_aws_imports() -> None:
    offenders: list[str] = []
    for source in SERVICES.rglob("*.py"):
        for module in _imported_modules(source) & set(FORBIDDEN):
            offenders.append(f"{source.relative_to(SERVICES.parent)} imports {module}")

    assert not offenders, "services/ must stay pure domain logic (ADR 001): " + ", ".join(offenders)
