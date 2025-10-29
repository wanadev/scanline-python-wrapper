import nox


PYTHON_FILES = [
    "scanline_wrapper.py",
    "noxfile.py",
    "test",
    "doc",
]

PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("-e", ".[dev]")
    session.run("flake8", *PYTHON_FILES)
    session.run("black", "--check", "--diff", "--color", *PYTHON_FILES)
    session.run("validate-pyproject", "pyproject.toml")


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("-e", ".[dev]")
    session.run("black", *PYTHON_FILES)


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def test(session):
    session.install("-e", ".[dev]")
    session.install(".")
    session.run("pytest", "-v", "test")


@nox.session(reuse_venv=True)
def gendoc(session):
    session.install("-e", ".[dev]")
    session.install(".")
    session.run("sphinx-build", "-M", "html", "doc", "build")
