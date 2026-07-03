from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_DIR_NAMES = {"sql", "oracle", "ssh", "listener", "awr", "ash", "alert_log"}
FORBIDDEN_CLASS_NAMES = {
    "OracleCollector",
    "OracleConnector",
    "SSHCollector",
    "SSHConnector",
    "ListenerCollector",
    "AlertLogCollector",
    "AWRCollector",
    "ASHCollector",
}
FORBIDDEN_DEPENDENCY_FRAGMENTS = {
    "anthropic",
    "asyncssh",
    "cx-oracle",
    "django",
    "fabric",
    "fastapi",
    "flask",
    "langchain",
    "llama-index",
    "mysqlclient",
    "openai",
    "oracledb",
    "paramiko",
    "psycopg",
    "pymysql",
    "sqlalchemy",
    "sqlite",
    "sqlite-utils",
    "sshtunnel",
    "starlette",
    "uvicorn",
}


def iter_project_files() -> list[Path]:
    ignored_parts = {".git", ".venv", "__pycache__", ".pytest_cache"}
    return [
        path
        for path in ROOT.rglob("*")
        if not any(part in ignored_parts for part in path.parts)
        and path.is_file()
    ]


def test_no_forbidden_future_phase_directories_exist() -> None:
    search_roots = [ROOT, ROOT / "src" / "oradiag"]
    dirs = set()
    for base in search_roots:
        if base.exists():
            dirs.update(
                path.name
                for path in base.rglob("*")
                if path.is_dir()
                and not {".git", ".venv", "__pycache__", ".pytest_cache"}.intersection(path.parts)
            )

    assert FORBIDDEN_DIR_NAMES.isdisjoint(dirs)


def test_no_sql_files_exist() -> None:
    ignored_parts = {".git", ".venv", "__pycache__", ".pytest_cache"}
    sql_files = [
        path.relative_to(ROOT)
        for path in ROOT.rglob("*.sql")
        if not ignored_parts.intersection(path.parts)
    ]

    assert sql_files == []


def test_no_forbidden_connector_class_names_exist() -> None:
    hits: list[str] = []
    for path in iter_project_files():
        if path.suffix != ".py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for class_name in FORBIDDEN_CLASS_NAMES:
            if f"class {class_name}" in text:
                hits.append(f"{path}:{class_name}")

    assert hits == []


def test_no_forbidden_dependencies_are_declared() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    dependencies = list(pyproject["project"].get("dependencies", []))
    for group in pyproject.get("dependency-groups", {}).values():
        dependencies.extend(group)
    lowered = "\n".join(dependencies).lower()

    assert all(fragment not in lowered for fragment in FORBIDDEN_DEPENDENCY_FRAGMENTS)


def test_examples_and_lab_fixtures_do_not_contain_secret_like_values() -> None:
    secret_fragments = (
        "access_key",
        "api_key",
        "credential",
        "passwd",
        "password",
        "private_key",
        "pwd",
        "secret",
        "token",
    )
    paths = []
    for base in [ROOT / "examples" / "lab", ROOT / "tests" / "fixtures" / "lab"]:
        if base.exists():
            paths.extend(path for path in base.rglob("*") if path.is_file())

    hits = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        if any(fragment in text for fragment in secret_fragments):
            hits.append(str(path.relative_to(ROOT)))

    assert hits == []
