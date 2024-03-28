import nox


PYTHON_FILES = [
    "scanline_wrapper.py",
    "setup.py",
    "noxfile.py",
    "test",
    "doc",
]

PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black")
    session.run("flake8", *PYTHON_FILES)
    session.run("black", "--check", "--diff", "--color", *PYTHON_FILES)


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("black")
    session.run("black", *PYTHON_FILES)


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install(".")
    session.run("pytest", "-v", "test")


@nox.session(reuse_venv=True)
def gendoc(session):
    session.install("sphinx", "sphinx-rtd-theme")
    session.install(".")
    session.run("sphinx-build", "-M", "html", "doc", "build")
