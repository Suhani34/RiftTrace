from __future__ import annotations

import ast
from pathlib import Path


ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

ENGINE_DIR = (
    ROOT_DIR
    / "backend"
    / "simulation_engine"
)


FORBIDDEN_IMPORT_ROOTS = {
    "accounts",
    "api",
    "assets",
    "benchmarking",
    "business",
    "django",
    "evaluation",
    "identities",
    "ingestion",
    "organizations",
    "reporting",
    "requests",
    "rest_framework",
    "scenarios",
    "security",
    "simulations",
    "subprocess",
}


NONDETERMINISTIC_IMPORT_ROOTS = {
    "random",
    "secrets",
    "uuid",
}


FORBIDDEN_ATTRIBUTE_NAMES = {
    "objects",
}


FORBIDDEN_CALL_NAMES = {
    "print",
}


def production_python_files():
    for path in sorted(
        ENGINE_DIR.rglob("*.py")
    ):
        if "__pycache__" in path.parts:
            continue

        if "tests" in path.parts:
            continue

        yield path


def imported_root(
    module_name: str | None,
) -> str | None:
    if not module_name:
        return None

    return module_name.split(
        ".",
        maxsplit=1,
    )[0]


def check_file(
    path: Path,
) -> list[str]:
    problems: list[str] = []

    source = path.read_text(
        encoding="utf-8"
    )

    try:
        tree = ast.parse(
            source,
            filename=str(path),
        )

    except SyntaxError as exc:
        problems.append(
            (
                f"{path}: "
                f"syntax error: "
                f"{exc}"
            )
        )

        return problems


    for node in ast.walk(
        tree
    ):
        if isinstance(
            node,
            ast.Import,
        ):
            for alias in node.names:
                root = imported_root(
                    alias.name
                )

                if (
                    root
                    in FORBIDDEN_IMPORT_ROOTS
                ):
                    problems.append(
                        (
                            f"{path}:"
                            f"{node.lineno}: "
                            "forbidden import "
                            f"'{alias.name}'"
                        )
                    )

                if (
                    root
                    in NONDETERMINISTIC_IMPORT_ROOTS
                ):
                    problems.append(
                        (
                            f"{path}:"
                            f"{node.lineno}: "
                            "nondeterministic "
                            "dependency "
                            f"'{alias.name}'"
                        )
                    )


        elif isinstance(
            node,
            ast.ImportFrom,
        ):
            root = imported_root(
                node.module
            )

            if (
                node.level == 0
                and root
                in FORBIDDEN_IMPORT_ROOTS
            ):
                problems.append(
                    (
                        f"{path}:"
                        f"{node.lineno}: "
                        "forbidden import "
                        f"'{node.module}'"
                    )
                )

            if (
                node.level == 0
                and root
                in NONDETERMINISTIC_IMPORT_ROOTS
            ):
                problems.append(
                    (
                        f"{path}:"
                        f"{node.lineno}: "
                        "nondeterministic "
                        "dependency "
                        f"'{node.module}'"
                    )
                )


        elif isinstance(
            node,
            ast.Attribute,
        ):
            if (
                node.attr
                in FORBIDDEN_ATTRIBUTE_NAMES
            ):
                problems.append(
                    (
                        f"{path}:"
                        f"{node.lineno}: "
                        "possible ORM access "
                        f"'.{node.attr}'"
                    )
                )


        elif isinstance(
            node,
            ast.Call,
        ):
            if isinstance(
                node.func,
                ast.Name,
            ):
                if (
                    node.func.id
                    in FORBIDDEN_CALL_NAMES
                ):
                    problems.append(
                        (
                            f"{path}:"
                            f"{node.lineno}: "
                            "debug output call "
                            f"'{node.func.id}()'"
                        )
                    )


    return problems


def main():
    if not ENGINE_DIR.exists():
        raise SystemExit(
            (
                "simulation_engine directory "
                "was not found."
            )
        )


    files = list(
        production_python_files()
    )


    if not files:
        raise SystemExit(
            (
                "No simulation engine "
                "Python files were found."
            )
        )


    problems: list[str] = []


    for path in files:
        problems.extend(
            check_file(
                path
            )
        )


    print(
        (
            "Checked "
            f"{len(files)} "
            "simulation-engine files."
        )
    )


    if problems:
        print()
        print(
            "Architecture violations:"
        )

        for problem in problems:
            print(
                f" - {problem}"
            )

        raise SystemExit(1)


    print(
        (
            "Simulation engine "
            "architecture check passed."
        )
    )


if __name__ == "__main__":
    main()
