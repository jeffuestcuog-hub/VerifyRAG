"""Build a public VerifyRAG archive only after scanning candidate files for secrets."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "VerifyRAG_public.zip"

CACHE_PARTS = {
    ".git",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "tmp",
}
TEXT_SUFFIXES = {
    ".cfg", ".csv", ".ini", ".ipynb", ".json", ".jsonl", ".md",
    ".py", ".rst", ".sv", ".svh", ".toml", ".txt", ".yaml", ".yml",
}
SECRET_PATTERNS = {
    "OpenRouter-style token": re.compile(r"sk-or-v1-[A-Za-z0-9_-]{20,}"),
    "private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "literal credential assignment": re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[\"']"
        r"(?!example|placeholder|test|your[-_ ]|<)[A-Za-z0-9_./+=-]{20,}[\"']"
    ),
}
SAFE_LIVE_EVIDENCE = {
    "records_compact.json",
    "records_posthoc_validator_v3.jsonl",
    "summary_posthoc_validator_v3.json",
    "preliminary_ai_source_review.csv",
    "preliminary_ai_source_review_summary.json",
}


def excluded(relative: Path, output: Path) -> bool:
    """Return True for files that must not enter the public archive."""
    if any(part in CACHE_PARTS for part in relative.parts):
        return True
    if relative.name == ".env" or relative.name.startswith(".env."):
        return True
    if relative.suffix.lower() in {".pyc", ".pyo"}:
        return True
    if (ROOT / relative).resolve() == output.resolve():
        return True
    if relative.name.startswith(".package-") and relative.suffix == ".zip":
        return True
    if relative.parts and relative.parts[0] == "results":
        if any(part.endswith("_live") for part in relative.parts[1:-1]) and relative.name not in SAFE_LIVE_EVIDENCE:
            return True
        if relative.name.startswith("latest_") and "_live" in relative.name:
            return True
        if relative.name == "live_progress.jsonl":
            return True
    return False


def public_files(output: Path) -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if not excluded(relative, output):
            files.append(path)
    return sorted(files, key=lambda path: path.as_posix().lower())


def scan_for_secrets(files: list[Path]) -> None:
    """Fail closed without printing any matched credential value."""
    findings = []
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{path.relative_to(ROOT).as_posix()}: {label}")
    if findings:
        details = "\n".join(f"  - {item}" for item in findings)
        raise SystemExit(
            "Secret-pattern scan failed. No archive was created. Review these files:\n" + details
        )


def build_archive(output: Path) -> Path:
    output = output.expanduser().resolve()
    files = public_files(output)
    scan_for_secrets(files)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=".package-", suffix=".zip", dir=output.parent, delete=False
    ) as stream:
        temporary = Path(stream.name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                archive.write(path, Path("VerifyRAG") / path.relative_to(ROOT))
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan public files for secrets, then build VerifyRAG_public.zip."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = build_archive(args.output)
    print(f"Public archive created: {output}")


if __name__ == "__main__":
    main()
